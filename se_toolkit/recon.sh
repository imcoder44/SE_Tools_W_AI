#!/bin/bash
# Advanced OSINT Reconnaissance Module
# For authorized security testing only

if [ -z "$1" ]; then
  echo "❌ Usage: $0 <domain>"
  exit 1
fi

DOMAIN=$1
OUTPUT_DIR="recon_data"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔍 Starting reconnaissance on $DOMAIN..."
echo "⚠️ Legal Notice: Only perform on systems you have explicit permission to test"

mkdir -p $OUTPUT_DIR

# Basic reconnaissance
echo "🕵️  Performing WHOIS lookup..."
whois $DOMAIN > "$OUTPUT_DIR/${DOMAIN}_whois_$TIMESTAMP.txt"

echo "📡 Querying DNS records..."
dig $DOMAIN ANY +noall +answer > "$OUTPUT_DIR/${DOMAIN}_dns_$TIMESTAMP.txt"

echo "🌐 Checking subdomains..."
subfinder -d $DOMAIN -silent > "$OUTPUT_DIR/${DOMAIN}_subdomains_$TIMESTAMP.txt" 2>/dev/null || 
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' > "$OUTPUT_DIR/${DOMAIN}_subdomains_$TIMESTAMP.txt"

# Advanced OSINT with AI
echo "🤖 Running AI-enhanced OSINT collection..."
python3 - <<END
from modules.osint import gather_osint
from modules.ai_content import generate_target_profile
import json

if __name__ == "__main__":
    # Basic OSINT
    data = gather_osint("$DOMAIN")
    
    # AI-enhanced analysis
    ai_profile = generate_target_profile(data)
    data['ai_analysis'] = ai_profile
    
    # Save comprehensive report
    with open("$OUTPUT_DIR/${DOMAIN}_full_$TIMESTAMP.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ OSINT gathered: {len(data.get('profiles', []))} profiles")
    print(f"🤖 AI generated profile summary")
END

echo "💾 Recon data saved to $OUTPUT_DIR/"
echo "🔐 Encrypting sensitive data..."
gpg --batch --passphrase "$(grep 'log_encryption_key' config/settings.yaml | cut -d' ' -f2)" \
--symmetric "$OUTPUT_DIR/${DOMAIN}_full_$TIMESTAMP.json"

echo "⚠️  LEGAL DISCLAIMER: Use only with explicit authorization"