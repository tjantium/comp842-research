

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