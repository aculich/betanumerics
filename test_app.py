#!/usr/bin/env python3
"""
Simple test script for the Betanumerics application
"""

import requests
import json
import time

def test_local_app():
    """Test the local Flask application"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Betanumerics Application")
    print("=" * 40)
    
    # Test 1: Check if app is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Application is running")
        else:
            print(f"❌ Application returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application. Is it running?")
        return False
    
    # Test 2: Generate a normal identifier
    print("\n📝 Testing normal identifier generation...")
    data = {
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{base_url}/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generated identifier: {result['identifier']}")
            print(f"✅ Generated URL: {result['url']}")
            print(f"✅ Easter egg: {result['easter_egg']}")
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return False
    
    # Test 3: Test the easter egg
    print("\n🐌 Testing easter egg (slug)...")
    data = {
        "email": "slug"
    }
    
    try:
        response = requests.post(f"{base_url}/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            if result['easter_egg']:
                print("✅ Easter egg triggered successfully!")
                print(f"✅ Message: {result['message']}")
            else:
                print("❌ Easter egg not triggered")
                return False
        else:
            print(f"❌ Easter egg test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during easter egg test: {e}")
        return False
    
    # Test 4: Test API endpoint
    print("\n🔌 Testing API endpoint...")
    data = {
        "email": "api@example.com"
    }
    
    try:
        response = requests.post(f"{base_url}/api/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API generated identifier: {result['identifier']}")
        else:
            print(f"❌ API test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during API test: {e}")
        return False
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    print("Starting tests in 3 seconds...")
    time.sleep(3)
    
    success = test_local_app()
    
    if success:
        print("\n✨ Application is working correctly!")
    else:
        print("\n💥 Some tests failed. Check the application.") 