from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables from environment
# web3_provider_http = os.getenv('WEB3_PROVIDER_HTTP')
# contract_address = os.getenv('CONTRACT_ADDRESS')
# account = Account.from_key(ganache_private_key)
# ipfs_hash = os.getenv('IPFS_HASH')
# private_key = os.getenv('PRIVATE_KEY')



web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Your Ganache URL
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


contract_address = "0xd0221388a73232325ce0641a8beca58b326d80bf"
# conver to checksum address
checksum_address = web3.to_checksum_address(contract_address)
contract_abi_path = "block_chain/build/contracts/SimpleStorage.json"

#  choose the first account from Ganache
ganache_private_key = "0xee9715fe3184b227d8967622f196b0d15900c79d8873472aabba99b6bcd6362d"
account = Account.from_key(ganache_private_key)

# Access the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Further usage of loaded variables for transactions or contract interactions
# For example, preparing a transaction
nonce = web3.eth.get_transaction_count(account_address)
transaction = contract.functions.storeIPFSHash(ipfs_hash).buildTransaction({
    'chainId': 1337,  # Adjust chainId according to your network
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'from': account_address
})

# Sign and send the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
