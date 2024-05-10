import torch
from Crypto.Protocol.SecretSharing import Shamir
import pickle

def serialize_model_weights(model):
    # Convert model weights to a byte array
    model_weights = {k: v.cpu().numpy() for k, v in model.state_dict().items()}
    return pickle.dumps(model_weights)

def deserialize_model_weights(weight_bytes):
    # Convert byte array back to model weights
    model_weights = pickle.loads(weight_bytes)
    return {k: torch.tensor(v) for k, v in model_weights.items()}

def split_weights_into_shares(model, n, k):
    # Serialize model weights to bytes
    weight_bytes = serialize_model_weights(model)
    # Split bytes into shares using Shamir's Secret Sharing
    shares = Shamir.split(k, n, weight_bytes)
    return shares

def combine_shares_to_weights(shares):
    # Combine shares into the original bytes
    weight_bytes = Shamir.combine(shares)
    # Deserialize bytes back to model weights
    model_weights = deserialize_model_weights(weight_bytes)
    return model_weights
