// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract SimpleStorage {
    // Mapping to store IPFS file hashes associated with Ethereum addresses
    mapping(address => string) public ipfsHashes;

    // Event emitted when a new IPFS file hash is stored
    event IPFSHashStored(address indexed sender, string ipfsHash);

    // Function to store an IPFS file hash
    function storeIPFSHash(string memory _ipfsHash) public {
        // Store the IPFS file hash associated with the sender's address
        ipfsHashes[msg.sender] = _ipfsHash;
        // Emit an event to notify listeners that a new IPFS file hash has been stored
        emit IPFSHashStored(msg.sender, _ipfsHash);
    }

    // Function to retrieve the IPFS file hash associated with an address
    function getIPFSHash(address _address) public view returns (string memory) {
        return ipfsHashes[_address];
    }
}