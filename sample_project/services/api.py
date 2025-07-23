"""
API client service
"""
import json
from typing import Dict, Any, List
import logging

from utils.http import HTTPClient, HTTPError
from models.response import APIResponse, ErrorResponse


logger = logging.getLogger(__name__)


class APIError(Exception):
    """Custom API exception"""
    pass


class APIClient:
    """API client for external service communication"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = HTTPClient()
        
    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare request headers"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def get_data(self, endpoint: str) -> List[Dict[str, Any]]:
        """Get data from API endpoint"""
        try:
            response = self.http_client.get(
                f"{self.base_url}{endpoint}",
                headers=self._prepare_headers()
            )
            
            # Parse response
            api_response = APIResponse.from_dict(response)
            
            if api_response.success:
                return api_response.data
            else:
                error_response = ErrorResponse.from_dict(response)
                raise APIError(f"API error: {error_response.message}")
                
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise APIError(f"Failed to fetch data: {str(e)}")
        except json.JSONDecodeError:
            # Missing exception handling - potential bug
            raise APIError("Invalid JSON response")
    
    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post data to API endpoint"""
        # Inefficient string concatenation
        url = self.base_url + endpoint
        
        response = self.http_client.post(
            url,
            json=data,
            headers=self._prepare_headers()
        )
        
        return response