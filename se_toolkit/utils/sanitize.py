# Advanced Input Sanitization
# With AI-Powered Injection Detection

import re
import yaml
import openai
import logging

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(filename='sanitization.log', level=logging.WARNING)

def clean_input(input_str):
    """Sanitize user input to prevent injection attacks"""
    if not input_str:
        return ""
    
    # Truncate to max length
    sanitized = str(input_str)[:config['security']['max_input_length']]
    
    # Remove suspicious patterns
    injection_patterns = [
        r"<script.*?>.*?</script>",  # Script tags
        r"javascript:",              # JS protocol
        r"on\w+=\".*?\"",            # Event handlers
        r"\${.*?}",                  # Template injections
        r"\{\{.*?\}\}",              # Double braces
        r"\\u[0-9a-fA-F]{4}",        # Unicode escapes
        r"[\;\|\`]"                  # Command separators
    ]
    
    for pattern in injection_patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
    
    # Escape special characters
    sanitized = (sanitized.replace("'", "&apos;")
                 .replace('"', "&quot;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;"))
    
    return sanitized.strip()

def ai_detect_injection(input_str):
    """Use AI to detect sophisticated prompt injections"""
    # Basic pattern matching first
    if any(token in input_str.lower() for token in ["system", "prompt", "ignore", "override"]):
        return True
    
    # AI detection if API available
    if config['ai'].get('openai_key'):
        try:
            response = openai.Moderation.create(
                input=input_str,
                model="text-moderation-latest"
            )
            return response.results[0].flagged
        except Exception as e:
            logging.warning(f"AI detection failed: {str(e)}")
    
    return False