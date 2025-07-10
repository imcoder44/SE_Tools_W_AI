# Advanced OSINT with AI Integration
# For authorized security research only

import requests
from bs4 import BeautifulSoup
import re
import json
import yaml
from utils.sanitize import clean_input
import time
import datetime

# Load configuration
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def gather_osint(identifier):
    """Gather comprehensive OSINT data for target"""
    # Determine if identifier is email, username, or domain
    if '@' in identifier:
        email = identifier
        username = email.split('@')[0]
        domain = email.split('@')[1]
    else:
        username = identifier
        domain = ""
        email = ""
    
    data = {
        'identifier': identifier,
        'type': 'email' if '@' in identifier else 'username',
        'email': email,
        'username': username,
        'domain': domain,
        'profiles': [],
        'social_links': [],
        'employment_history': [],
        'credentials_found': 0,
        'importance': 0  # 1-10 scale
    }
    
    try:
        # Step 1: Basic social media discovery
        print(f"🔍 Starting OSINT for {identifier}")
        social_platforms = {
            'twitter': f"https://twitter.com/{username}",
            'linkedin': f"https://linkedin.com/in/{username}",
            'github': f"https://github.com/{username}",
            'instagram': f"https://instagram.com/{username}",
            'facebook': f"https://facebook.com/{username}"
        }
        
        for platform, url in social_platforms.items():
            response = requests.head(url, headers=HEADERS, timeout=5)
            if response.status_code == 200:
                data['social_links'].append(url)
                data['profiles'].append({
                    'platform': platform,
                    'url': url,
                    'valid': True
                })
                data['importance'] += 1
        
        # Step 2: Domain-based intelligence
        if domain:
            # WHOIS data
            try:
                from modules.whois_tools import get_whois_data
                data['whois'] = get_whois_data(domain)
            except:
                pass
            
            # Company info
            try:
                hq_response = requests.get(f"https://api.domainsdb.info/v1/domains/search?domain={domain}", 
                                          headers=HEADERS)
                if hq_response.status_code == 200:
                    data['company_info'] = hq_response.json().get('domains', [{}])[0]
            except:
                pass
        
        # Step 3: Breach data (simulated)
        data['breaches'] = simulate_breach_check(email)
        
        # Step 4: Metadata analysis
        data['metadata'] = extract_metadata(identifier)
        
        # Calculate importance score
        data['importance'] = min(10, data['importance'])
        
        return data
    except Exception as e:
        print(f"OSINT error: {str(e)}")
        return data

def simulate_breach_check(email):
    """Simulate breach data check (replace with real API)"""
    # In a real implementation, use HaveIBeenPwned API
    breaches = []
    if "highvalue" in email:
        breaches.append({
            'name': 'Example Mega Breach 2023',
            'date': '2023-06-15',
            'data_classes': ['Emails', 'Passwords']
        })
        breaches.append({
            'name': 'Corporate Leak 2022',
            'date': '2022-11-03',
            'data_classes': ['Emails', 'Job Titles']
        })
    return breaches

def extract_metadata(identifier):
    """Extract metadata from OSINT sources"""
    metadata = {
        'creation_dates': [],
        'last_seen': datetime.datetime.utcnow().isoformat(),
        'associated_ips': [],
        'associated_domains': []
    }
    
    # Simulated data extraction
    if '@' in identifier:
        metadata['creation_dates'].append("2020-05-12")
        metadata['associated_ips'].append("192.168.1.1")
        metadata['associated_domains'].append("company.com")
    
    return metadata

def enrich_target(identifier):
    """Public interface for target enrichment"""
    return gather_osint(clean_input(identifier))