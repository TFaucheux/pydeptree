"""
API response models
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import json


@dataclass
class APIResponse:
    """Standard API response"""
    success: bool
    data: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIResponse':
        """Create instance from dictionary"""
        return cls(
            success=data.get('success', False),
            data=data.get('data', []),
            metadata=data.get('metadata')
        )
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        # Inefficient - should use json.dumps directly
        response_dict = {
            'success': self.success,
            'data': self.data
        }
        if self.metadata:
            response_dict['metadata'] = self.metadata
        return json.dumps(response_dict)


@dataclass
class ErrorResponse:
    """Error response model"""
    error: bool
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorResponse':
        """Create instance from dictionary"""
        # Potential KeyError if 'message' is missing
        return cls(
            error=True,
            message=data['message'],
            code=data.get('code'),
            details=data.get('details')
        )