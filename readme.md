
# Blockchain-Based enhanced Federated Learning with Threshold Secret Sharing (TSS)

- Problem trying to solve 
    - True purpose of  a federated ML is to make sure that maintain privacy of the data, and making sure the model got integrity.  This is not exposed to attack vectors.
    - The current federated ML systems are distributed and the overhead cost of implementation, maintaining those are expensive , consume tons  of infra , require specific skill sets to integrate with current technology in place. 
    - Often hard to scale.
    - Often doesn’t work as expected. 
- Solution
    - By trying to introduce the new layer of validation using blockchain and reduce the complexity around implementation and integration. Be able to extend that concept to wider compute resources and be able to fast track ML model training, and bridge the gap between current computer bottle necks, in a much secure way. 

    
## Scope of the FL 

Client-side: Clients pull the model from the server, train locally, and send updates back.
Server-side: The server aggregates these updates to improve the global model.


## Blockchain

Use a blockchain to record hashes of model updates and metadata about the training rounds.
Every transaction (model update sent to and from the server) can be recorded as a blockchain transaction.
Use smart contracts for automated tasks, like triggering model updates when certain conditions are met.

## some low-level frameworks to apply concepts

- e.g. using PySyft for homomorphic encryption and secure multi-party computation. ( Scope down to the multipart using tss as a novel approach)

## How to Use TSS in Federated Learning

- Distribute Model Weights Using TSS:
- At the server: Model weights can be split into multiple shares using TSS before being sent to the clients. This means that no single client has access to the full - model information, adding an extra layer of privacy.
- At the client: Each client receives a share of the model weights, trains locally, and sends back a share of the updated weights.
- Reconstruct and Aggregate Model Weights:
- At the server: When the server receives enough shares from the clients (meeting the threshold), it can reconstruct the updated model weights. This aggregation can then be used to update the global model.



```bash

+-----------+       +-------------+       +-------------------+
|           |       |             |       |                   |
|   Client  +------>+  server.py  +------>+  Smart Contract   |
|           |       |  (Flask API)|       |  (Ethereum Block- |
+-----------+       +-------------+       |  chain)           |
        |                                 +-------------------+
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


## How to Use TSS in Federated Learning

- Distribute Model Weights Using TSS:
- At the server: Model weights can be split into multiple shares using TSS before being sent to the clients. This means that no single client has access to the full - model information, adding an extra layer of privacy.
- At the client: Each client receives a share of the model weights, trains locally, and sends back a share of the updated weights.
- Reconstruct and Aggregate Model Weights:
- At the server: When the server receives enough shares from the clients (meeting the threshold), it can reconstruct the updated model weights. This aggregation can then be used to update the global model.


## Components
### Smart Contract
- Deployed on Ethereum.
- Manages storage and retrieval of IPFS hashes.

### server.py (Flask API)
- Interfaces between the client and the smart contract.
- Handles all client requests and communicates with the blockchain.

### Client
- Interacts with the Flask API to perform operations on the blockchain.

## Setup and Running
Describe how to set up and run the project here.


## Setup Guidelines

### Prerequisites
- Node.js and npm: [Download & Install Node.js](https://nodejs.org/en/download/)
- Python: [Download & Install Python](https://www.python.org/downloads/)
- Flask: Install via pip:
  ```bash
  pip install Flask

- Web3.py: Install via pip:
  ```bash
  pip install web3
  ```

### Installation other dependencies

- Install other dependencies:
  ```bash
  npm install
  ```

- Install Ganache CLI:
  ```bash
  npm install -g ganache-cli
  ```

- Install truffle:
  ```bash
  npm install -g truffle
  ```

- Download and install IPFS: [IPFS Installation](https://docs.ipfs.io/install/command-line/)
- Start IPFS daemon:
  ```bash
  ipfs daemon
  ```

## Running Server/ Client

running server 

```bash
python server.py
```

running client

```bash
python client.py
```


Successfully running the server and client will allow you to interact with the blockchain and perform various operations.


e.g.

```bash 
(comp842p) ➜  comp842-research git:(contract) ✗ python client.py
Epoch 1, Loss: 0.3872787058353424
Epoch 2, Loss: 0.36850738525390625
Epoch 3, Loss: 0.3506479263305664
Epoch 4, Loss: 0.33365580439567566
Epoch 5, Loss: 0.3174889385700226
Epoch 6, Loss: 0.3021070063114166
Epoch 7, Loss: 0.2874719202518463
Epoch 8, Loss: 0.2735472023487091
Epoch 9, Loss: 0.26029837131500244
Epoch 10, Loss: 0.24769258499145508
Model saved locally at local_model.pth
Model file uploaded successfully.
Server response: {
  "ipfs_hash": "QmTK27Vv8ZNqmm6BR4NSNaKbYDcmFRBvE8M9FRoRr6MVfm",
  "message": "File uploaded and logged successfully.",
  "status": "success",
  "tx_hash": "0x3538b5319d60692095cd90cdf1d977a74a5c77485692891bee39c89a69292acd"
}
```


## TroubleShooting

Flask App Not Starting: Ensure all dependencies are installed and environment variables are set. Check the terminal for any specific error messages.
Ganache CLI Errors: Make sure that Ganache CLI is not already running on the same port. If errors persist, try restarting Ganache CLI with a different port.
Truffle Migration Issues: Confirm that Ganache CLI is running and accessible. Ensure your truffle-config.js file has the correct configurations for the development network.
Connection Issues with Ganache: Verify network configuration in both your Flask app and Truffle settings. Ensure they are pointing to the same Ganache instance.

