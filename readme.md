

## scope of the FL 

Client-side: Clients pull the model from the server, train locally, and send updates back.
Server-side: The server aggregates these updates to improve the global model.


## block chain

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
                         ^                +-------------------+
                         |
                         v
                +------------------+
                | External Systems |
                | (e.g., Database, |
                |  IPFS, etc.)     |
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


## TroubleShooting

Flask App Not Starting: Ensure all dependencies are installed and environment variables are set. Check the terminal for any specific error messages.
Ganache CLI Errors: Make sure that Ganache CLI is not already running on the same port. If errors persist, try restarting Ganache CLI with a different port.
Truffle Migration Issues: Confirm that Ganache CLI is running and accessible. Ensure your truffle-config.js file has the correct configurations for the development network.
Connection Issues with Ganache: Verify network configuration in both your Flask app and Truffle settings. Ensure they are pointing to the same Ganache instance.

