from google import genai
import json
try:
    from api_keys_config import GEMINI_API_KEY
except:
    GEMINI_API_KEY = None
import asyncio
from typing import List
from smart_product_finder import ProductHit
import random

class GeminiProductSearch:
    # List of models to try in order (best to fallback)
    MODELS = [
        "gemini-2.0-flash",
        "gemini-2.5-flash", 
        "gemini-2.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    
    # Query optimization templates for better search results
    QUERY_TEMPLATES = {
        "mobile": "best {query} under {budget} with good camera battery life and performance reviews ratings",
        "phone": "best {query} under {budget} with good camera battery life and performance reviews ratings",
        "laptop": "best {query} under {budget} with good performance battery life and build quality reviews",
        "headphone": "best {query} under {budget} with good sound quality comfort and battery life reviews",
        "earphone": "best {query} under {budget} with good sound quality comfort and battery life reviews",
        "watch": "best {query} under {budget} with good features battery life and build quality reviews",
        "tablet": "best {query} under {budget} with good display performance and battery life reviews",
        "camera": "best {query} under {budget} with good image quality features and build quality reviews",
        "tv": "best {query} under {budget} with good picture quality smart features and build quality reviews",
        "default": "best {query} under {budget} with high ratings good reviews and value for money"
    }
    
    def __init__(self, api_key=None):
        self.api_key = api_key or GEMINI_API_KEY or "YOUR_GEMINI_API_KEY_HERE"
        self.client = None
        self.working_model = None
        
        if self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                self.client = genai.Client(api_key=self.api_key)
                self._find_working_model()
            except Exception as e:
                print(f"  Gemini initialization error: {e}")
                self.client = None
    

    def _is_valid_product_url(self, url: str) -> bool:
        """Check if URL is a valid product page (not placeholder or invalid)"""
        if not url or url == "":
            return False
        
        # Check for placeholder URLs
        invalid_patterns = [
            "example.com",
            "placeholder",
            "actual-product-url",
            "product-url.com",
            "...",
            "PRODUCTID",
            "itm123456789"
        ]
        
        url_lower = url.lower()
        for pattern in invalid_patterns:
            if pattern in url_lower:
                return False
        
        # Check for valid marketplace domains
        valid_domains = [
            "amazon.in", "amazon.com",
            "flipkart.com",
            "ebay.com", "ebay.in",
            "snapdeal.com",
            "walmart.com",
            "myntra.com",
            "ajio.com"
        ]
        
        for domain in valid_domains:
            if domain in url_lower:
                return True
        
        return False

    def _find_working_model(self):
        """Try models in order until one works"""
        if not self.client:
            return
        
        for model in self.MODELS:
            try:
                # Test the model with a simple request
                test_response = self.client.models.generate_content(
                    model=model,
                    contents="Say 'OK'"
                )
                if test_response.text:
                    self.working_model = model
                    print(f" Gemini AI ready with model: {model}")
                    return
            except Exception as e:
                print(f"  Model {model} not available: {str(e)[:50]}")
                continue
        
        print(" No working Gemini models found")
        self.client = None
    
    def _optimize_query(self, query: str, budget: float = None, currency: str = "INR") -> str:
        """Enhance user query for better search results"""
        query_lower = query.lower()
        
        # Find matching template
        template = self.QUERY_TEMPLATES["default"]
        for key in self.QUERY_TEMPLATES:
            if key in query_lower:
                template = self.QUERY_TEMPLATES[key]
                break
        
        # Format budget
        if budget:
            budget_str = f"{budget} {currency}"
        else:
            budget_str = "best price"
        
        optimized = template.format(query=query, budget=budget_str)
        print(f" Optimized query: {optimized}")
        return optimized
    
    async def search_products(self, query: str, country: str = "India", max_results: int = 10, 
                            budget: float = None, currency: str = "INR") -> List[ProductHit]:
        if not self.client or not self.working_model:
            print("  Gemini API not configured, skipping AI search")
            return []
        
        # Optimize the search query
        optimized_query = self._optimize_query(query, budget, currency)
        
        # Build smart prompt with web search instruction
        budget_instruction = ""
        if budget:
            budget_instruction = f"Focus on products within {budget} {currency} budget. Also include 2-3 premium options up to {budget * 1.2} {currency} with excellent ratings."
        
        prompt = f"""I need you to search the web and find REAL products for: "{optimized_query}" in {country}.

{budget_instruction}

STEP 1: Search Google/web for these products on major e-commerce sites:
- Amazon India (amazon.in)
- Flipkart (flipkart.com)  
- Snapdeal (snapdeal.com)
- eBay India (ebay.in)

STEP 2: For each product you find, extract:
- The EXACT product title from the website
- The ACTUAL current price
- The REAL product page URL (must be a working link)
- The marketplace name
- Ratings and reviews if available

STEP 3: Return {max_results} products in this JSON format:
[
  {{
    "title": "Samsung Galaxy M34 5G (Midnight Blue, 6GB, 128GB)",
    "price": 16999,
    "currency": "INR",
    "url": "https://www.amazon.in/dp/B0C4SD8XD9",
    "source": "Amazon",
    "seller_name": "Appario Retail",
    "rating": 4.3,
    "reviews": 2847,
    "description": "50MP Triple Camera, 6000mAh Battery, 120Hz Display"
  }}
]

CRITICAL: 
- URLs MUST be real, working product page links
- Use actual product IDs in URLs (like /dp/B0C4SD8XD9 for Amazon)
- Verify each URL format is correct for the marketplace
- Do NOT use placeholder or example URLs

Return ONLY the JSON array, no other text."""
        
        try:
            print(f" Gemini AI searching with {self.working_model}...")
            
            response = self.client.models.generate_content(
                model=self.working_model,
                contents=prompt
            )
            
            text = response.text.strip()
            print(f" Got response ({len(text)} chars)")
            
            # Extract JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            # Find JSON array
            if "[" in text and "]" in text:
                text = text[text.index("["):text.rindex("]")+1]
            
            products_data = json.loads(text)
            
            if not isinstance(products_data, list):
                print("  Response is not a list")
                return []
            
            results = []
            skipped = 0
            for p in products_data[:max_results]:
                try:
                    product_url = p.get("url", "")
                    
                    # Skip products with invalid URLs
                    if not self._is_valid_product_url(product_url):
                        print(f"  Skipping product with invalid URL: {p.get('title', 'Unknown')[:50]}")
                        skipped += 1
                        continue
                    
                    price = float(p.get("price", 0))
                    
                    # Calculate if within budget or slightly above
                    within_budget = True
                    if budget:
                        within_budget = price <= budget * 1.2  # Allow 20% above budget
                    
                    if not within_budget:
                        continue  # Skip products too far above budget
                    
                    hit = ProductHit(
                        name=p.get("title", "Unknown Product"),
                        price=price,
                        url=product_url,

                        

                        rating=float(p.get("rating", 4.0)),
                        reviews_count=int(p.get("reviews", 100)),
                        image_url=f"https://via.placeholder.com/400x400/4A90E2/FFFFFF?text={p.get('source', 'Product').replace(' ', '+')}",
                        description=p.get("description", "")[:200]
                    )
                    
                    # Add budget indicator
                    if budget:
                        if price <= budget:
                            hit.best_choice_reason = f" Within budget  {p.get('rating', 4.0)}/5.0  {p.get('reviews', 0)} reviews  {p.get('source')}"
                        else:
                            hit.best_choice_reason = f" Slightly above budget but EXCELLENT rating {p.get('rating', 4.0)}/5.0  {p.get('reviews', 0)} reviews  {p.get('source')}"
                    else:
                        hit.best_choice_reason = f"AI-found  {p.get('rating', 4.0)}/5.0  {p.get('reviews', 0)} reviews  {p.get('source')}"
                    
                    results.append(hit)
                except Exception as e:
                    print(f"  Error parsing product: {e}")
                    continue
            
            # Sort results: within budget first (by trust score), then above budget (by rating)
            if budget:
                within = [r for r in results if r.price <= budget]
                above = [r for r in results if r.price > budget]
                
                # Sort within budget by trust score (descending)
                within.sort(key=lambda x: x.trust_score if hasattr(x, 'trust_score') else x.rating, reverse=True)
                
                # Sort above budget by rating (descending)
                above.sort(key=lambda x: x.rating, reverse=True)
                
                results = within + above
            
            print(f" Gemini AI found {len(results)} products (skipped {skipped} with invalid URLs)")
            return results
            
        except json.JSONDecodeError as e:
            print(f" JSON parse error: {e}")
            print(f"Response: {text[:200]}...")
            return []
        except Exception as e:
            print(f" Gemini search error: {e}")
            return []

async def test_gemini():
    print("\n" + "="*80)
    print("GEMINI AI TEST - SMART SEARCH")
    print("="*80)
    
    searcher = GeminiProductSearch()
    
    if not searcher.client:
        print("\n  Gemini not configured")
        print("Add your API key to api_keys_config.py")
        return
    
    # Test 1: Search with budget
    print("\n Test 1: Mobile phone with budget")
    results = await searcher.search_products("mobile phone", "India", 5, budget=20000)  # currency="INR"
    
    if results:
        print(f"\n Found {len(results)} products")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.title}")
            print(f"   Price: {r.price} {r.currency}")
            print(f"   {r.best_choice_reason}")
    else:
        print("\n  No results")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(test_gemini())
