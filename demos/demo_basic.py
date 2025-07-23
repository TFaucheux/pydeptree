#!/usr/bin/env python3
"""
Demo script to showcase PyDepTree basic CLI features
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

def create_sample_project(temp_dir):
    """Create a temporary sample project for demonstration"""
    print_subheader("Creating temporary sample project...")
    
    # Create directory structure
    project_dir = temp_dir / "demo_project"
    project_dir.mkdir()
    
    models_dir = project_dir / "models"
    models_dir.mkdir()
    
    services_dir = project_dir / "services"
    services_dir.mkdir()
    
    utils_dir = project_dir / "utils"
    utils_dir.mkdir()
    
    # Create main.py
    main_py = project_dir / "main.py"
    main_py.write_text('''"""
Main application entry point
"""
from services.user_service import UserService
from models.user import User

def main():
    """Main application function"""
    service = UserService()
    user = User("demo_user")
    result = service.process_user(user)
    print(f"Processing result: {result}")
    return result

if __name__ == "__main__":
    main()
''')
    
    # Create models/user.py
    user_model = models_dir / "user.py"
    user_model.write_text('''"""
User model definition
"""
from typing import Optional
from utils.validators import validate_username

class User:
    """User model class"""
    
    def __init__(self, username: str, email: Optional[str] = None):
        self.username = validate_username(username)
        self.email = email
        self.active = True
    
    def __str__(self):
        return f"User({self.username})"
    
    def deactivate(self):
        """Deactivate the user"""
        self.active = False

class AdminUser(User):
    """Admin user with elevated privileges"""
    
    def __init__(self, username: str, email: Optional[str] = None):
        super().__init__(username, email)
        self.is_admin = True
''')
    
    # Create models/__init__.py
    (models_dir / "__init__.py").write_text('"""Models package"""')
    
    # Create services/user_service.py
    user_service = services_dir / "user_service.py"
    user_service.write_text('''"""
User service for business logic
"""
from models.user import User, AdminUser
from utils.database import save_user

class UserService:
    """Service for user operations"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_user(self, user: User) -> bool:
        """Process a user through the system"""
        if not user.active:
            return False
            
        # Save to database
        result = save_user(user)
        if result:
            self.processed_count += 1
            
        return result
    
    def create_admin(self, username: str) -> AdminUser:
        """Create a new admin user"""
        admin = AdminUser(username)
        self.process_user(admin)
        return admin
''')
    
    # Create services/__init__.py
    (services_dir / "__init__.py").write_text('"""Services package"""')
    
    # Create utils/validators.py
    validators = utils_dir / "validators.py"
    validators.write_text('''"""
Validation utilities
"""
import re

def validate_username(username: str) -> str:
    """Validate and return username"""
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    
    return username.lower()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
''')
    
    # Create utils/database.py
    database = utils_dir / "database.py"
    database.write_text('''"""
Database utilities
"""
from models.user import User

# Simple in-memory storage for demo
user_storage = {}

def save_user(user: User) -> bool:
    """Save user to storage"""
    try:
        user_storage[user.username] = user
        return True
    except Exception:
        return False

def get_user(username: str) -> User:
    """Get user from storage"""
    return user_storage.get(username)

def list_users() -> list:
    """List all stored users"""
    return list(user_storage.values())
''')
    
    # Create utils/__init__.py
    (utils_dir / "__init__.py").write_text('"""Utils package"""')
    
    print(f"✅ Created sample project at: {project_dir}")
    print(f"   📁 Structure:")
    print(f"   ├── main.py")
    print(f"   ├── models/")
    print(f"   │   ├── __init__.py")
    print(f"   │   └── user.py")
    print(f"   ├── services/")
    print(f"   │   ├── __init__.py")
    print(f"   │   └── user_service.py")
    print(f"   └── utils/")
    print(f"       ├── __init__.py")
    print(f"       ├── validators.py")
    print(f"       └── database.py")
    
    return project_dir

def main():
    """Run demo of PyDepTree basic features"""
    print_header("PyDepTree Basic CLI Demo")
    print("This demo showcases the core dependency analysis features")
    print("of PyDepTree using a temporary sample project.")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create sample project
        project_dir = create_sample_project(temp_path)
        main_file = project_dir / "main.py"
        
        # Change to project directory for relative imports
        original_cwd = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Demo 1: Basic dependency tree
            print_header("Demo 1: Basic Dependency Tree")
            run_command(
                ["pydeptree", str(main_file)],
                "Basic dependency analysis of main.py"
            )
            
            # Demo 2: Dependency tree with depth limit
            print_header("Demo 2: Limited Depth Analysis")
            run_command(
                ["pydeptree", str(main_file), "--depth", "1"],
                "Dependency analysis with depth=1 (direct dependencies only)"
            )
            
            # Demo 3: Show import statements
            print_header("Demo 3: Import Statement Preview")
            run_command(
                ["pydeptree", str(main_file), "--show-code"],
                "Show actual import statements alongside dependency tree"
            )
            
            # Demo 4: Analyze specific file
            print_header("Demo 4: Analyze Specific Module")
            user_service = project_dir / "services" / "user_service.py"
            run_command(
                ["pydeptree", str(user_service), "--depth", "2"],
                "Analyze user_service.py dependencies"
            )
            
            # Demo 5: Different entry points
            print_header("Demo 5: Different Starting Points")
            user_model = project_dir / "models" / "user.py"
            run_command(
                ["pydeptree", str(user_model)],
                "Analyze user.py model dependencies"
            )
            
        finally:
            # Restore original directory
            os.chdir(original_cwd)
    
    print_header("Demo Complete!")
    print("✅ All basic PyDepTree features demonstrated successfully!")
    print("\n📖 Key Features Shown:")
    print("   • Dependency tree visualization")
    print("   • Configurable analysis depth")
    print("   • Import statement preview")
    print("   • Multiple entry points")
    print("   • Clean, readable output")
    print("\n🚀 Try PyDepTree on your own projects:")
    print("   pydeptree your_file.py --depth 3 --show-code")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())