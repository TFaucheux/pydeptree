"""
Settings and configuration models
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class APISettings:
    """API configuration settings"""
    endpoint: str
    key: str
    timeout: int = 30
    retry_count: int = 3
    
    def __post_init__(self):
        # Long line that will trigger line length warning
        if not self.endpoint.startswith('http://') and not self.endpoint.startswith('https://'):
            self.endpoint = 'https://' + self.endpoint


@dataclass
class DatabaseSettings:
    """Database configuration settings"""
    host: str
    port: int
    username: str
    password: str
    database: str
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class Settings:
    """Application settings"""
    api: APISettings
    database: Optional[DatabaseSettings] = None
    debug: bool = False
    log_level: str = "INFO"
    
    def validate(self) -> bool:
        """Validate all settings"""
        # TODO: Implement validation logic
        return True