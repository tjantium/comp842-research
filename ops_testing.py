import ipfshttpclient

def check_file_exists(ipfs_client, file_hash):
    try:
        # Check if the file exists on the local node
        ipfs_client.get(file_hash)
        return True
    except ipfshttpclient.exceptions.ErrorResponse as e:
        # If the file is not found, ErrorResponse will be raised
        if "not found" in str(e).lower():
            return False
        else:
            # Handle other types of errors
            raise

def main():
    # Connect to the local IPFS node
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

    # IPFS hash of the file to be verified
    file_hash = "QmTzWgipYRwPHyKqD8z44xMFPj3x2hJ5WooTYCSshUi2qp"

    # Check if the file exists on the local node
    if check_file_exists(client, file_hash):
        print("File exists on the local IPFS node.")
    else:
        print("File does not exist on the local IPFS node.")

if __name__ == "__main__":
    main()



from web3 import Web3
from solcx import compile_standard

# IPFS file verification code
def check_file_exists(ipfs_client, file_hash):
    # Check if the file exists on the local node
    try:
        ipfs_client.get(file_hash)
        return True
    except ipfshttpclient.exceptions.ErrorResponse as e:
        if "not found" in str(e).lower():
            return False
        else:
            raise

# Connect to Ganache blockchain
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract ABI and address
abi = [...]  # Contract ABI
contract_address = "0x..."  # Contract address
contract = web3.eth.contract(address=contract_address, abi=abi)

# IPFS hash of the file to be verified
file_hash = "<your-file-hash>"

# Verify file existence on IPFS
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
if check_file_exists(client, file_hash):
    print("File exists on the local IPFS node.")
    
    # Store file hash on the Ethereum blockchain
    txn_hash = contract.functions.storeIPFSHash(file_hash).transact()
    receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    print("File hash stored on Ethereum blockchain:", receipt)
else:
    print("File does not exist on the local IPFS node.")
