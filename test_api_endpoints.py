#!/usr/bin/env python3
"""
Test script to verify API endpoints are working
"""
import requests
import json

def test_search_api():
    """Test the /api/search endpoint"""
    url = "http://localhost:5000/api/search"
    data = {
        "query": "laptop",
        "budget": 50000,
        "max_results": 5
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Search API Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Search Success: {result.get('success', False)}")
            print(f"Results Count: {len(result.get('results', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Search API Error: {e}")

def test_ai_chat_api():
    """Test the /api/ai/chat endpoint"""
    url = "http://localhost:5000/api/ai/chat"
    data = {
        "message": "Find me a good laptop under 50000",
        "products": []
    }
    
    try:
        response = requests.post(url, json=data, timeout=15)
        print(f"AI Chat API Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"AI Chat Success: {result.get('success', False)}")
            print(f"Response: {result.get('response', '')[:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"AI Chat API Error: {e}")

def test_mobile_search_api():
    """Test the /api/mobile/search endpoint"""
    url = "http://localhost:5000/api/mobile/search"
    data = {
        "query": "iPhone 15 Pro Max",
        "price_min": 0,
        "price_max": 150000,
        "min_cpi": 0
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Mobile Search API Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Mobile Search Success: {result.get('success', False)}")
            print(f"Results Count: {result.get('total_results', 0)}")
            print(f"Live Search Suggestion: {result.get('live_search_suggestion', False)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Mobile Search API Error: {e}")

if __name__ == "__main__":
    print("Testing API Endpoints...")
    print("=" * 50)
    
    print("\n1. Testing Search API:")
    test_search_api()
    
    print("\n2. Testing AI Chat API:")
    test_ai_chat_api()
    
    print("\n3. Testing Mobile Search API:")
    test_mobile_search_api()
    
    print("\n" + "=" * 50)
    print("Test completed!")