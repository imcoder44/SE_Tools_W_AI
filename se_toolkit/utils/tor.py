# Tor Hidden Service Integration
# For anonymity in authorized testing

import stem.process
from stem.control import Controller
import yaml
import os
import time
import logging

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(filename='tor.log', level=logging.INFO)

def configure_tor_service():
    """Configure Tor hidden service"""
    try:
        service_dir = config['tor'].get('service_dir', '/var/lib/tor/hidden_service/')
        
        # Create directory
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)
        
        # Update torrc configuration
        torrc_path = "/etc/tor/torrc"
        with open(torrc_path, "a") as torrc:
            torrc.write("\n\n# Ethical SET Configuration")
            torrc.write(f"\nHiddenServiceDir {service_dir}")
            torrc.write("\nHiddenServicePort 80 127.0.0.1:5000")
            if config['tor'].get('control_password'):
                torrc.write(f"\nHashedControlPassword {hash_password(config['tor']['control_password'])}")
        
        # Restart Tor service
        os.system("systemctl restart tor")
        logging.info("Tor hidden service configured")
        return True
    except Exception as e:
        logging.error(f"Tor configuration error: {str(e)}")
        return False

def get_onion_address():
    """Get Tor hidden service address"""
    service_dir = config['tor'].get('service_dir', '/var/lib/tor/hidden_service/')
    hostname_file = os.path.join(service_dir, "hostname")
    
    try:
        with open(hostname_file, "r") as f:
            return f.read().strip()
    except:
        return None

def start_tor_proxy():
    """Start Tor proxy service"""
    try:
        tor_process = stem.process.launch_tor_with_config(
            config = {
                'SocksPort': '9050',
                'ControlPort': '9051',
                'DataDirectory': '/tmp/tor-data',
                'Log': 'notice stdout'
            }
        )
        logging.info("Tor proxy started")
        return tor_process
    except Exception as e:
        logging.error(f"Tor start error: {str(e)}")
        return None

def hash_password(password):
    """Hash password for Tor control port"""
    from hashlib import sha1
    from binascii import b2a_hex
    salt = os.urandom(8)
    hash = sha1(password.encode('utf8'))
    hash.update(salt)
    return "16:" + b2a_hex(salt).decode('utf8') + b2a_hex(hash.digest()).decode('utf8')