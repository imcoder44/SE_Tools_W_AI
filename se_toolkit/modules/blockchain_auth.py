# Blockchain Command Authorization
# For high-security operations

from web3 import Web3
import json
import os
import yaml
from eth_account.messages import encode_defunct
from utils.sanitize import clean_input

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connect to Ethereum network
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{config['blockchain']['infura_key']}"))

# Contract setup
CONTRACT_ADDRESS = config['blockchain']['contract_address']
with open('contract_abi.json') as f:
    CONTRACT_ABI = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def verify_signature(message, signature, address):
    """Verify cryptographic signature"""
    try:
        message = encode_defunct(text=clean_input(message))
        recovered_address = w3.eth.account.recover_message(message, signature=signature)
        return recovered_address.lower() == address.lower()
    except:
        return False

def is_authorized(command, executor):
    """Check if command is authorized on-chain"""
    try:
        return contract.functions.isCommandAuthorized(
            clean_input(command), 
            clean_input(executor)
        ).call()
    except:
        return False

def authorize_command(command, address):
    """Authorize a command via blockchain"""
    try:
        # Check if already authorized
        if is_authorized(command, address):
            return True
            
        # Create transaction
        tx = contract.functions.authorizeCommand(
            clean_input(command), 
            clean_input(address)
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gas': 200000
        })
        
        # Sign and send (requires private key in secure env)
        private_key = os.getenv(f"ETH_PK_{address}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    except Exception as e:
        print(f"⛓ Blockchain auth error: {str(e)}")
        return False

def log_to_blockchain(log_entry):
    """Create immutable log entry on blockchain"""
    try:
        admin_address = config['blockchain']['admin_addresses'][0]
        tx = contract.functions.createLogEntry(
            clean_input(json.dumps(log_entry))
        ).build_transaction({
            'from': admin_address,
            'nonce': w3.eth.get_transaction_count(admin_address)
        })
        
        private_key = os.getenv(f"ETH_PK_{admin_address}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()
    except:
        return None