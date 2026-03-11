#!/usr/bin/env python3
"""
Test script to check AI integration locally
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from bedrock_ai_assistant import BedrockShoppingAssistant
    
    print("="*60)
    print("TESTING AI INTEGRATION LOCALLY")
    print("="*60)
    
    # Test with Mistral Small (current default)
    print("\n1. Testing Mistral Small (current default)...")
    assistant = BedrockShoppingAssistant(region='us-east-1', model='mistral-small')
    
    if assistant.bedrock:
        print("✓ Bedrock client initialized successfully")
        
        # Test a simple chat
        print("\n2. Testing chat functionality...")
        result = assistant.chat("Hello, I need help finding a phone")
        
        print(f"Response: {result['response'][:100]}...")
        print(f"Error in response: {'error' in result['response'].lower()}")
        
        if 'error' in result['response'].lower() or 'access denied' in result['response'].lower():
            print("\n❌ Mistral Small has access issues")
            
            # Try Claude Haiku as fallback
            print("\n3. Testing Claude Haiku as fallback...")
            assistant2 = BedrockShoppingAssistant(region='us-east-1', model='claude-haiku')
            
            if assistant2.bedrock:
                result2 = assistant2.chat("Hello, I need help finding a phone")
                print(f"Claude Response: {result2['response'][:100]}...")
                
                if 'error' not in result2['response'].lower():
                    print("✓ Claude Haiku works! Recommend switching default.")
                else:
                    print("❌ Claude Haiku also has issues")
            else:
                print("❌ Claude Haiku client failed to initialize")
        else:
            print("✓ Mistral Small is working correctly")
    else:
        print("❌ Bedrock client failed to initialize")
        print("Check AWS credentials and region settings")
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS:")
    
    # Check available models
    models = BedrockShoppingAssistant.get_available_models()
    print("\nAvailable models:")
    for key, desc in models.items():
        print(f"  - {key}: {desc}")
    
    print("\nNext steps:")
    print("1. Check AWS Bedrock Console → Model access")
    print("2. Ensure Mistral Small is enabled")
    print("3. If not available, enable Claude Haiku")
    print("4. Update web_app.py default model if needed")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()