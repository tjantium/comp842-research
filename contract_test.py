import os
import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Your Ganache URL
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Correctly using the checksum address for all operations
contract_address = "0xd0221388a73232325ce0641a8beca58b326d80bf"
checksum_address = web3.to_checksum_address(contract_address)
contract_abi_path = "block_chain/build/contracts/SimpleStorage.json"

# Load contract ABI from Truffle-generated artifacts
with open(contract_abi_path, 'r') as f:
    contract_data = json.load(f)
    contract_abi = contract_data['abi']

# Initialize the account with the private key
ganache_private_key = "0xee9715fe3184b227d8967622f196b0d15900c79d8873472aabba99b6bcd6362d"
account = Account.from_key(ganache_private_key)
account_address = account.address

# Access the contract using the checksummed address
contract = web3.eth.contract(address=checksum_address, abi=contract_abi)

# Example IPFS hash to store
ipfs_hash = "QmSomeHashHere"

# Preparing the transaction
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

# Output the transaction receipt
print(receipt)
