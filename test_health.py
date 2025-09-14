#!/usr/bin/env python3
"""
Test script to verify health check endpoints
"""
import requests
import sys

def test_health_endpoints():
    base_url = "http://localhost:8005"  # Adjust port as needed
    
    endpoints = [
        "/health/",
        "/health/ready/",
        "/health/live/"
    ]
    
    print("Testing health check endpoints...")
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.status_code} - {response.json()}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: Connection failed - {e}")
    
    print("\nHealth check test completed!")

if __name__ == "__main__":
    test_health_endpoints()
