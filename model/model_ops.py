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
