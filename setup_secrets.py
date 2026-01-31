#!/usr/bin/env python3
"""
Synova AI - Secure Secret Generator and Configuration Setup

This script will:
1. Generate secure random secrets
2. Create .env and .env.prod files
3. Update configuration files
4. Set secure file permissions
"""

import os
import secrets
import base64
import stat
from pathlib import Path
from typing import Dict, Any

# Configuration
CONFIG = {
    "project_name": "synova-ai",
    "project_dir": Path(__file__).parent.absolute(),
    "env_files": [
        ".env",
        ".env.prod"
    ],
    "template_files": [
        ".env.example",
        ".secrets.template"
    ]
}

def generate_secret_key(length: int = 32) -> str:
    """Generate a secure secret key."""
    return secrets.token_urlsafe(length)

def generate_fernet_key() -> str:
    """Generate a Fernet encryption key."""
    from cryptography.fernet import Fernet
    return base64.urlsafe_b64encode(Fernet.generate_key()).decode()

def generate_password(length: int = 32) -> str:
    """Generate a secure password."""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_files() -> Dict[str, Any]:
    """Create environment files with secure values."""
    # Generate all secrets
    secrets = {
        # Core
        "SECRET_KEY": generate_secret_key(),
        "FERNET_KEY": generate_fernet_key(),
        "JWT_SECRET": generate_secret_key(),
        
        # Database
        "DB_NAME": "synova_prod",
        "DB_USER": "synova_user",
        "DB_PASSWORD": generate_password(32),
        "DB_HOST": "db",
        "DB_PORT": "5432",
        
        # Redis
        "REDIS_PASSWORD": generate_password(32),
        "REDIS_HOST": "redis",
        "REDIS_PORT": "6379",
        
        # Security
        "JWT_ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "REFRESH_TOKEN_EXPIRE_DAYS": "7",
        
        # CORS
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:8000",
        
        # Security Headers
        "SECURE_HSTS_SECONDS": "31536000",
        "SECURE_SSL_REDIRECT": "True",
        "SESSION_COOKIE_SECURE": "True",
        "CSRF_COOKIE_SECURE": "True",
        
        # Environment
        "ENVIRONMENT": "production",
        "DEBUG": "False"
    }
    
    # Generate DATABASE_URL and REDIS_URL
    secrets["DATABASE_URL"] = f"postgresql://{secrets['DB_USER']}:{secrets['DB_PASSWORD']}@{secrets['DB_HOST']}:{secrets['DB_PORT']}/{secrets['DB_NAME']}"
    secrets["REDIS_URL"] = f"redis://:{secrets['REDIS_PASSWORD']}@{secrets['REDIS_HOST']}:{secrets['REDIS_PORT']}/0"
    
    return secrets

def write_env_file(secrets: Dict[str, Any], env_type: str = "development") -> None:
    """Write environment variables to a file."""
    if env_type == "production":
        filename = ".env.prod"
        secrets["ENVIRONMENT"] = "production"
        secrets["DEBUG"] = "False"
    else:
        filename = ".env"
        secrets["ENVIRONMENT"] = "development"
        secrets["DEBUG"] = "True"
    
    filepath = CONFIG["project_dir"] / filename
    
    # Create the .env file
    with open(filepath, 'w') as f:
        f.write(f"# {filename.upper()}\n")
        f.write(f"# Auto-generated - DO NOT COMMIT TO VERSION CONTROL\n\n")
        
        # Write core settings
        f.write("# Core Application Settings\n")
        f.write(f"SECRET_KEY={secrets['SECRET_KEY']}\n")
        f.write(f"FERNET_KEY={secrets['FERNET_KEY']}\n")
        f.write(f"JWT_SECRET={secrets['JWT_SECRET']}\n")
        f.write(f"ENVIRONMENT={secrets['ENVIRONMENT']}\n")
        f.write(f"DEBUG={secrets['DEBUG']}\n\n")
        
        # Database settings
        f.write("# Database Settings\n")
        f.write(f"DB_NAME={secrets['DB_NAME']}\n")
        f.write(f"DB_USER={secrets['DB_USER']}\n")
        f.write(f"DB_PASSWORD={secrets['DB_PASSWORD']}\n")
        f.write(f"DB_HOST={secrets['DB_HOST']}\n")
        f.write(f"DB_PORT={secrets['DB_PORT']}\n")
        f.write(f"DATABASE_URL={secrets['DATABASE_URL']}\n\n")
        
        # Redis settings
        f.write("# Redis Settings\n")
        f.write(f"REDIS_PASSWORD={secrets['REDIS_PASSWORD']}\n")
        f.write(f"REDIS_HOST={secrets['REDIS_HOST']}\n")
        f.write(f"REDIS_PORT={secrets['REDIS_PORT']}\n")
        f.write(f"REDIS_URL={secrets['REDIS_URL']}\n\n")
        
        # Security settings
        f.write("# Security Settings\n")
        f.write(f"JWT_ALGORITHM={secrets['JWT_ALGORITHM']}\n")
        f.write(f"ACCESS_TOKEN_EXPIRE_MINUTES={secrets['ACCESS_TOKEN_EXPIRE_MINUTES']}\n")
        f.write(f"REFRESH_TOKEN_EXPIRE_DAYS={secrets['REFRESH_TOKEN_EXPIRE_DAYS']}\n")
        f.write(f"CORS_ORIGINS={secrets['CORS_ORIGINS']}\n")
        f.write(f"SECURE_HSTS_SECONDS={secrets['SECURE_HSTS_SECONDS']}\n")
        f.write(f"SECURE_SSL_REDIRECT={secrets['SECURE_SSL_REDIRECT']}\n")
        f.write(f"SESSION_COOKIE_SECURE={secrets['SESSION_COOKIE_SECURE']}\n")
        f.write(f"CSRF_COOKIE_SECURE={secrets['CSRF_COOKIE_SECURE']}\n")
        
        # Add placeholders for optional settings
        f.write("\n# Optional Settings (Uncomment and configure as needed)\n")
        f.write("# OPENAI_API_KEY=your_openai_api_key_here\n")
        f.write("# SMTP_SERVER=smtp.example.com\n")
        f.write("# SMTP_PORT=587\n")
        f.write("# SMTP_USER=your_email@example.com\n")
        f.write("# SMTP_PASSWORD=your_email_password_here\n")
        f.write("# AWS_ACCESS_KEY_ID=your_aws_access_key\n")
        f.write("# AWS_SECRET_ACCESS_KEY=your_aws_secret_key\n")
        f.write("# AWS_STORAGE_BUCKET_NAME=your-bucket-name\n")
        f.write("# SENTRY_DSN=your_sentry_dsn_here\n")
    
    # Set secure file permissions (read/write for owner only)
    os.chmod(filepath, 0o600)
    print(f"Created {filename} with secure permissions")

