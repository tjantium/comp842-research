import torch
from torch import nn, optim
import requests
import json

# Assuming the model and optimizer have been defined similarly to the server script
model = nn.Linear(2, 1)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Load your local dataset here
# For demonstration, we will use dummy data:
X_train = torch.tensor([[1., 2], [2., 3], [3., 4]], dtype=torch.float32)
y_train = torch.tensor([[1.], [2.], [3.]], dtype=torch.float32)
X_train = (X_train - X_train.mean()) / X_train.std()
y_train = (y_train - y_train.mean()) / y_train.std()

# Local training function
def train_local_model(X_train, y_train):
    for epoch in range(10):  # number of epochs
        optimizer.zero_grad()
        output = model(X_train)
        loss = nn.MSELoss()(output, y_train)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")
    return model

# Function to save the model locally
def save_model_locally(model, filepath):
    torch.save(model.state_dict(), filepath)
    print(f"Model saved locally at {filepath}")

# Function to send model file to the server
def upload_model_to_server(filepath):
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:5003/upload", files=files)
            if response.status_code == 200:
                print("Model file uploaded successfully.")
            else:
                print("Failed to upload model file. Server responded with status code:", response.status_code)
            print("Server response:", response.text)  # Print server response for debugging
            return response.status_code
    except Exception as e:
        print("An error occurred while uploading the model file:", str(e))
        return None


def retrieve_data_from_server():
    try:
        response = requests.get("http://localhost:5003/retrieve_data")
        if response.status_code == 200:
            data = response.json()
            ipfs_hash = data.get("ipfs_hash")
            if ipfs_hash:
                return ipfs_hash
            else:
                print("No IPFS hash found in the response.")
                return None
        else:
            print("Failed to retrieve data from server. Server responded with status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred while retrieving data from server:", str(e))
        return None


def get_transaction_history(url):
    try:
        # Sending a GET request to the Flask server's endpoint
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print or process the JSON data returned from the server
            transaction_history = response.json()
            print("Transaction History Retrieved Successfully:")
            for entry in transaction_history:
                print(entry)
        else:
            print("Failed to retrieve transaction history, Status Code:", response.status_code)
    except Exception as e:
        print("An error occurred while trying to fetch transaction history:", str(e))


def receive_and_train_share(share):
    # Example function to handle a share
    local_model_weights = reconstruct_weights_from_shares([share])  # If allowed and secure
    train_local_model(local_model_weights)
    updated_weights = model.state_dict()
    updated_share = split_weights_into_shares(updated_weights, 1, 1)[0]  # Split updated weights into one share
    return updated_share


def send_update_to_server(updated_share):
    response = requests.post("http://localhost:5003/receive_update", json={"share": updated_share})
    print("Response from server:", response.status_code, response.text)


def upload_model_update_to_ipfs(model_weights):
    # Serialize and save model weights to a file or handle directly if IPFS client supports
    filename = 'updated_weights.pth'
    torch.save(model_weights, filename)
    ipfs_hash = upload_to_ipfs(filename)
    return ipfs_hash

def notify_server_of_update(ipfs_hash):
    # Sending the IPFS hash back to the server
    data = {'ipfs_hash': ipfs_hash}
    response = requests.post("http://localhost:5003/model_update_notification", json=data)
    return response.status_code

# Main execution function
if __name__ == "__main__":
    model = train_local_model(X_train, y_train)
    model_filepath = "local_model.pth"
    save_model_locally(model, model_filepath)  # Save the model to a file
    status_code = upload_model_to_server(model_filepath)
    if status_code == 200:
        print("Model uploaded successfully.")
    else:
        print("Failed to upload the model file.")
