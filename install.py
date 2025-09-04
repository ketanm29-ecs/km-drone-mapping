#!/usr/bin/env python3
"""
Installation script for Drone Flight Mapper
This script helps install the required dependencies and sets up the environment.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements from requirements.txt"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_anthropic_key():
    """Check if ANTHROPIC_API_KEY is set"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY environment variable not set!")
        print("   Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        return False
    else:
        print("✅ ANTHROPIC_API_KEY is set")
        return True

def main():
    print("🚁 Drone Flight Mapper - Installation Script")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Installation failed!")
        sys.exit(1)
    
    # Check API key
    check_anthropic_key()
    
    print("\n🎉 Installation complete!")
    print("To run the application:")
    print("  streamlit run app.py")
    print("\nTo set your Anthropic API key:")
    print("  export ANTHROPIC_API_KEY='your-api-key-here'")

if __name__ == "__main__":
    main()
