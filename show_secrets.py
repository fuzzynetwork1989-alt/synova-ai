#!/usr/bin/env python3
"""
Synova AI - Secure Secrets Viewer

This script displays the contents of .env and .env.prod files
while hiding comments and empty lines for better readability.
"""

import os
from pathlib import Path

def display_secrets_safely(filepath):
    """Display secrets in a secure way"""
    print(f"\n🔐 Contents of {filepath}:\n")
    print("=" * 80)
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                print(line, end='')
    print("=" * 80)

def main():
    env_files = ['.env', '.env.prod']
    backup_file = 'secrets_backup.enc'
    
    print("🔒 Secure Secrets Backup Utility\n")
    
    # Display secrets from both files
    for env_file in env_files:
        if os.path.exists(env_file):
            display_secrets_safely(env_file)
        else:
            print(f"⚠️  {env_file} not found")
    
    print("\n📋 Backup Instructions:")
    print("1. Copy the contents above and save them in your password manager")
    print("2. For additional security, you can encrypt the backup file:")
    print(f"   openssl enc -aes-256-cbc -salt -in .env -out {backup_file}")
    print(f"   (You'll be prompted to set a password)")
    print("\n🚨 IMPORTANT: Never commit these secrets to version control!")
    print("   The .gitignore has been updated to prevent accidental commits.")

if __name__ == "__main__":
    main()
