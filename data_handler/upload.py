# IPFS module to upload data chunks and metadata to IPFS

# define a metadata schema for ipfs to validate node, and model metadata, accuracy,timestamp etc

import ipfshttpclient
import json
from dotenv import load_dotenv

load_dotenv()

class IPFS:
    def __init__(self):
        self.client = ipfshttpclient.connect('/ip4/')
        pass