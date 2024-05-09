
# High-level architecture for the system.

```bash

+-----------+       +-------------+       +-------------------+
|           |       |             |       |                   |
|   Client  +------>+  server.py  +------>+  Smart Contract   |
|           |       |  (Flask API)|       |  (Ethereum Block- |
+-----------+       +-------------+       |  chain)           |
        |                                +-------------------+
        |                                           ^
        |                                           |
        v                                           |
+------------------+                                |
|    Encrypt and   |                                |
|  Upload to IPFS  +--------------------------------+
+------------------+                                |
        |                                           |
        v                                           |
+------------------+                                |
|    IPFS Hash     |                                |
|  Registration    +--------------------------------+
+------------------+


```


## Detailed Flow Explanation

### Client
- **Action**: The client encrypts their portion of the data.

### Encrypt and Upload to IPFS
- **Action**: The encrypted data is uploaded to IPFS directly from the client or through the server acting as a mediator.

### IPFS Hash Registration
- **Action**: After receiving the hash from IPFS, the client or server registers this hash on the Ethereum blockchain via the smart contract. This step ensures that the data's existence and its integrity are verifiable and traceable via blockchain.

### Smart Contract on Ethereum Blockchain
- **Action**: The smart contract handles the registration of IPFS hashes, maintaining a ledger of data uploads and potentially other operations such as access control or triggering further actions based on the data.

## Enhanced Descriptions for Each Component

### Client
- **Role**: Encrypts data, interacts with the server to handle data, and possibly directly with IPFS and the blockchain.
- **Processes**:
  1. Data encryption.
  2. Upload encrypted data to IPFS.
  3. Receive IPFS hash and register it on the blockchain.

### server.py (Flask API)
- **Role**: Acts as an intermediary that may assist in handling data, interacting with IPFS, and communicating with the blockchain.
- **Processes**:
  1. Facilitate encrypted data uploads to IPFS if needed.
  2. Assist in registering the IPFS hash on the blockchain.

### Smart Contract (Ethereum Blockchain)
- **Role**: Manages the registration and tracking of IPFS hashes, ensuring data traceability and integrity.
- **Processes**:
  1. Registers IPFS hashes submitted by clients or the server.
  2. Manages access control or other logic related to the data stored on IPFS.

### IPFS
- **Role**: Decentralized storage for the encrypted data.
- **Processes**:
  1. Receives encrypted data uploads.
  2. Provides hashes of the stored data for blockchain registration.
