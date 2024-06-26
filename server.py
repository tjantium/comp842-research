from flask import Flask, request, jsonify
import torch
from torch import nn
import json
from werkzeug.utils import secure_filename
import os
import ipfshttpclient
import json
import datetime
import traceback
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account
from flask_restx import Api, Resource
from fed.fed_tss import split_weights_into_shares

app = Flask(__name__)

api = Api(app, version='1.0', title='API Documentation', description='A simple API')
ns = api.namespace('IPFS', description='IPFS operations')

# Assuming the same model structure as the clients
model = nn.Linear(2, 1)

# Store aggregated updates or initial model weights if starting fresh
# For simplicity, we initialize a dictionary to simulate the parameter averaging process
aggregated_weights = {name: torch.zeros_like(param) for name, param in model.named_parameters()}
client_count = 0

# configurtion for web3
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Your Ganache URL
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Correctly using the checksum address for all operations
contract_address = "0x7e1fcf190c223398b851047be094d8e4da564731"
checksum_address = web3.to_checksum_address(contract_address)
contract_abi_path = "block_chain/build/contracts/SimpleStorage.json"

# Load contract ABI from Truffle-generated artifacts
with open(contract_abi_path, 'r') as f:
    contract_data = json.load(f)
    contract_abi = contract_data['abi']

# Initialize the account with the private key
ganache_private_key = "0xab0f62f94a335b1bbee0e8ec3364f474fe2fb99d61b59b8748f873735b6328ae"
account = Account.from_key(ganache_private_key)
account_address = account.address
# Access the contract using the checksummed address
contract = web3.eth.contract(address=checksum_address, abi=contract_abi)


def deserialize_model(serialized_model):
    try:
        return {name: torch.tensor(weights) for name, weights in json.loads(serialized_model).items()}
    except Exception as e:
        raise ValueError(f"Failed to deserialize model: {e}")

def update_model(aggregated_weights, client_weights, client_count):
    try:
        for name in aggregated_weights:
            aggregated_weights[name] += client_weights[name]
        if client_count > 0:  # Avoid division by zero
            for name in aggregated_weights:
                aggregated_weights[name] /= client_count
        # Update server model
        with torch.no_grad():
            for name, param in model.named_parameters():
                param.copy_(aggregated_weights[name])
    except Exception as e:
        raise ValueError(f"Failed to update model: {e}")

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Max Upload Limit
# Connect to IPFS
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define allowed extensions
ALLOWED_EXTENSIONS = {'pth', 'npy', 'pt', 'h5'}
LOG_DIR = 'logs/'

def retrieve_data_from_logs():
    try:
        # Retrieve logs related to the IPFSHashStored event
        event_logs = contract.events.IPFSHashStored().getLogs()

        # Extract IPFS hash from the logs
        ipfs_hashes = [log['args']['ipfsHash'] for log in event_logs]

        # Write IPFS hashes to log file
        write_to_log(ipfs_hashes)

        return ipfs_hashes
    except Exception as e:
        print(f"Error retrieving data from contract logs: {e}")
        return None

def write_to_log(ipfs_hashes):
    try:
        # Create logs directory if it doesn't exist
        os.makedirs(LOG_DIR, exist_ok=True)
        # Generate log file name with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(LOG_DIR, f"log_{timestamp}.txt")

        # Write IPFS hashes to log file
        with open(log_file, 'w') as f:
            for ipfs_hash in ipfs_hashes:
                f.write(ipfs_hash + '\n')
        
        print(f"IPFS hashes written to log file: {log_file}")
    except Exception as e:
        print(f"Error writing to log file: {e}")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def log_to_contract(ipfs_hash, message, status):
    try:
        print(f"Logging to contract: {message}, Status: {status}")
        nonce = web3.eth.get_transaction_count(account_address)
        transaction = contract.functions.storeIPFSHash(ipfs_hash).build_transaction({
            'chainId': 1337,  # Adjust chainId according to your network
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'from': account_address
        })
        # Sign and send the transaction using the same private key
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=ganache_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 0:
            return False, tx_hash.hex(), "Transaction failed or reverted"
        return True, tx_hash.hex(), "Transaction successful"
    except Exception as e:
        return False, None, str(e)


