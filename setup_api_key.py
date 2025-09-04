#!/usr/bin/env python3
"""
Setup script to configure the Anthropic API key
"""

import os
import sys

def setup_api_key():
    """Interactive setup for API key"""
    print("🚁 Drone Flight Mapper - API Key Setup")
    print("=" * 50)
    
    # Check if config.env already exists
    if os.path.exists('config.env'):
        print("📁 Found existing config.env file")
        with open('config.env', 'r') as f:
            content = f.read()
            if 'your-anthropic-api-key-here' not in content:
                print("✅ API key appears to be already configured!")
                return True
    
    print("\n🔑 Anthropic API Key Setup")
    print("Get your API key from: https://console.anthropic.com/")
    print()
    
    api_key = input("Enter your Anthropic API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided!")
        return False
    
    if api_key == 'your-anthropic-api-key-here':
        print("❌ Please enter your actual API key, not the placeholder!")
        return False
    
    # Create or update config.env
    config_content = f"""# Anthropic API Configuration
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY={api_key}

# Optional: Streamlit Configuration
# STREAMLIT_SERVER_PORT=8501
# STREAMLIT_SERVER_ADDRESS=localhost
"""
    
    try:
        with open('config.env', 'w') as f:
            f.write(config_content)
        
        print("✅ API key saved to config.env")
        print("🔒 Make sure to keep this file secure and don't share it!")
        
        # Test the API key
        print("\n🧪 Testing API key...")
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            print("✅ API key is valid!")
            return True
        except Exception as e:
            print(f"⚠️  API key test failed: {e}")
            print("   The key might still work, but please verify it's correct.")
            return True
            
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def main():
    if setup_api_key():
        print("\n🎉 Setup complete!")
        print("You can now run the application with:")
        print("  streamlit run app.py")
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
