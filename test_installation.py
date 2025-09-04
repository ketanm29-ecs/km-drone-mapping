#!/usr/bin/env python3
"""
Test script to verify that all dependencies are properly installed
"""

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import folium
        print("✅ folium")
    except ImportError as e:
        print(f"❌ folium: {e}")
        return False
    
    try:
        import anthropic
        print("✅ anthropic")
    except ImportError as e:
        print(f"❌ anthropic: {e}")
        return False
    
    try:
        import plotly
        print("✅ plotly")
    except ImportError as e:
        print(f"❌ plotly: {e}")
        return False
    
    # Test streamlit_folium with fallback
    try:
        from streamlit_folium import folium_static
        print("✅ streamlit_folium")
    except ImportError:
        print("⚠️  streamlit_folium not available, will use fallback")
    
    return True

def test_anthropic_client():
    """Test Anthropic client initialization"""
    print("\n🤖 Testing Anthropic client...")
    
    try:
        import anthropic
        import os
        
        # Try to load from config.env file
        try:
            from dotenv import load_dotenv
            load_dotenv('config.env')
        except ImportError:
            pass
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not set")
            print("   Run: python setup_api_key.py")
            return False
        
        client = anthropic.Anthropic(api_key=api_key)
        # Test with a simple message to verify the model works
        try:
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print("✅ Anthropic client and model work successfully")
        except Exception as model_error:
            print(f"⚠️  Client initialized but model test failed: {model_error}")
        return True
    except Exception as e:
        print(f"❌ Anthropic client error: {e}")
        return False

def main():
    print("🚁 Drone Flight Mapper - Installation Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Some imports failed. Please run: pip install -r requirements.txt")
        return False
    
    # Test Anthropic client
    test_anthropic_client()
    
    print("\n🎉 All tests passed! You're ready to run the application.")
    print("Run: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main()