def upload_to_ipfs(file_path):
    try:
        # Upload file to IPFS
        res = client.add(file_path)
        ipfs_hash = res['Hash']
        return ipfs_hash
    except Exception as e:
        print(f"Error uploading file to IPFS: {e}")
        return None


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if request.method != 'POST':
            return jsonify({"status": "error", "message": "Method not allowed"}), 405

        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected for uploading"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Upload to IPFS and log to contract
            ipfs_hash = upload_to_ipfs(file_path)
            if ipfs_hash:
                success, tx_hash, error_message = log_to_contract(ipfs_hash, f"File {filename} uploaded successfully.", "success")
                if success:
                    return jsonify({"status": "success", "message": "File uploaded and logged successfully.", "ipfs_hash": ipfs_hash, "tx_hash": tx_hash}), 200
                else:
                    return jsonify({"status": "error", "message": "Failed to log IPFS hash to the blockchain: " + error_message, "ipfs_hash": ipfs_hash}), 500
            else:
                return jsonify({"status": "error", "message": "Failed to upload file to IPFS"}), 500
        else:
            return jsonify({"status": "error", "message": "File type not allowed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/update_model', methods=['POST'])
def receive_updates():
    global client_count, aggregated_weights  # Include aggregated_weights in global declaration
    try:
        data = request.get_json()
        client_model = deserialize_model(data['model'])
        client_count += 1
        update_model(aggregated_weights, client_model, client_count)

        if client_count == 5:  # Reset after receiving updates from 5 clients
            # Average and update the model parameters
            for name in aggregated_weights:
                aggregated_weights[name] /= client_count
            with torch.no_grad():
                for name, param in model.named_parameters():
                    param.copy_(aggregated_weights[name])

            # Reset for the next round
            aggregated_weights = {name: torch.zeros_like(param) for name, param in model.named_parameters()}
            client_count = 0
            print("Model updated after receiving all client updates")
            return jsonify({"status": "success", "message": "Model updated and ready for new round"}), 200

        return jsonify({"status": "success", "message": "Update received but waiting for more"}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500


@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    try:
        # Call the contract's getIPFSHash function
        ipfs_hash = contract.functions.getIPFSHash().call()

        # Return the IPFS hash to the client
        return jsonify({"status": "success", "ipfs_hash": ipfs_hash}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500


@app.route('/get_tx_history', methods=['GET'])
def get_transaction_history():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        from_block = request.args.get('0x0', '0')
        to_block = request.args.get('to', 'latest')

        # filter = contract.events.IPFSHashStored.create_filter(fromBlock=from_block, toBlock=to_block)
        # Correctly specify the block numbers in hexadecimal
        block_number = 0
        hex_block_number = hex(block_number)  # Converts 0 to '0x0'
        nd_block = web3.eth.blockNumber

        filter = contract.events.IPFSHashStored.create_filter(fromBlock='0x0', ttoBlock=hex(end_block))

        events = filter.get_all_entries()

        # Implementing pagination
        start = (page - 1) * per_page
        end = start + per_page
        paginated_events = events[start:end]

        history = [{"blockNumber": event['blockNumber'], "sender": event['args']['sender'], "ipfsHash": event['args']['ipfsHash']} for event in paginated_events]
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/distribute_shares', methods=['GET'])
def distribute_shares():
    # Assuming model is globally defined and already trained or initialized
    shares = split_weights_into_shares(model, n=10, k=5)  # Example: 10 shares, threshold of 5
    # Serialize shares for transmission
    serialized_shares = [pickle.dumps(share).hex() for share in shares]
    # Store shares securely and send one share per client
    # In a real application, you would send each share to a different client securely
    return jsonify({"shares": serialized_shares}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
    # Example usage:
    # retrieve_data_from_logs()


