"""
Application Configuration Module
This module contains all configuration settings for the sample project.
"""

import os
from typing import Dict, Any, Optional

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'name': os.getenv('DB_NAME', 'sample_db'),
    'username': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'secret'),
    'pool_size': 10,
    'max_overflow': 20,
}

# API Configuration
API_CONFIG = {
    'host': os.getenv('API_HOST', 'localhost'),
    'port': int(os.getenv('API_PORT', '8080')),
    'version': 'v1',
    'timeout': 30,
    'retries': 3,
    'rate_limit': {
        'requests_per_minute': 60,
        'burst_limit': 10
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'handlers': ['console', 'file'],
    'file_path': '/var/log/sample_project.log'
}

# Feature Flags
FEATURE_FLAGS = {
    'enable_metrics': True,
    'enable_analytics': False,
    'enable_caching': True,
    'enable_rate_limiting': True,
    'debug_mode': os.getenv('DEBUG', 'false').lower() == 'true'
}

# Cache Configuration
CACHE_CONFIG = {
    'backend': 'redis',
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', '6379')),
    'db': 0,
    'ttl': 3600,
    'max_size': 1000
}


def get_config(section: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific section"""
    configs = {
        'database': DATABASE_CONFIG,
        'api': API_CONFIG,
        'logging': LOGGING_CONFIG,
        'features': FEATURE_FLAGS,
        'cache': CACHE_CONFIG
    }
    return configs.get(section)


def validate_config() -> bool:
    """Validate all configuration settings"""
    try:
        # Validate database config
        if not DATABASE_CONFIG['host'] or not DATABASE_CONFIG['name']:
            return False
            
        # Validate API config
        if not (1 <= API_CONFIG['port'] <= 65535):
            return False
            
        # Validate logging config
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if LOGGING_CONFIG['level'] not in valid_levels:
            return False
            
        return True
    except Exception:
        return False


# Global configuration instance
CONFIG = {
    'database': DATABASE_CONFIG,
    'api': API_CONFIG,
    'logging': LOGGING_CONFIG,
    'features': FEATURE_FLAGS,
    'cache': CACHE_CONFIG
}

# Export commonly used settings
DEBUG = FEATURE_FLAGS['debug_mode']
API_HOST = API_CONFIG['host']
API_PORT = API_CONFIG['port']
DB_NAME = DATABASE_CONFIG['name']