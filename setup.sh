#!/bin/bash
# Ethical Social Engineering Toolkit Installer
# ONLY FOR AUTHORIZED PENETRATION TESTING

set -e

# Check root privileges
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root"
  exit 1
fi

echo "🛠️ Starting installation of Ethical SET..."

# System updates
echo "🔄 Updating system packages..."
apt update && apt full-upgrade -y

# Install core dependencies
echo "📦 Installing dependencies..."
apt install -y python3 python3-venv python3-pip nginx curl git whois dnsutils \
gpg tor openssl libssl-dev build-essential

# Create project structure
echo "📂 Creating project structure..."
mkdir -p se_toolkit/{config,modules,templates,utils,logs/archive}
touch se_toolkit/{recon.sh,app.py}
touch se_toolkit/config/settings.yaml
touch se_toolkit/templates/{login.html,redirect.html}
touch se_toolkit/modules/{__init__.py,mailer.py,analytics.py,osint.py,ai_content.py,blockchain_auth.py,voice_synthesis.py}
touch se_toolkit/utils/{sanitize.py,logger.sh,tor.py}

# Setup Python environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv se_toolkit/venv
source se_toolkit/venv/bin/activate

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install flask requests beautifulsoup4 pyyaml twilio openai web3 eth_account \
python-dotenv uwsgi stem 

# Set permissions
echo "🔒 Setting file permissions..."
chmod -R 750 se_toolkit
chmod 600 se_toolkit/config/settings.yaml

# Configure Tor hidden service
echo "🧅 Configuring Tor hidden service..."
# python3 - <<END
# from utils.tor import configure_tor_service
# configure_tor_service()
cd se_toolkit
source venv/bin/activate
python3 -c "from utils.tor import configure_tor_service; configure_tor_service()"
cd ..


# Generate default config
echo "⚙️ Creating default configuration..."
cat > se_toolkit/config/settings.yaml <<EOL
# Ethical SET Configuration
# WARNING: FOR AUTHORIZED TESTING ONLY

phishing:
  company_name: "SecureCorp"
  redirect_url: "https://example.com/auth-error"
  login_page_title: "Secure Portal Login"

server:
  host: "127.0.0.1"
  port: 5000
  use_ssl: true

mailer:
  smtp_server: "smtp.example.com"
  smtp_port: 587
  smtp_user: "user@example.com"
  smtp_pass: ""

twilio:
  account_sid: ""
  auth_token: ""
  from_number: "+1234567890"
  whatsapp_number: "+1234567890"

telegram:
  bot_token: ""
  default_chat_id: ""

security:
  log_encryption_key: "changeme-32char-encryption-key-here"
  max_input_length: 128

ai:
  openai_key: ""
  resembleai_key: ""

blockchain:
  infura_key: ""
  contract_address: "0x..."
  admin_addresses: 
    - "0xYourEthAddress"

tor:
  enabled: true
EOL

echo "✅ Installation complete!"
echo "ℹ️ Next steps:"
echo "1. Edit se_toolkit/config/settings.yaml"
echo "2. Generate SSL certs: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365"
echo "3. Place certs in se_toolkit directory"
echo ""
echo "⚠️  WARNING: Use only for AUTHORIZED penetration testing"
echo "⛓️ Blockchain Admin Addresses: $(grep 'admin_addresses' se_toolkit/config/settings.yaml)"