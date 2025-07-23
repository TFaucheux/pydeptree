#!/usr/bin/env python3
"""
Demo script to showcase PyDepTree advanced CLI features
Creates temporary sample files to ensure it works regardless of installation method.
"""
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import time
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60 + "\n")

def print_subheader(text):
    """Print a formatted subheader"""
    print(f"\n🔹 {text}")
    print("-" * 50)

def run_command(cmd, description):
    """Run a command and display it"""
    print(f"\n💻 {description}")
    print(f"   Command: {' '.join(cmd)}")
    print("-" * 60)
    time.sleep(1)  # Brief pause for readability
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def create_advanced_sample_project(temp_dir):
    """Create a more complex temporary sample project for advanced demonstration"""
    print_subheader("Creating advanced sample project...")
    
    # Create directory structure
    project_dir = temp_dir / "advanced_demo"
    project_dir.mkdir()
    
    # Create subdirectories
    for subdir in ["models", "services", "utils", "config", "tests"]:
        (project_dir / subdir).mkdir()
    
    # Create main.py with complexity
    main_py = project_dir / "main.py"
    main_py.write_text('''"""
Advanced application entry point with multiple features
TODO: Add proper error handling
FIXME: Optimize startup time
"""
import sys
from typing import Optional
from config.settings import load_config
from services.api_client import APIClient
from services.data_processor import DataProcessor
from models.user_profile import UserProfile
from utils.logger import setup_logging

def complex_startup_logic(config_path: Optional[str] = None) -> bool:
    """Complex startup with multiple branches - TODO: simplify this"""
    try:
        config = load_config(config_path)
        if not config:
            return False
        
        # Multiple nested conditions for complexity
        if config.get("debug_mode"):
            if config.get("verbose_logging"):
                setup_logging("DEBUG")
                if config.get("log_to_file"):
                    print("Logging to file enabled")
                    return True
                else:
                    print("Console logging only")
            else:
                setup_logging("INFO")
        else:
            setup_logging("ERROR")
        
        return True
    except Exception as e:
        print(f"Startup failed: {e}")
        return False

def main():
    """Main application function with high complexity"""
    if not complex_startup_logic():
        sys.exit(1)
    
    # Initialize services
    api_client = APIClient()
    processor = DataProcessor()
    
    # Multiple processing paths
    for user_id in range(1, 6):
        try:
            # Nested complexity
            if user_id % 2 == 0:
                if user_id > 2:
                    profile_data = api_client.fetch_user_profile(user_id)
                    if profile_data:
                        profile = UserProfile.from_dict(profile_data)
                        if profile.is_active:
                            result = processor.process_profile(profile)
                            print(f"Processed user {user_id}: {result}")
                        else:
                            print(f"User {user_id} is inactive")
                    else:
                        print(f"No data for user {user_id}")
                else:
                    print(f"Skipping user {user_id} (too low)")
            else:
                print(f"Skipping odd user {user_id}")
        except Exception as e:
            print(f"Error processing user {user_id}: {e}")
    
    return 0

if __name__ == "__main__":
    # HACK: Quick fix for testing
    sys.exit(main())
''')
    
    # Create config/settings.py with intentional lint issues
    config_dir = project_dir / "config"
    settings_py = config_dir / "settings.py"
    settings_py.write_text('''"""
Configuration management module
TODO: Add environment variable support
"""
import os
import json
from typing import Dict, Any, Optional

# Intentional lint issues for demonstration
unused_variable = "this will trigger a warning"

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or defaults"""
    default_config = {
        "debug_mode": True,
        "verbose_logging": False,
        "log_to_file": True,
        "api_timeout": 30,
        "max_retries": 3
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                default_config.update(file_config)
        except Exception as e:
            print(f"Config load error: {e}")
    
    return default_config

class ConfigManager:
    """Manages application configuration - TODO: implement caching"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self._config = None
    
    def get_config(self):
        """Get configuration dict"""
        if not self._config:
            self._config = load_config(self.config_path)
        return self._config
    
    def reload_config(self):
        """Reload configuration - FIXME: add validation"""
        self._config = None
        return self.get_config()
''')
    
    # Create models with complex inheritance
    models_dir = project_dir / "models"
    user_profile_py = models_dir / "user_profile.py"
    user_profile_py.write_text('''"""
User profile models with inheritance and complexity
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.validators import validate_email, validate_phone

class BaseProfile:
    """Base profile class with common functionality"""
    
    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = validate_email(email)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update_timestamp(self):
        """Update the modification timestamp"""
        self.updated_at = datetime.now()

class UserProfile(BaseProfile):
    """User profile with personal information - TODO: add privacy controls"""
    
    def __init__(self, user_id: int, email: str, name: str = ""):
        super().__init__(user_id, email)
        self.name = name
        self.phone = None
        self.preferences = {}
        self.is_active = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create profile from dictionary data"""
        profile = cls(
            user_id=data["user_id"],
            email=data["email"],
            name=data.get("name", "")
        )
        
        if "phone" in data:
            profile.set_phone(data["phone"])
        
        if "preferences" in data:
            profile.preferences.update(data["preferences"])
        
        profile.is_active = data.get("is_active", True)
        return profile
    
    def set_phone(self, phone: str) -> bool:
        """Set and validate phone number - FIXME: better validation needed"""
        if validate_phone(phone):
            self.phone = phone
            self.update_timestamp()
            return True
        return False
    
    def deactivate(self):
        """Deactivate user profile"""
        self.is_active = False
        self.update_timestamp()

class PremiumProfile(UserProfile):
    """Premium user profile with additional features"""
    
    def __init__(self, user_id: int, email: str, name: str = ""):
        super().__init__(user_id, email, name)
        self.subscription_tier = "premium"
        self.feature_flags = []
    
    def add_feature(self, feature: str):
        """Add premium feature to profile"""
        if feature not in self.feature_flags:
            self.feature_flags.append(feature)
            self.update_timestamp()
''')
    
    # Create services with high complexity
    services_dir = project_dir / "services"
    api_client_py = services_dir / "api_client.py"
    api_client_py.write_text('''"""
API client service with complex retry logic
NOTE: This module has intentionally complex functions for demo purposes
"""
import time
import random
from typing import Optional, Dict, Any
from config.settings import load_config

class APIClient:
    """API client with retry logic and error handling"""
    
    def __init__(self):
        self.config = load_config()
        self.timeout = self.config.get("api_timeout", 30)
        self.max_retries = self.config.get("max_retries", 3)
        self.base_url = "https://api.example.com"
    
    def fetch_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Fetch user profile with complex retry logic - OPTIMIZE: reduce complexity"""
        retry_count = 0
        
        while retry_count < self.max_retries:
            try:
                # Simulate network conditions
                if random.random() < 0.3:  # 30% chance of failure
                    if retry_count < 2:
                        if random.random() < 0.5:
                            raise ConnectionError("Network timeout")
                        else:
                            raise ValueError("Invalid response")
                    else:
                        # Final retry always succeeds for demo
                        pass
                
                # Simulate successful response
                profile_data = {
                    "user_id": user_id,
                    "email": f"user{user_id}@example.com",
                    "name": f"User {user_id}",
                    "is_active": user_id % 3 != 0,  # Some inactive users
                    "preferences": {
                        "theme": "dark" if user_id % 2 == 0 else "light",
                        "notifications": True
                    }
                }
                
                return profile_data
                
            except (ConnectionError, ValueError) as e:
                retry_count += 1
                if retry_count >= self.max_retries:
                    print(f"API call failed after {self.max_retries} retries: {e}")
                    return None
                
                # Exponential backoff
                wait_time = (2 ** retry_count) * 0.1
                time.sleep(wait_time)
                print(f"Retry {retry_count} after {wait_time}s...")
        
        return None
    
    def health_check(self) -> bool:
        """Check API health - TODO: implement proper health endpoint"""
        # Simple simulation
        return random.random() > 0.1  # 90% success rate
''')
    
    data_processor_py = services_dir / "data_processor.py"
    data_processor_py.write_text('''"""
Data processing service with complex algorithms
BUG: Memory leak in batch processing mode
"""
from typing import List, Dict, Any
from models.user_profile import UserProfile, PremiumProfile

class DataProcessor:
    """Processes user data with complex business logic"""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.cache = {}
    
    def process_profile(self, profile: UserProfile) -> Dict[str, Any]:
        """Process a user profile with complex validation - HACK: needs refactoring"""
        result = {"user_id": profile.user_id, "status": "unknown"}
        
        try:
            # Complex validation chain
            if self._validate_basic_info(profile):
                if self._validate_preferences(profile):
                    if self._validate_activity_status(profile):
                        if isinstance(profile, PremiumProfile):
                            result = self._process_premium_profile(profile)
                        else:
                            result = self._process_standard_profile(profile)
                        
                        self.processed_count += 1
                        result["status"] = "success"
                    else:
                        result["status"] = "inactive"
                        result["reason"] = "User is not active"
                else:
                    result["status"] = "invalid_preferences"
            else:
                result["status"] = "invalid_basic_info"
                
        except Exception as e:
            self.error_count += 1
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _validate_basic_info(self, profile: UserProfile) -> bool:
        """Validate basic profile information"""
        if not profile.email or "@" not in profile.email:
            return False
        
        if profile.user_id <= 0:
            return False
        
        return True
    
    def _validate_preferences(self, profile: UserProfile) -> bool:
        """Validate user preferences - FIXME: add proper schema validation"""
        if not isinstance(profile.preferences, dict):
            return False
        
        # Complex preference validation
        valid_themes = ["light", "dark", "auto"]
        if "theme" in profile.preferences:
            if profile.preferences["theme"] not in valid_themes:
                return False
        
        return True
    
    def _validate_activity_status(self, profile: UserProfile) -> bool:
        """Check if user is active and eligible for processing"""
        return profile.is_active
    
    def _process_standard_profile(self, profile: UserProfile) -> Dict[str, Any]:
        """Process standard user profile"""
        return {
            "user_id": profile.user_id,
            "type": "standard",
            "features_enabled": ["basic_features"],
            "processing_time": 0.1
        }
    
    def _process_premium_profile(self, profile: PremiumProfile) -> Dict[str, Any]:
        """Process premium user profile with extra features"""
        return {
            "user_id": profile.user_id,
            "type": "premium",
            "features_enabled": ["basic_features", "premium_features"] + profile.feature_flags,
            "processing_time": 0.2
        }
''')
    
    # Create utils with various complexity levels
    utils_dir = project_dir / "utils"
    validators_py = utils_dir / "validators.py"
    validators_py.write_text('''"""
Validation utilities with intentional complexity
"""
import re
from typing import Optional

def validate_email(email: str) -> str:
    """Validate email with complex regex - OPTIMIZE: use standard library"""
    if not email:
        raise ValueError("Email cannot be empty")
    
    # Overly complex email validation for demo purposes
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        if "@" not in email:
            if "." not in email:
                raise ValueError("Email must contain @ and .")
            else:
                raise ValueError("Email must contain @")
        else:
            if "." not in email.split("@")[1]:
                raise ValueError("Email domain must contain .")
            else:
                raise ValueError("Invalid email format")
    
    return email.lower()

def validate_phone(phone: str) -> bool:
    """Validate phone number - TODO: support international formats"""
    if not phone:
        return False
    
    # Remove common formatting
    cleaned = re.sub(r'[()-\s]', '', phone)
    
    # Complex validation chain
    if len(cleaned) < 10:
        return False
    elif len(cleaned) > 15:
        return False
    else:
        if cleaned.isdigit():
            return True
        elif cleaned.startswith('+') and cleaned[1:].isdigit():
            return True
        else:
            return False

def sanitize_input(input_str: str) -> str:
    """Sanitize user input - HACK: quick fix for XSS"""
    if not input_str:
        return ""
    
    # Multiple sanitization steps
    sanitized = input_str.strip()
    
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        if char in sanitized:
            sanitized = sanitized.replace(char, '')
    
    return sanitized
''')
    
    logger_py = utils_dir / "logger.py"
    logger_py.write_text('''"""
Logging utilities
"""
import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup application logging with complex configuration"""
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    logging.info(f"Logging initialized at {level} level")

def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance"""
    return logging.getLogger(name)
''')
    
    # Create test files
    tests_dir = project_dir / "tests"
    test_user_py = tests_dir / "test_user_profile.py"
    test_user_py.write_text('''"""
Test cases for user profile functionality
"""
import pytest
from models.user_profile import UserProfile, PremiumProfile

def test_user_profile_creation():
    """Test basic user profile creation"""
    profile = UserProfile(1, "test@example.com", "Test User")
    assert profile.user_id == 1
    assert profile.email == "test@example.com"
    assert profile.name == "Test User"
    assert profile.is_active is True

def test_premium_profile_features():
    """Test premium profile specific features"""
    profile = PremiumProfile(2, "premium@example.com", "Premium User")
    profile.add_feature("advanced_analytics")
    
    assert profile.subscription_tier == "premium"
    assert "advanced_analytics" in profile.feature_flags

class TestProfileValidation:
    """Test profile validation methods"""
    
    def test_email_validation(self):
        """Test email validation in profile creation"""
        # This would normally use a proper validation library
        profile = UserProfile(1, "valid@example.com")
        assert "@" in profile.email
    
    def test_profile_deactivation(self):
        """Test profile deactivation functionality"""
        profile = UserProfile(1, "test@example.com")
        profile.deactivate()
        assert profile.is_active is False
''')
    
    # Create __init__.py files
    for subdir in ["models", "services", "utils", "config", "tests"]:
        (project_dir / subdir / "__init__.py").write_text(f'"""{subdir.title()} package"""')
    
    print(f"✅ Created advanced sample project at: {project_dir}")
    print(f"   📁 Complex structure with intentional issues for demonstration:")
    print(f"   ├── main.py (high complexity)")
    print(f"   ├── config/settings.py (config file with TODOs)")
    print(f"   ├── models/user_profile.py (inheritance hierarchy)")
    print(f"   ├── services/ (complex business logic)")
    print(f"   ├── utils/ (various utility functions)")
    print(f"   └── tests/ (test files)")
    
    return project_dir

