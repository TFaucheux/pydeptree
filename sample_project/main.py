#!/usr/bin/env python3
"""
Main application entry point
"""
from utils.config import load_config, validate_config
from services.api import APIClient, APIError


def main():
    """Main application logic"""
    # Load and validate configuration
    config = load_config("config.yaml")
    if not validate_config(config):
        raise ValueError("Invalid configuration")
    
    # Initialize API client
    client = APIClient(config["api_endpoint"], config["api_key"])
    
    try:
        # Make API call
        response = client.get_data("/users")
        print(f"Retrieved {len(response)} users")
    except APIError as e:
        print(f"API Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())