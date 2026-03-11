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
            print(f"✓ Bedrock AI ready with {model} in {region}")
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

When you have enough information to search, provide search parameters in your response.

IMPORTANT: If the user asks about displayed phones (like "which is best", "best camera", "list phones"), 
use the displayedPhones data in context to answer. Each phone has CPI scores:
- overall_cpi: Overall quality score
- camera_score: Camera quality
- battery_score: Battery performance
- display_score: Display quality
- processor_score: Processor performance
- storage_score: Storage capacity
- price_value_ratio: Value for money

Answer based on these scores. For "best phone", use overall_cpi. For "best camera", use camera_score, etc."""

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
            
            # Add displayed phones data if available
            if context.get('displayedPhones'):
                phones = context['displayedPhones']
                context_info += f"\n\nCurrently displayed phones ({len(phones)} phones):"
                for i, phone in enumerate(phones[:10], 1):  # Show top 10
                    context_info += f"\n{i}. {phone.get('name', 'Unknown')} - ₹{phone.get('price', 0):,}"
                    context_info += f" | CPI: {phone.get('overall_cpi', 0):.1f}"
                    context_info += f" | Camera: {phone.get('camera_score', 0):.1f}"
                    context_info += f" | Battery: {phone.get('battery_score', 0):.1f}"
                if len(phones) > 10:
                    context_info += f"\n... and {len(phones) - 10} more phones"
        
        # Build conversation history for Claude
        messages = []
        for msg in self.conversation_history[-5:]:  # Last 5 messages for context
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})
        
        # Add current message
        full_message = f"{user_message}{context_info}"
        messages.append({"role": "user", "content": full_message})
        
        try:
            # Build request body based on model type
            request_body = self._build_request_body(messages, system_prompt, max_tokens=1000, temperature=0.7)
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            ai_response = self._extract_response_text(response_body)
            
            # Store in conversation history
            self.conversation_history.append({
                "user": user_message,
                "assistant": ai_response
            })
            
            # Parse response for search parameters
            search_params = self._extract_search_params(ai_response, context)
            ready_to_search = search_params is not None
            
            # Debug logging
            if search_params:
                print(f'[DEBUG] Search params extracted: {search_params}')
            else:
                print(f'[DEBUG] No search params found. User message: {user_message[:50]}...')
            
            # Extract criteria from user message for intelligent ranking
            import re
            criteria = []
            message_lower = user_message.lower()
            if re.search(r'(camera|photo|picture|selfie)', message_lower):
                criteria.append('camera')
            if re.search(r'(battery|backup|charging|power)', message_lower):
                criteria.append('battery')
            if re.search(r'(display|screen|watch|gaming)', message_lower):
                criteria.append('display')
            if re.search(r'(performance|fast|speed|processor)', message_lower):
                criteria.append('performance')
            if re.search(r'(storage|memory|space)', message_lower):
                criteria.append('storage')
            
            return {
                "response": ai_response,
                "suggestions": self._extract_suggestions(ai_response),
                "search_params": search_params,
                "ready_to_search": ready_to_search,
                "criteria": criteria  # Pass criteria for intelligent ranking
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
            messages = [{"role": "user", "content": prompt}]
            request_body = self._build_request_body(messages, "", max_tokens=1500, temperature=0.7)
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return self._extract_response_text(response_body)
            
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
            messages = [{"role": "user", "content": prompt}]
            request_body = self._build_request_body(messages, "", max_tokens=800, temperature=0.7)
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            summary_text = self._extract_response_text(response_body)
            
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
            messages = [{"role": "user", "content": prompt}]
            request_body = self._build_request_body(messages, "", max_tokens=800, temperature=0.8)
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            recommendations_text = self._extract_response_text(response_body)
            
            # Parse recommendations (simple split by lines)
            recommendations = [line.strip() for line in recommendations_text.split('\n') 
                             if line.strip() and not line.strip().startswith('#')]
            
            return recommendations[:5]
            
        except Exception as e:
            print(f"Recommendations error: {e}")
            return []
    
    def _extract_search_params(self, response: str, context: Optional[Dict]) -> Optional[Dict]:
        """Extract search parameters from AI response and user message"""
        import re
        
        # Get original user message from context if available
        user_message = ""
        if context and 'message' in context:
            user_message = context['message'].lower()
        
        response_lower = response.lower()
        combined = (user_message + " " + response_lower).lower()
        
        # Check if this is a product search query
        product_keywords = ['phone', 'mobile', 'laptop', 'headphone', 'watch', 'tablet', 
                           'smartphone', 'computer', 'earphone', 'earbud', 'notebook']
        
        has_product = any(keyword in combined for keyword in product_keywords)
        if not has_product:
            return None
        
        # Extract product type - prioritize user message over AI response
        query = None
        for keyword in product_keywords:
            if keyword in user_message:
                query = keyword
                break
        
        # If not found in user message, check combined
        if not query:
            for keyword in product_keywords:
                if keyword in combined:
                    query = keyword
                    break
        
        # Extract budget from user message (more reliable than AI response)
        budget = None
        
        # Try patterns like "under 50k", "under 50000", "below 30k", "less than 40000"
        budget_patterns = [
            r'under\s+(\d+)k',
            r'below\s+(\d+)k', 
            r'less\s+than\s+(\d+)k',
            r'under\s+(\d+)',
            r'below\s+(\d+)',
            r'less\s+than\s+(\d+)',
            r'budget\s+(\d+)k',
            r'budget\s+(\d+)',
            r'(\d+)k\s+budget',
            r'(\d+)\s+budget'
        ]
        
        # First try user message for budget
        for pattern in budget_patterns:
            match = re.search(pattern, user_message)
            if match:
                amount = int(match.group(1))
                # If it's in 'k' format, multiply by 1000
                if 'k' in pattern:
                    budget = amount * 1000
                else:
                    # If number is less than 1000, assume it's in thousands
                    budget = amount * 1000 if amount < 1000 else amount
                break
        
        # If not found in user message, try combined
        if not budget:
            for pattern in budget_patterns:
                match = re.search(pattern, combined)
                if match:
                    amount = int(match.group(1))
                    if 'k' in pattern:
                        budget = amount * 1000
                    else:
                        budget = amount * 1000 if amount < 1000 else amount
                    break
        
        # Also check context for budget
        if not budget and context and context.get('budget'):
            budget = context['budget']
        
        if query:
            return {
                "query": query,
                "budget": budget,
                "max_results": 20
            }
        
        return None
    

    
    def extract_criteria_and_rank(self, user_message: str, products: list) -> dict:
        """
        Extract multiple criteria from user query and intelligently rank products
        
        Args:
            user_message: User's search query
            products: List of products with CPI scores
            
        Returns:
            Dict with ranked products, criteria, and AI suggestions
        """
        import re
        
        message_lower = user_message.lower()
        
        # Extract criteria from user message
        criteria = []
        criteria_scores = {}
        
        # Camera keywords
        if re.search(r'(camera|photo|picture|selfie|photography)', message_lower):
            criteria.append('camera')
            criteria_scores['camera'] = 'camera_score'
        
        # Battery keywords
        if re.search(r'(battery|backup|charging|power|long lasting)', message_lower):
            criteria.append('battery')
            criteria_scores['battery'] = 'battery_score'
        
        # Display keywords
        if re.search(r'(display|screen|watch|gaming|amoled)', message_lower):
            criteria.append('display')
            criteria_scores['display'] = 'display_score'
        
        # Performance keywords
        if re.search(r'(performance|fast|speed|processor|gaming)', message_lower):
            criteria.append('performance')
            criteria_scores['performance'] = 'processor_score'
        
        # Storage keywords
        if re.search(r'(storage|memory|space|lots of photos)', message_lower):
            criteria.append('storage')
            criteria_scores['storage'] = 'storage_score'
        
        # If no criteria found, return products as-is
        if not criteria:
            return {
                'ranked_products': products,
                'criteria': [],
                'suggestions': [],
                'banners': {}
            }
        
        # Add implicit 3rd criterion based on primary criterion
        implicit_criteria = {
            'camera': 'storage',  # Camera users need storage
            'gaming': 'battery',  # Gamers need battery
            'display': 'battery'  # Display users watch videos, need battery
        }
        
        # Add implicit criterion if only 1-2 criteria specified
        if len(criteria) <= 2:
            for crit in criteria:
                if crit in implicit_criteria and implicit_criteria[crit] not in criteria:
                    implicit_crit = implicit_criteria[crit]
                    criteria.append(implicit_crit)
                    criteria_scores[implicit_crit] = criteria_scores.get(implicit_crit, f'{implicit_crit}_score')
                    break
        
        # Rank products based on multiple criteria
        ranked_products = []
        suggestions = []
        banners = {}
        
        # Calculate composite scores
        for product in products:
            cpi_scores = product.get('cpi_scores', {})
            
            # Calculate average of specified criteria
            scores = []
            for crit in criteria[:2]:  # Primary criteria
                score_key = criteria_scores.get(crit, f'{crit}_score')
                scores.append(cpi_scores.get(score_key, 0))
            
            if scores:
                product['composite_score'] = sum(scores) / len(scores)
                product['criteria_scores'] = {crit: cpi_scores.get(criteria_scores[crit], 0) for crit in criteria}
            else:
                product['composite_score'] = cpi_scores.get('overall_cpi', 0)
                product['criteria_scores'] = {}
            
            ranked_products.append(product)
        
        # Sort by composite score, then 3rd criterion, then overall_cpi
        ranked_products.sort(key=lambda x: (
            x['composite_score'],
            x['cpi_scores'].get(criteria_scores.get(criteria[2], 'storage_score'), 0) if len(criteria) > 2 else 0,
            x['cpi_scores'].get('overall_cpi', 0)
        ), reverse=True)
        
        # Find best scores for each criterion
        best_scores = {}
        for crit in criteria[:2]:
            score_key = criteria_scores[crit]
            best_scores[crit] = max([p['cpi_scores'].get(score_key, 0) for p in ranked_products])
        
        # Identify balanced options (within 20% of best in each criterion)
        for i, product in enumerate(ranked_products):
            product_banners = []
            
            # Check if it's a balanced option
            is_balanced = False
            for crit in criteria[:2]:
                score_key = criteria_scores[crit]
                product_score = product['cpi_scores'].get(score_key, 0)
                best_score = best_scores[crit]
                
                if best_score > 0:
                    percentage = (product_score / best_score) * 100
                    if 80 <= percentage < 100:  # Within 20% but not the best
                        is_balanced = True
                        product_banners.append(f"Balanced {crit}: {product_score:.1f} ({percentage:.0f}% of best)")
            
            if is_balanced and len(criteria) >= 2:
                banners[product['name']] = {
                    'type': 'balanced',
                    'message': f" Balanced Approach: Great {' & '.join(criteria[:2])} combination",
                    'details': product_banners
                }
            
            # Add storage suggestion for camera users
            if 'camera' in criteria and 'storage' not in criteria[:2]:
                storage_score = product['cpi_scores'].get('storage_score', 0)
                if storage_score >= 7.5:  # Good storage
                    if product['name'] not in banners:
                        banners[product['name']] = {
                            'type': 'storage',
                            'message': ' Better Storage: Great for lots of photos',
                            'details': [f"Storage score: {storage_score:.1f}"]
                        }
        
        # Generate AI suggestions
        if 'camera' in criteria and 'storage' not in criteria:
            suggestions.append(" Tip: If you take lots of photos, consider phones with better storage options")
        
        if len(criteria) >= 2:
            suggestions.append(f" Showing phones optimized for {' and '.join(criteria[:2])}")
        
        return {
            'ranked_products': ranked_products,
            'criteria': criteria,
            'suggestions': suggestions,
            'banners': banners
        }

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
    
    
    @classmethod
    def get_available_models(cls) -> Dict[str, str]:
        """Get list of available AI models with descriptions"""
        return {
            'mistral-small': 'Mistral Small (Default - Available)',
            'mistral-small': 'Mistral Small (Budget-friendly)',
            'claude-sonnet': 'Claude 3.5 Sonnet (Latest)',
            'claude-haiku': 'Claude 3 Haiku (Fast)',
            'llama3-70b': 'Llama 3 70B (Open Source)',
            'titan': 'Amazon Titan (AWS Native)'
        }
    
    def switch_model(self, model: str) -> bool:
        """Switch to a different AI model"""
        if model in self.MODELS:
            old_model_id = self.model_id
            self.model_id = self.MODELS[model]
            self.conversation_history = []  # Reset conversation when switching models
            print(f'Switched from {old_model_id} to {self.model_id}')
            return True
        else:
            print(f'Model {model} not available')
            return False
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
