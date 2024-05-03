from flask import Flask, request, jsonify
import torch
from torch import nn
import json
from werkzeug.utils import secure_filename
import os
import ipfshttpclient


app = Flask(__name__)

# Assuming the same model structure as the clients
model = nn.Linear(2, 1)

# Store aggregated updates or initial model weights if starting fresh
# For simplicity, we initialize a dictionary to simulate the parameter averaging process
aggregated_weights = {name: torch.zeros_like(param) for name, param in model.named_parameters()}
client_count = 0

def deserialize_model(serialized_model):
    return {name: torch.tensor(weights) for name, weights in json.loads(serialized_model).items()}

def update_model(aggregated_weights, client_weights, client_count):
    for name in aggregated_weights:
        aggregated_weights[name] += client_weights[name]
    if client_count > 0:  # Avoid division by zero
        for name in aggregated_weights:
            aggregated_weights[name] /= client_count
    # Update server model
    with torch.no_grad():
        for name, param in model.named_parameters():
            param.copy_(aggregated_weights[name])


# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Max Upload Limit
# Connect to IPFS
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define allowed extensions
ALLOWED_EXTENSIONS = {'pth', 'npy', 'pt', 'h5'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"status": "error", "message": "No file part in the request"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"status": "error", "message": "No file selected for uploading"}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         try:
#             file.save(file_path)
#             # Optionally load and update the model here if needed
#             return jsonify({"status": "success", "message": f"File {filename} uploaded successfully."}), 200
#         except Exception as e:
#             return jsonify({"status": "error", "message": f"Failed to save the file: {str(e)}"}), 500
#     else:
#         return jsonify({"status": "error", "message": "File type not allowed"}), 400



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected for uploading"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            # Upload to IPFS
            res = client.add(file_path)
            ipfs_hash = res['Hash']
            # Optionally load and update the model here if needed
            return jsonify({"status": "success", "message": f"File {filename} uploaded successfully.", "ipfs_hash": ipfs_hash}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Failed to save the file: {str(e)}"}), 500
    else:
        return jsonify({"status": "error", "message": "File type not allowed"}), 400



@app.route('/api/update_model', methods=['POST'])
def receive_updates():
    global client_count, aggregated_weights  # Include aggregated_weights in global declaration
    data = request.get_json()
    client_model = deserialize_model(data['model'])
    client_count += 1
    update_model(aggregated_weights, client_model, client_count)

    if client_count == 5:  # Reset after receiving updates from 5 clients
        # Average and update the model parameters
        for name in aggregated_weights:
            aggregated_weights[name] /= client_count
        with torch.no_grad():
            for name, param in model.named_parameters():
                param.copy_(aggregated_weights[name])

        # Reset for the next round
        aggregated_weights = {name: torch.zeros_like(param) for name, param in model.named_parameters()}
        client_count = 0
        print("Model updated after receiving all client updates")
        return jsonify({"status": "success", "message": "Model updated and ready for new round"}), 200

    return jsonify({"status": "success", "message": "Update received but waiting for more"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
