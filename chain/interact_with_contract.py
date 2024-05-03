from web3 import Web3
import json
import logging
logging.getLogger("eth_typing").setLevel(logging.ERROR)

# Connect to Ganache blockchain
ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Read ABI from file
with open('contracts/IPFSStorage_sol_IPFSStorage.abi', 'r') as file:
    abi = json.load(file)

# Define contract address
contract_address = "0x5942D4b96b410fB6909925dd5b44B79985766a6a"  # Update with your deployed contract address

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Get transaction count for account
account = web3.eth.accounts[0]  # Use the first account for deployment
nonce = web3.eth.get_transaction_count(account)

print("Transaction count for account:", nonce)
