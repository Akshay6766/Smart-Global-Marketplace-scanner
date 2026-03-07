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
        'claude-sonnet': 'us.anthropic.claude-3-5-sonnet-20241022-v2:0',  # Claude Sonnet 4.6 (Latest - use case submitted)
        'claude-sonnet-v1': 'us.anthropic.claude-3-5-sonnet-20240620-v1:0',  # Claude 3.5 Sonnet v1 (older)
        'claude-haiku': 'us.anthropic.claude-3-haiku-20240307-v1:0',      # Fast & cheap
        'llama3-70b': 'meta.llama3-70b-instruct-v1:0',                 # Open source
        'titan': 'amazon.titan-text-premier-v1:0'                       # AWS native
    }
    
    def __init__(self, region='us-east-1', model='claude-sonnet'):
        """
        Initialize Bedrock client
        
        Args:
            region: AWS region (default: us-east-1)
            model: Model to use (claude-sonnet, claude-haiku, llama3-70b, titan)
        """
        self.region = region
        self.model_id = self.MODELS.get(model, self.MODELS['claude-sonnet'])
        self.conversation_history = []
        
        try:
            self.bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name=region
            )
            print(f"✓ Bedrock AI ready with {model} in {region}")
        except Exception as e:
            print(f"✗ Bedrock initialization error: {e}")
            self.bedrock = None
    
    def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Chat with Claude AI assistant
        
        Args:
            user_message: User's question or request
            context: Optional context (budget, preferences, search history)
        
        Returns:
            Dict with response, suggestions, and search parameters
        """
        if not self.bedrock:
            return {
                "response": "AI assistant is not configured. Please check AWS credentials.",
                "suggestions": [],
                "search_params": None,
                "ready_to_search": False
            }
        
        # Build context-aware system prompt
        system_prompt = """You are a friendly, helpful shopping assistant for an e-commerce platform. 
Your personality is warm, enthusiastic, and genuinely interested in helping users find the perfect products.

Guidelines:
- Be conversational and friendly, not robotic
- Ask clarifying questions naturally
- Show excitement about good deals
- Provide honest recommendations
- Use emojis occasionally to be more engaging
- Remember user preferences from the conversation

When you have enough information to search, provide search parameters in your response."""

        # Build user context
        context_info = ""
        if context:
            if context.get('budget'):
                context_info += f"\nUser's budget: ₹{context['budget']}"
            if context.get('previous_search'):
                context_info += f"\nPrevious search: {context['previous_search']}"
            if context.get('preferences'):
                prefs = context['preferences']
                context_info += f"\nPreferences: {', '.join(prefs)}"
        
        # Build conversation history for Claude
        messages = []
        for msg in self.conversation_history[-5:]:  # Last 5 messages for context
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})
        
        # Add current message
        full_message = f"{user_message}{context_info}"
        messages.append({"role": "user", "content": full_message})
        
        try:
            # Call Claude via Bedrock
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": system_prompt,
                "messages": messages,
                "temperature": 0.7  # Warmer, more creative responses
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            ai_response = response_body['content'][0]['text']
            
            # Store in conversation history
            self.conversation_history.append({
                "user": user_message,
                "assistant": ai_response
            })
            
            # Parse response for search parameters
            search_params = self._extract_search_params(ai_response, context)
            ready_to_search = search_params is not None
            
            return {
                "response": ai_response,
                "suggestions": self._extract_suggestions(ai_response),
                "search_params": search_params,
                "ready_to_search": ready_to_search
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return {
                    "response": "⚠️ Bedrock access denied. Please enable model access in AWS Console.",
                    "suggestions": ["Go to AWS Bedrock Console → Model access → Enable Claude"],
                    "ready_to_search": False
                }
            else:
                return {
                    "response": f"Sorry, I encountered an error: {error_code}",
                    "suggestions": [],
                    "ready_to_search": False
                }
        except Exception as e:
            print(f"Chat error: {e}")
            return {
                "response": "I'm having trouble right now. Could you try rephrasing that?",
                "suggestions": [],
                "ready_to_search": False
            }
    
    def compare_products(self, products: List[Dict]) -> str:
        """Generate AI comparison of products using Claude"""
        if not self.bedrock or len(products) < 2:
            return "Need at least 2 products to compare"
        
        products_info = []
        for i, p in enumerate(products[:5], 1):
            products_info.append(f"""
Product {i}: {p.get('title', 'Unknown')}
- Price: ₹{p.get('price', 0):,}
- Rating: {p.get('product_rating', 0)}/5.0 ({p.get('review_count', 0)} reviews)
- Source: {p.get('source', 'Unknown')}
""")
        
        prompt = f"""Compare these products and help the user decide. Be friendly and conversational!

