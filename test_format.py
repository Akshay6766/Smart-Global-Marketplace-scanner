import requests
import json

# Test the improved AI formatting
url = 'http://localhost:5000/api/ai/chat'
data = {
    'message': 'I need a phone with great camera and battery under 30k',
    'context': {}
}

try:
    print('Testing improved AI formatting...')
    response = requests.post(url, json=data, timeout=15)
    result = response.json()
    
    if result.get('success'):
        ai_response = result.get('response', '')
        print('\n=== AI RESPONSE ===')
        print(ai_response)
        print('\n=== ANALYSIS ===')
        print(f'Length: {len(ai_response)} characters')
        print(f'Lines: {ai_response.count(chr(10)) + 1}')
        print(f'Ready to search: {result.get("ready_to_search")}')
    else:
        print(f'Error: {result.get("error")}')
        
except Exception as e:
    print(f'Request failed: {e}')