import boto3
import json

print('Testing Bedrock with Claude Haiku...')
print('=' * 60)

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

try:
    response = bedrock.invoke_model(
        modelId='us.anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 50,
            'messages': [{'role': 'user', 'content': 'Say hi'}]
        })
    )
    result = json.loads(response['body'].read())
    print('SUCCESS! Bedrock is working!')
    print('Response:', result['content'][0]['text'])
except Exception as e:
    print('ERROR:', str(e))
    print('')
    if 'INVALID_PAYMENT_INSTRUMENT' in str(e):
        print('Payment method issue detected.')
        print('Please check:')
        print('1. Payment method is valid and not expired')
        print('2. Wait 2-5 minutes after adding payment method')
        print('3. Check AWS Bedrock console for model access status')