def main():
    """Run demo of PyDepTree advanced features"""
    print_header("PyDepTree Advanced CLI Demo")
    print("This demo showcases the advanced features including:")
    print("• File type detection and color coding")
    print("• Complexity analysis and metrics")
    print("• TODO/FIXME comment detection")
    print("• Search and grep functionality") 
    print("• Lint checking integration")
    print("• Statistics and summary tables")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create advanced sample project
        project_dir = create_advanced_sample_project(temp_path)
        main_file = project_dir / "main.py"
        
        # Change to project directory for relative imports
        original_cwd = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Demo 1: Basic advanced analysis
            print_header("Demo 1: Advanced Dependency Analysis")
            run_command(
                ["pydeptree-advanced", str(main_file), "--depth", "2"],
                "Full advanced analysis with file types, metrics, and lint checking"
            )
            
            # Demo 2: Search functionality
            print_header("Demo 2: Search and Grep Features")
            run_command(
                ["pydeptree-advanced", str(main_file), "--search", "TODO", "--depth", "2"],
                "Search for TODO comments across the codebase"
            )
            
            # Demo 3: Class search
            print_header("Demo 3: Class Search")
            run_command(
                ["pydeptree-advanced", str(main_file), "--search", "UserProfile", "--search-type", "class"],
                "Search for specific class definitions"
            )
            
            # Demo 4: Complexity focus
            print_header("Demo 4: Complexity Analysis")
            run_command(
                ["pydeptree-advanced", str(main_file), "--depth", "3", "--show-metrics"],
                "Detailed complexity metrics and code structure analysis"
            )
            
            # Demo 5: Inline import display
            print_header("Demo 5: Inline Import Display")
            run_command(
                ["pydeptree-advanced", str(main_file), "--show-code", "inline", "--depth", "2"],
                "Show import statements directly in the dependency tree"
            )
            
            # Demo 6: Config file detection
            print_header("Demo 6: Config File Detection")
            config_file = project_dir / "config" / "settings.py"
            run_command(
                ["pydeptree-advanced", str(config_file), "--depth", "1"],
                "Analyze configuration file with config type detection"
            )
            
            # Demo 7: Statistics focus
            print_header("Demo 7: Statistics and Summary")
            run_command(
                ["pydeptree-advanced", str(main_file), "--show-stats", "--depth", "2"],
                "Comprehensive statistics and summary tables"
            )
            
            # Demo 8: Function search
            print_header("Demo 8: Function Search")
            run_command(
                ["pydeptree-advanced", str(main_file), "--search", "validate", "--search-type", "function"],
                "Search for functions containing 'validate'"
            )
            
        finally:
            # Restore original directory
            os.chdir(original_cwd)
    
    print_header("Advanced Demo Complete!")
    print("✅ All advanced PyDepTree features demonstrated successfully!")
    print("\n📖 Advanced Features Shown:")
    print("   • 🎨 Color-coded file types (Models, Services, Utils, Config, Tests, Main)")
    print("   • 📐 Complexity analysis with visual indicators")
    print("   • 🔍 Search and grep functionality (text, class, function, import)")
    print("   • 📌 TODO/FIXME/HACK comment detection")
    print("   • 📊 Comprehensive statistics and metrics")
    print("   • 🔧 Lint checking integration")
    print("   • 📍 Flexible import display options")
    print("   • ⚙️ Configuration file detection")
    print("\n🚀 Try these advanced features on your projects:")
    print("   pydeptree-advanced your_file.py --search 'TODO' --depth 3")
    print("   pydeptree-advanced your_file.py --show-code inline --show-metrics")
    print("   pydeptree-advanced your_file.py --search 'MyClass' --search-type class")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())