{chr(10).join(products_info)}

Provide:
1. 🏆 Quick winner for different needs (best value, best quality, best budget)
2. 📊 Key differences that matter
3. 💡 Your honest recommendation with reasoning
4. ⚠️ Any concerns or things to watch out for

Be enthusiastic and helpful, like talking to a friend!"""
        
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1500,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return f"Comparison error: {e}"
    
    def summarize_reviews(self, product_name: str, reviews: List[str]) -> Dict:
        """Summarize product reviews with personality"""
        if not self.bedrock or not reviews:
            return {"summary": "No reviews available", "pros": [], "cons": []}
        
        reviews_text = "\n".join([f"- {r}" for r in reviews[:20]])
        
        prompt = f"""Analyze these reviews for "{product_name}" and give me the real scoop! 🔍

Reviews:
{reviews_text}

Give me:
1. Overall vibe (is it worth it?)
2. Top 3 things people LOVE ❤️
3. Top 2-3 complaints 😕
4. Your honest take

Be real and conversational, like you're telling a friend!"""
        
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 800,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            summary_text = response_body['content'][0]['text']
            
            return {
                "summary": summary_text,
                "sentiment": "positive",  # Could parse from response
                "raw_response": summary_text
            }
            
        except Exception as e:
            return {"summary": f"Error: {e}", "pros": [], "cons": []}
    
    def get_personalized_recommendations(self, search_history: List[str], 
                                        preferences: Dict) -> List[str]:
        """Get personalized product recommendations"""
        if not self.bedrock:
            return []
        
        history_text = "\n".join([f"- {s}" for s in search_history[-10:]])
        prefs_text = json.dumps(preferences, indent=2)
        
        prompt = f"""Based on this user's shopping behavior, suggest 5 products they might love:

Recent searches:
{history_text}

Preferences:
{prefs_text}

Give me 5 specific product suggestions with brief reasons why they'd like each one.
Be enthusiastic and personalized!"""
        
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 800,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            recommendations_text = response_body['content'][0]['text']
            
            # Parse recommendations (simple split by lines)
            recommendations = [line.strip() for line in recommendations_text.split('\n') 
                             if line.strip() and not line.strip().startswith('#')]
            
            return recommendations[:5]
            
        except Exception as e:
            print(f"Recommendations error: {e}")
            return []
    
    def _extract_search_params(self, response: str, context: Optional[Dict]) -> Optional[Dict]:
        """Extract search parameters from AI response"""
        # Simple keyword extraction
        response_lower = response.lower()
        
        # Check if AI is ready to search
        search_indicators = ['search for', 'look for', 'find', 'show you', 'here are']
        if not any(indicator in response_lower for indicator in search_indicators):
            return None
        
        # Extract budget from context or response
        budget = None
        if context and context.get('budget'):
            budget = context['budget']
        
        # Try to extract product category/query from response
        # This is simplified - in production, use more sophisticated NLP
        query = None
        for word in ['phone', 'mobile', 'laptop', 'headphone', 'watch', 'tablet']:
            if word in response_lower:
                query = word
                break
        
        if query:
            return {
                "query": query,
                "budget": budget,
                "max_results": 20
            }
        
        return None
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract suggestions from AI response"""
        # Simple extraction - look for bullet points or numbered lists
        suggestions = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ', '1.', '2.', '3.')):
                suggestions.append(line.lstrip('-•*123456789. '))
        
        return suggestions[:5]
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✓ Conversation reset")


# Test the Bedrock assistant
if __name__ == "__main__":
    print("\n" + "="*80)
    print("AMAZON BEDROCK AI ASSISTANT TEST")
    print("="*80)
    
    assistant = BedrockShoppingAssistant(region='us-east-1', model='claude-sonnet')
    
    if not assistant.bedrock:
        print("\n⚠️  Bedrock not configured")
        print("\nSetup steps:")
        print("1. Go to AWS Console → Bedrock")
        print("2. Click 'Model access' in left sidebar")
        print("3. Enable 'Claude 3.5 Sonnet'")
        print("4. Ensure your AWS credentials are configured")
    else:
        # Test conversation
        print("\n📱 Test 1: Initial query")
        result = assistant.chat("I need a good mobile phone")
        print(f"AI: {result['response']}")
        print(f"Ready to search: {result['ready_to_search']}")
        
        print("\n💰 Test 2: With budget")
        result = assistant.chat("My budget is 25000 rupees", {"budget": 25000})
        print(f"AI: {result['response']}")
        if result.get('search_params'):
            print(f"Search params: {result['search_params']}")
        
        print("\n" + "="*80)
