const Web3 = require('web3');

const fs = require('fs');

// Connect to Ganache blockchain
const ganacheUrl = 'http://127.0.0.1:7545'; // Update with your Ganache URL
const web3 = new Web3(ganacheUrl);

// Read ABI and bytecode from files
const abi = JSON.parse(fs.readFileSync('chain/contracts/IPFSStorage_sol_IPFSStorage.abi', 'utf8'));
const bytecode = '0x' + fs.readFileSync('chain/contracts/IPFSStorage_sol_IPFSStorage.bin', 'utf8');

// Deploy the contract
const deployContract = async () => {
    try {
        // Get the contract instance
        const contract = new web3.eth.Contract(abi);

        // Deploy the contract
        const deployedContract = await contract.deploy({
            data: bytecode,
            arguments: [], // If your constructor requires arguments, provide them here
        }).send({
            from: '0x5942D4b96b410fB6909925dd5b44B79985766a6a', // Your account address
            gas: 2000000, // Adjust gas limit as needed
        });

        // Print the contract address
        console.log('Contract deployed at:', deployedContract.options.address);
    } catch (error) {
        console.error('Error deploying contract:', error);
    }
};

deployContract();
