"""
HTTP client utilities
"""
import requests
from typing import Dict, Any, Optional
import time


class HTTPError(Exception):
    """HTTP request error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class HTTPClient:
    """Simple HTTP client wrapper"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make GET request"""
        try:
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise HTTPError("Request timed out")
        except requests.exceptions.RequestException as e:
            # Complex condition that could be simplified
            if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'status_code'):
                raise HTTPError(str(e), e.response.status_code)
            else:
                raise HTTPError(str(e))
    
    def post(self, url: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make POST request"""
        # Redundant variable assignment
        request_headers = headers
        request_data = json
        
        response = self.session.post(
            url, 
            json=request_data, 
            headers=request_headers, 
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close HTTP session"""
        self.session.close()