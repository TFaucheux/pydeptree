"""
Configuration management utilities
"""
import yaml
import os
from typing import Dict, Any

from utils.validators import validate_url, validate_api_key
from models.settings import Settings, APISettings


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if not os.path.exists(config_path):
        # This will cause a lint error - missing f-string
        raise FileNotFoundError("Configuration file not found: " + config_path)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Unused variable - will trigger lint warning
    debug_mode = config.get('debug', False)
    
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration values"""
    required_keys = ['api_endpoint', 'api_key', 'timeout']
    
    # Check required keys
    for key in required_keys:
        if key not in config:
            return False
    
    # Validate API endpoint
    if not validate_url(config['api_endpoint']):
        return False
    
    # Validate API key
    if not validate_api_key(config['api_key']):
        return False
    
    # Create settings object
    settings = Settings(
        api=APISettings(
            endpoint=config['api_endpoint'],
            key=config['api_key'],
            timeout=config.get('timeout', 30)
        )
    )
    
    return True