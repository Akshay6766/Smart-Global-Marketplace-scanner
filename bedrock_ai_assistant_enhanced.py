"""
Amazon Bedrock AI Assistant - Conversational Shopping with Claude
Uses AWS Bedrock with Claude 3.5 Sonnet for warm, helpful personality
"""

import boto3
import json
from typing import List, Dict, Optional
from botocore.exceptions import ClientError


class BedrockShoppingAssistant:
    """
    AI Shopping Assistant powered by Amazon Bedrock (Claude 3.5 Sonnet)
    Provides warm, conversational product recommendations
    """
    
    # Available models in Bedrock
    MODELS = {
        'mistral-large': 'mistral.mistral-large-2407-v1:0',            # Mistral Large (DEFAULT - Fast & Smart)
        'mistral-small': 'mistral.mistral-small-2402-v1:0',            # Mistral Small (Budget-friendly) - try v1:0
        'mistral-small-alt': 'mistral.mistral-small-2402-v1:0',        # Alternative ID
        'claude-sonnet': 'anthropic.claude-3-5-sonnet-20241022-v2:0',  # Claude Sonnet 4.6 (Latest)
        'claude-sonnet-v1': 'us.anthropic.claude-3-5-sonnet-20240620-v1:0',  # Claude 3.5 Sonnet v1
        'claude-haiku': 'us.anthropic.claude-3-haiku-20240307-v1:0',      # Fast & cheap
        'llama3-70b': 'meta.llama3-70b-instruct-v1:0',                 # Open source
        'titan': 'amazon.titan-text-premier-v1:0'                       # AWS native
    }
    
    def __init__(self, region='us-east-1', model='claude-haiku'):
        """
        Initialize Bedrock client
        
        Args:
            region: AWS region (default: us-east-1)
            model: Model to use (mistral-large, claude-sonnet, claude-haiku, llama3-70b, titan)
        """
        self.region = region
        self.model_id = self.MODELS.get(model, self.MODELS['claude-haiku'])
        self.conversation_history = []
        
        try:
            self.bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name=region
            )
            print(f"✓ Bedrock AI ready with {model} ({self.model_id}) in {region}")
        except Exception as e:
            print(f"✗ Bedrock initialization error: {e}")
            self.bedrock = None
    
    
    def _is_claude_model(self) -> bool:
        """Check if current model is a Claude model"""
        return 'claude' in self.model_id.lower()
    
    def _is_mistral_model(self) -> bool:
        """Check if current model is a Mistral model"""
        return 'mistral' in self.model_id.lower()
    
    def _build_request_body(self, messages: list, system_prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> dict:
        """Build request body based on model type"""
        if self._is_claude_model():
            # Claude format
            return {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
                "temperature": temperature
            }
        elif self._is_mistral_model():
            # Mistral format for AWS Bedrock - uses <s>[INST] instruction format
            prompt_text = "<s>"
            
            # Add system prompt in first instruction
            if system_prompt and messages:
                first_msg = messages[0]['content']
                prompt_text += f"[INST] {system_prompt}\n\n{first_msg} [/INST]"
                messages = messages[1:]  # Skip first message as it's already added
            elif messages:
                prompt_text += f"[INST] {messages[0]['content']} [/INST]"
                messages = messages[1:]
            
            # Add remaining conversation
            for msg in messages:
                if msg['role'] == 'user':
                    prompt_text += f"</s><s>[INST] {msg['content']} [/INST]"
                elif msg['role'] == 'assistant':
                    prompt_text += f" {msg['content']}"
            
            return {
                "prompt": prompt_text,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "top_k": 50
            }
        else:
            # Generic format for other models (Llama, Titan)
            prompt_text = f"{system_prompt}\n\n"
            for msg in messages:
                role = msg['role'].capitalize()
                prompt_text += f"{role}: {msg['content']}\n\n"
            prompt_text += "Assistant: "
            return {
                "inputText": prompt_text,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature
                }
            }

    def _extract_response_text(self, response_body: dict) -> str:
        """Extract response text based on model type"""
        if self._is_claude_model():
            return response_body['content'][0]['text']
        elif self._is_mistral_model():
            # Mistral returns outputs array with text
            outputs = response_body.get('outputs', [])
            if outputs and len(outputs) > 0:
                return outputs[0].get('text', '')
            return ''
        else:
            # Generic format (Titan, Llama)
            return response_body.get('results', [{}])[0].get('outputText', '')