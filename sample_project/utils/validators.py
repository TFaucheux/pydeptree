"""
Validation utilities for configuration and input data
"""
import re
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """Validate if string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    # API key should be alphanumeric and at least 32 characters
    if not api_key or len(api_key) < 32:
        return False
    
    # Check if alphanumeric with possible hyphens
    pattern = re.compile(r'^[a-zA-Z0-9\-]+$')
    return bool(pattern.match(api_key))


def validate_timeout(timeout: int) -> bool:
    """Validate timeout value"""
    return isinstance(timeout, int) and 1 <= timeout <= 300


# Type annotation error - missing import
def validate_email(email: str) -> Optional[str]:
    """Validate email format"""
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if pattern.match(email):
        return email.lower()
    return None