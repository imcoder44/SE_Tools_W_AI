# Advanced Multi-Channel Delivery Module
# Only for authorized security testing

import yaml
import smtplib
from twilio.rest import Client
import requests
import json
import time
import random
from utils.sanitize import clean_input

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Delivery timing randomization
MIN_DELAY = 1  # seconds
MAX_DELAY = 30 # seconds

def random_delay():
    """Random delay to avoid pattern detection"""
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY))

def send_email(to, subject, body, importance=5):
    """Send AI-crafted phishing email"""
    try:
        # Blockchain authorization for high-impact emails
        if importance > 7 and config['blockchain']['enabled']:
            from modules.blockchain_auth import authorize_command
            if not authorize_command(f"SEND_EMAIL:{to}:{subject[:20]}", 
                                    config['blockchain']['admin_addresses'][0]):
                return False
        
        # Randomize headers
        msg = f"Subject: {clean_input(subject)}\n"
        msg += f"X-Mailer: {random.choice(['Outlook', 'AppleMail', 'Thunderbird'])}\n"
        msg += f"Message-ID: <{random.getrandbits(128)}@example.com>\n\n"
        msg += clean_input(body)
        
        # Send with SMTP
        with smtplib.SMTP(config['mailer']['smtp_server'], config['mailer']['smtp_port']) as server:
            server.starttls()
            server.login(config['mailer']['smtp_user'], config['mailer']['smtp_pass'])
            server.sendmail(config['mailer']['smtp_user'], to, msg)
            
        random_delay()
        return True
    except Exception as e:
        print(f"📧 Email error: {str(e)}")
        return False

def send_sms(to, message):
    """Send SMS via Twilio"""
    try:
        client = Client(config['twilio']['account_sid'], config['twilio']['auth_token'])
        client.messages.create(
            body=clean_input(message),
            from_=config['twilio']['from_number'],
            to=to
        )
        random_delay()
        return True
    except Exception as e:
        print(f"📱 SMS error: {str(e)}")
        return False

def send_whatsapp(to, message):
    """Send WhatsApp message"""
    try:
        client = Client(config['twilio']['account_sid'], config['twilio']['auth_token'])
        client.messages.create(
            body=clean_input(message),
            from_='whatsapp:' + config['twilio']['whatsapp_number'],
            to='whatsapp:' + to
        )
        random_delay()
        return True
    except Exception as e:
        print(f"💬 WhatsApp error: {str(e)}")
        return False

def send_telegram(message, chat_id=None):
    """Send Telegram alert"""
    try:
        bot_token = config['telegram']['bot_token']
        chat_id = chat_id or config['telegram']['default_chat_id']
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': clean_input(message),
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload)
        random_delay()
        return response.json().get('ok', False)
    except Exception as e:
        print(f"📣 Telegram error: {str(e)}")
        return False

def send_voice_alert(message):
    """Send voice alert to Telegram"""
    try:
        from modules.voice_synthesis import clone_voice
        audio_url = clone_voice(message, config['ai']['voice_model'])
        
        if audio_url:
            bot_token = config['telegram']['bot_token']
            chat_id = config['telegram']['default_chat_id']
            url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
            
            # Download and send audio
            audio_data = requests.get(audio_url).content
            files = {'voice': ('alert.mp3', audio_data)}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
            return response.json().get('ok', False)
        return False
    except Exception as e:
        print(f"📢 Voice alert error: {str(e)}")
        return False