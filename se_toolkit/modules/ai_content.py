# AI-Driven Content Generation
# Ethical Use Only

import openai
import yaml
import random
import time
from utils.sanitize import clean_input, ai_detect_injection

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Set API key
openai.api_key = config['ai']['openai_key']

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 20
request_timestamps = []

def rate_limit():
    """Enforce rate limiting for API calls"""
    global request_timestamps
    
    # Remove old timestamps
    now = time.time()
    request_timestamps = [t for t in request_timestamps if t > now - 60]
    
    # Wait if rate limit reached
    if len(request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        sleep_time = 60 - (now - request_timestamps[0]) + 1
        time.sleep(sleep_time)
    
    request_timestamps.append(time.time())

def generate_phishing_content(target_info, content_type="email"):
    """Generate AI-powered phishing content"""
    try:
        # Rate limit check
        rate_limit()
        
        # Build context
        context = f"Target: {target_info.get('username', 'User')}"
        if 'email' in target_info:
            context += f" ({target_info['email']})"
        if 'company_info' in target_info:
            context += f", Company: {target_info['company_info'].get('organization', 'Unknown')}"
        
        # Define content templates
        templates = {
            "email": "Write a convincing phishing email about {theme} with this context: {context}",
            "sms": "Create an urgent SMS message about {theme} with this context: {context}",
            "social": "Draft a friendly social media DM offering a special deal about {theme} with context: {context}"
        }
        
        # Select theme based on target profile
        themes = [
            "security update", "account verification", "system maintenance",
            "bonus announcement", "policy change", "urgent action required"
        ]
        theme = random.choice(themes)
        
        # Generate content
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a cybersecurity expert creating ethical phishing content for penetration testing. "
                               "Generate realistic but harmless content that would be used in authorized security testing."
                },
                {
                    "role": "user", 
                    "content": templates[content_type].format(theme=theme, context=context)
                }
            ],
            max_tokens=config['ai'].get('max_tokens', 256),
            temperature=0.75
        )
        
        content = clean_input(response.choices[0].message.content)
        
        # Safety check
        if ai_detect_injection(content):
            content = f"Security Update: Your attention is required for account maintenance."
            
        return content
    except Exception as e:
        print(f"🤖 AI content error: {str(e)}")
        # Fallback templates
        return fallback_content(content_type)

def fallback_content(content_type):
    """Fallback content if AI fails"""
    fallbacks = {
        "email": [
            "Urgent: Your account requires immediate verification",
            "Security Alert: Suspicious activity detected on your account",
            "Action Required: Confirm your identity for security purposes"
        ],
        "sms": [
            "ALERT: Verify your account now - {link}",
            "URGENT: Security update required for your account",
            "ACTION NEEDED: Unusual login attempt detected"
        ],
        "social": [
            "Hi! We're offering a special security upgrade for your account",
            "Limited time offer: Enhance your account protection today",
            "Important security notice regarding your profile"
        ]
    }
    return random.choice(fallbacks.get(content_type, ["Important security update"]))

def generate_target_profile(osint_data):
    """Generate AI analysis of OSINT data"""
    try:
        rate_limit()
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity analyst. Analyze this OSINT data and provide a profile summary:"
                },
                {
                    "role": "user",
                    "content": json.dumps(osint_data, indent=2)
                }
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        return clean_input(response.choices[0].message.content)
    except:
        return "Analysis unavailable"

def analyze_threats(log_data):
    """AI-powered threat analysis of log data"""
    try:
        rate_limit()
        
        summary = f"Analyze these security events for threats: {json.dumps(log_data[-10:])}"
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a threat intelligence analyst. Identify potential threats:"
                },
                {
                    "role": "user",
                    "content": summary
                }
            ],
            max_tokens=400,
            temperature=0.4
        )
        
        return clean_input(response.choices[0].message.content)
    except:
        return "Threat analysis unavailable"