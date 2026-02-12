import hvac
import os

# Connect to Vault
client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='root'  # In production, use proper authentication
)

# Check if authenticated
if client.is_authenticated():
    print("✅ Connected to Vault")
    
    # Read secret
    secret = client.secrets.kv.v2.read_secret_version(path='mnist-model')
    
    model_path = secret['data']['data']['model_path']
    api_endpoint = secret['data']['data']['api_endpoint']
    
    print(f"Model Path: {model_path}")
    print(f"API Endpoint: {api_endpoint}")
else:
    print("❌ Failed to authenticate")