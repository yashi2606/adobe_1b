import re

def is_valid_section(text):
    if not text:
        return False
        
    # Too short or too long
    if len(text.split()) < 3 or len(text.split()) > 20:
        return False
        
    # Contains numbers only
    if re.match(r'^[\d\s\-–]+$', text):
        return False
        
    # Page number or footer/header
    if re.match(r'^(page|pg|p\.?)\s*\d+', text.lower()):
        return False
        
    return True

def clean_text(text):
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove special characters at start/end
    text = text.strip('*•-–· ')
    
    return text
