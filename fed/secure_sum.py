import syft as sy
import torch as th

def secure_sum_example():
    # Hook PyTorch to add extra functionalities to support Federated Learning and other privacy preserving techniques
    hook = sy.TorchHook(th)

    # Create a couple of workers
    alice = sy.VirtualWorker(hook, id="alice")
    bob = sy.VirtualWorker(hook, id="bob")
    secure_worker = sy.VirtualWorker(hook, id="secure_worker")

    # Data that Alice and Bob want to sum securely
    alice_data = th.tensor([5.]).send(alice)
    bob_data = th.tensor([3.]).send(bob)

    # Encrypt the data by sending it to the secure_worker
    # The data is now split between Alice and Bob, and both parts are encrypted
    alice_data = alice_data.fix_prec().share(alice, bob, crypto_provider=secure_worker)
    bob_data = bob_data.fix_prec().share(alice, bob, crypto_provider=secure_worker)

    # Secure computation
    secure_result = alice_data + bob_data

    # Decrypt the result
    result = secure_result.get().float_prec()
    print("Secure Sum:", result)

# Run the function
secure_sum_example()
