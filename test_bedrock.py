"""
Test Bedrock AI Integration
Run this to verify Bedrock is working
"""

print("\n" + "="*80)
print("TESTING BEDROCK AI INTEGRATION")
print("="*80)

# Test 1: Import
print("\n1. Testing import...")
try:
    from bedrock_ai_assistant import BedrockShoppingAssistant
    print("   ✓ Import successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    exit(1)

# Test 2: Initialize
print("\n2. Testing initialization...")
try:
    ai = BedrockShoppingAssistant(region='us-east-1', model='claude-haiku')
    if ai.bedrock:
        print("   ✓ Bedrock client initialized")
    else:
        print("   ✗ Bedrock client is None")
        print("\n   Setup required:")
        print("   1. Configure AWS credentials: aws configure")
        print("   2. Go to AWS Console → Bedrock → Model access")
        print("   3. Enable 'Claude 3 Haiku'")
        exit(1)
except Exception as e:
    print(f"   ✗ Initialization failed: {e}")
    print("\n   Possible issues:")
    print("   - AWS credentials not configured")
    print("   - boto3 not installed (run: pip install boto3)")
    exit(1)

# Test 3: Chat
print("\n3. Testing chat...")
try:
    result = ai.chat("I need a phone under 25000")
    if result.get('response'):
        print("   ✓ Chat working!")
        print(f"\n   AI Response:\n   {result['response'][:200]}...")
    else:
        print(f"   ✗ No response: {result}")
except Exception as e:
    error_str = str(e)
    if 'AccessDeniedException' in error_str:
        print("   ✗ Access denied - Claude not enabled")
        print("\n   Enable Claude:")
        print("   1. Go to: https://console.aws.amazon.com/bedrock")
        print("   2. Click 'Model access' → 'Manage model access'")
        print("   3. Check 'Claude 3 Haiku'")
        print("   4. Click 'Save changes'")
        print("   5. Wait 2-3 minutes")
    else:
        print(f"   ✗ Chat failed: {e}")
    exit(1)

# Test 4: Web app integration
print("\n4. Testing web app integration...")
try:
    import web_app
    if hasattr(web_app, 'bedrock_ai') and web_app.bedrock_ai:
        print("   ✓ Bedrock integrated in web_app.py")
    else:
        print("   ⚠ Bedrock not found in web_app.py")
except Exception as e:
    print(f"   ⚠ Could not test web_app: {e}")

print("\n" + "="*80)
print("✓ BEDROCK AI INTEGRATION COMPLETE!")
print("="*80)
print("\nNext steps:")
print("1. Start your app: python web_app.py")
print("2. Test AI chat: POST http://localhost:5000/api/ai/chat")
print("3. Deploy to AWS: eb deploy")
print("\n")
