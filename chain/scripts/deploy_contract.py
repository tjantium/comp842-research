from web3 import Web3
from solcx import compile_source
import solcx

# Connect to Ganache blockchain
ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))






# Deploy the contract
account = web3.eth.accounts[0]  # Use the first account for deployment
nonce = web3.eth.getTransactionCount(account)
gas_price = web3.eth.gas_price
gas_limit = 3000000  # Adjust as needed
chain_id = 5777  # Adjust for the correct chain ID


contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.constructor().buildTransaction({
    'chainId': chain_id,  # Adjust for the correct chain ID
    'from': account,
    'nonce': nonce,
    'gas': gas_limit,
    'gasPrice': gas_price,
})

signed_tx = web3.eth.account.signTransaction(tx_hash, private_key='0xd8c8d69a81130fe67d4abdd90aa24280a2609ba2fdd4041f3a981f9e6c48742d')
tx_receipt = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
contract_address = web3.eth.getTransactionReceipt(tx_receipt)['contractAddress']
print("Contract deployed at:", contract_address)