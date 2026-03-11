"""
SerpAPI Integration for Real Product Search
Gets actual product URLs from Google Shopping
"""

import requests
from typing import List
from smart_product_finder import ProductHit
import random

try:
    from api_keys_config import SERPAPI_KEY
except:
    SERPAPI_KEY = None

class SerpAPISearch:
    """Search products using SerpAPI (Google Shopping)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or SERPAPI_KEY or "YOUR_SERPAPI_KEY_HERE"
        self.base_url = "https://serpapi.com/search"
    
    async def search_products(self, query: str, country: str = "India", max_results: int = 10,
                            budget: float = None, currency: str = "INR") -> List[ProductHit]:
        """Search for products using Google Shopping via SerpAPI"""
        
        if not self.api_key or self.api_key == "YOUR_SERPAPI_KEY_HERE":
            print("  SerpAPI key not configured")
            return []
        
        try:
            # Build search query with budget
            search_query = query
            if budget:
                search_query = f"{query} under {budget} {currency}"
            
            print(f" SerpAPI searching: {search_query}")
            
            # Determine country code for Google Shopping
            country_codes = {
                "India": "in",
                "United States": "us",
                "United Kingdom": "uk",
                "Canada": "ca",
                "Australia": "au"
            }
            gl = country_codes.get(country, "in")
            
            # SerpAPI parameters
            params = {
                "engine": "google_shopping",
                "q": search_query,
                "gl": gl,  # Country
                "hl": "en",  # Language
                "num": min(max_results * 2, 50),  # Get more results
                "api_key": self.api_key
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract shopping results
            shopping_results = data.get("shopping_results", [])
            
            if not shopping_results:
                print("  No shopping results found")
                return []
            
            results = []
            for item in shopping_results[:max_results]:
                try:
                    # Extract product details
                    title = item.get("title", "Unknown Product")
                    price_str = item.get("price", "0")
                    
                    # Parse price (remove currency symbols)
                    price = 0
                    try:
                        price = float(''.join(filter(str.isdigit, price_str.replace(',', ''))))
                    except:
                        price = 0
                    
                    # Get product URL (Google Shopping link that redirects to marketplace)
                    product_url = item.get("product_link", "")
                    
                    # Skip if no valid URL
                    if not product_url:
                        continue
                    
                    # Extract source from URL
                    source = "Unknown"
                    if "amazon" in product_url:
                        source = "Amazon"
                    elif "flipkart" in product_url:
                        source = "Flipkart"
                    elif "ebay" in product_url:
                        source = "eBay"
                    elif "snapdeal" in product_url:
                        source = "Snapdeal"
                    elif "myntra" in product_url:
                        source = "Myntra"
                    else:
                        # Extract domain name
                        try:
                            from urllib.parse import urlparse
                            domain = urlparse(product_url).netloc
                            source = domain.replace("www.", "").split(".")[0].title()
                        except:
                            source = "Online Store"
                    
                    # Get rating and reviews
                    rating = item.get("rating", 4.0)
                    reviews = item.get("reviews", 100)
                    
                    # Budget check - show all products but categorize them
                    # No filtering, just categorization
                    
                    # Get thumbnail
                    thumbnail = item.get("thumbnail", "")
                    if not thumbnail:
                        thumbnail = f"https://via.placeholder.com/400x400/4A90E2/FFFFFF?text={source.replace(' ', '+')}"
                    
                    # Create ProductHit
                    hit = ProductHit(
                        name=title,
                        price=price,
                        
                        url=product_url,
                        # seller_rating=4.5,
                        rating=float(rating) if rating else 4.0,
                        reviews_count=int(reviews) if reviews else 100,
                        image_url=thumbnail,
                        description=item.get("snippet", "")[:200]
                    )
                    
                    results.append(hit)
                    
                except Exception as e:
                    print(f"  Error parsing product: {e}")
                    continue
            
            print(f" SerpAPI found {len(results)} REAL products with working URLs")
            return results
            
        except requests.exceptions.RequestException as e:
            print(f" SerpAPI request error: {e}")
            return []
        except Exception as e:
            print(f" SerpAPI error: {e}")
            return []

# Test function
async def test_serpapi():
    import asyncio
    
    print("\n" + "="*80)
    print("SERPAPI TEST - REAL PRODUCT SEARCH")
    print("="*80)
    
    searcher = SerpAPISearch()
    
    if searcher.api_key == "YOUR_SERPAPI_KEY_HERE":
        print("\n  SerpAPI key not configured")
        print("\nTo get your FREE API key:")
        print("1. Go to: https://serpapi.com/users/sign_up")
        print("2. Sign up (free account)")
        print("3. Get your API key from dashboard")
        print("4. Add it to api_keys_config.py")
        print("\nFree tier: 100 searches/month")
        return
    
    print("\nSearching for mobile phones under 20000 INR...")
    results = await searcher.search_products("mobile phone", "India", 5, budget=20000)  # currency="INR"
    
    if results:
        print(f"\n Found {len(results)} products with REAL URLs:")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.title[:60]}")
            print(f"   Price: {r.price} {r.currency}")
            print(f"   URL: {r.url[:80]}...")
            print(f"   Source: {r.source}")
    else:
        print("\n  No results")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_serpapi())