def create_template_file() -> None:
    """Create a .env.example template file."""
    template = """# .env.example
# Copy this file to .env or .env.prod and fill in the values

# Core Application
SECRET_KEY=your_secret_key_here
FERNET_KEY=your_fernet_key_here
JWT_SECRET=your_jwt_secret_here
ENVIRONMENT=development
DEBUG=True

# Database
DB_NAME=synova_dev
DB_USER=postgres
DB_PASSWORD=your_db_password_here
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# Redis
REDIS_PASSWORD=your_redis_password_here
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}/0

# Security
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Security Headers
SECURE_HSTS_SECONDS=31536000
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Optional Settings (Uncomment and configure as needed)
# OPENAI_API_KEY=your_openai_api_key_here
# SMTP_SERVER=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=your_email@example.com
# SMTP_PASSWORD=your_email_password_here
# AWS_ACCESS_KEY_ID=your_aws_access_key
# AWS_SECRET_ACCESS_KEY=your_aws_secret_key
# AWS_STORAGE_BUCKET_NAME=your-bucket-name
# SENTRY_DSN=your_sentry_dsn_here
"""
    
    filepath = CONFIG["project_dir"] / ".env.example"
    with open(filepath, 'w') as f:
        f.write(template)
    
    print("Created .env.example template")

def update_gitignore() -> None:
    """Update .gitignore to exclude sensitive files."""
    gitignore_path = CONFIG["project_dir"] / ".gitignore"
    gitignore_content = """
# Environment files
.env
.env.*
!.env.example
.secrets.*
!.secrets.template

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv
venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Logs
*.log

# Local development
.docker/

# Docker
Dockerfile.local
docker-compose.override.yml
"""
    
    with open(gitignore_path, 'a') as f:
        f.write(gitignore_content)
    
    print("Updated .gitignore with security rules")

def main() -> None:
    """Main function to set up the environment."""
    print("🚀 Setting up Synova AI environment...\n")
    
    try:
        # Generate secrets
        print("🔑 Generating secure secrets...")
        secrets = create_env_files()
        
        # Create environment files
        print("📝 Creating environment files...")
        write_env_file(secrets, "development")
        write_env_file(secrets, "production")
        
        # Create template file
        print("📋 Creating template files...")
        create_template_file()
        
        # Update .gitignore
        print("🔒 Updating .gitignore...")
        update_gitignore()
        
        print("\n✅ Environment setup complete!")
        print("\n📋 Next steps:")
        print("1. Review the generated .env and .env.prod files")
        print("2. Add any additional environment-specific settings")
        print("3. Commit the .env.example and .gitignore files")
        print("4. DO NOT commit .env or .env.prod to version control")
        print("\n🔒 Your secrets have been generated with secure random values.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n⚠️  Please ensure you have the required dependencies installed:")
        print("   pip install cryptography")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
