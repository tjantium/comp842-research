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