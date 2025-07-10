# Secure Analytics and Logging Module
# Includes Blockchain-Auditable Logging

import json
import os
import datetime
import hashlib
import yaml
from collections import defaultdict
from utils.logger import rotate_logs, encrypt_log
from utils.sanitize import clean_input

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

LOG_DIR = "logs"
CURRENT_LOG = os.path.join(LOG_DIR, "events.log")
DASHBOARD_FILE = os.path.join(LOG_DIR, "dashboard.json")

# Blockchain integration
try:
    from modules.blockchain_auth import log_to_blockchain
    BLOCKCHAIN_LOGGING = config['blockchain'].get('enabled', False)
except:
    BLOCKCHAIN_LOGGING = False

def log_event(event_data):
    """Securely log event with encryption and optional blockchain"""
    try:
        # Rotate logs if needed
        if config['logging'].get('rotation', True):
            rotate_logs()
        
        # Add metadata
        timestamp = datetime.datetime.utcnow().isoformat()
        event_data['timestamp'] = timestamp
        event_id = hashlib.sha256(
            f"{timestamp}{event_data.get('ip','')}{event_data.get('type','')}".encode()
        ).hexdigest()[:16]
        event_data['event_id'] = event_id
        
        # Append to log
        with open(CURRENT_LOG, 'a') as logfile:
            logfile.write(json.dumps(event_data) + '\n')
            
        # Encrypt logs
        if config['logging'].get('encryption', True):
            encrypt_log(CURRENT_LOG, config['security']['log_encryption_key'])
        
        # Blockchain audit trail for critical events
        if BLOCKCHAIN_LOGGING and event_data.get('type') in ['credential', 'admin_action']:
            log_to_blockchain(json.dumps({
                'event_id': event_id,
                'event_type': event_data.get('type'),
                'timestamp': timestamp
            }))
        
        return True
    except Exception as e:
        print(f"📊 Logging error: {str(e)}")
        return False

def generate_realtime_dashboard():
    """Generate real-time analytics dashboard with AI insights"""
    # Aggregate data (simplified)
    stats = defaultdict(int)
    locations = defaultdict(int)
    user_agents = defaultdict(int)
    
    try:
        # Read logs (decrypt if needed)
        log_data = []
        if os.path.exists(CURRENT_LOG + ".enc"):
            from utils.logger import decrypt_log
            decrypt_log(CURRENT_LOG + ".enc", config['security']['log_encryption_key'])
            
        if os.path.exists(CURRENT_LOG):
            with open(CURRENT_LOG, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        stats[event.get('type', 'unknown')] += 1
                        
                        if 'ip' in event:
                            locations[event['ip']] += 1
                            
                        if 'user_agent' in event:
                            ua = event['user_agent'][:50]  # Truncate long UAs
                            user_agents[ua] += 1
                            
                        log_data.append(event)
                    except:
                        continue
        
        # Generate summary
        dashboard = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'total_events': sum(stats.values()),
            'event_types': dict(stats),
            'top_ips': sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10],
            'top_user_agents': sorted(user_agents.items(), key=lambda x: x[1], reverse=True)[:5]
        }
        
        # AI-powered threat analysis
        if config['ai'].get('openai_key') and log_data:
            try:
                from modules.ai_content import analyze_threats
                dashboard['ai_analysis'] = analyze_threats(log_data)
            except:
                pass
        
        # Save dashboard snapshot
        with open(DASHBOARD_FILE, 'w') as f:
            json.dump(dashboard, f)
        
        return jsonify(dashboard)
    except Exception as e:
        return jsonify({'error': str(e)}), 500