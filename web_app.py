"""
Modern Web Application for Geo-Aware Product Search
Flask backend with REST API
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
from typing import List, Dict
import json

from geo_product_finder import GeoProductSearchEngine
from geo_marketplace_config import GeoMarketplaceConfig
from smart_product_finder import ProductHit
from budget_advisor import BudgetAdvisor
from dataclasses import asdict
from live_cpi_calculator import LiveCPICalculator
from search_cache_manager import SearchCacheManager


app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Global search engine instance
search_engines = {}


def get_search_engine(country_code: str) -> GeoProductSearchEngine:
    """Get or create search engine for country"""
    if country_code not in search_engines:
        search_engines[country_code] = GeoProductSearchEngine(country_code=country_code)
    return search_engines[country_code]



# Spec cache to ensure same model shows same specs regardless of storage variant
# Cache is cleared on app restart to get fresh specs with updated prompts
spec_cache = {}

# CPI Calculator instance
cpi_calculator = LiveCPICalculator()

# Search Cache Manager instance
search_cache = SearchCacheManager()

def extract_base_model(title):
    """Extract base model name without storage/RAM/color variants"""
    import re
    # Remove storage variants (128GB, 256GB, 512GB, 1TB, etc.)
    title = re.sub(r'\b\d+\s*(GB|TB|MB)\b', '', title, flags=re.IGNORECASE)
    # Remove RAM variants (6GB RAM, 8GB RAM, etc.)
    title = re.sub(r'\b\d+\s*GB\s*(RAM|Memory)\b', '', title, flags=re.IGNORECASE)
    # Remove color variants in parentheses
    title = re.sub(r'\([^)]*\)', '', title)
    # Remove extra spaces
    title = ' '.join(title.split())
    return title.strip()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get list of supported countries"""
    try:
        countries = GeoMarketplaceConfig.get_all_supported_countries()
        return jsonify({
            'success': True,
            'countries': countries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketplaces/<country_code>', methods=['GET'])
def get_marketplaces(country_code):
    """Get marketplaces for a specific country"""
    try:
        marketplaces = GeoMarketplaceConfig.get_marketplaces_for_country(
            country_code.upper(), 
            popular_only=False
        )
        
        marketplace_data = [
            {
                'name': m.name,
                'domain': m.domain,
                'currency': m.currency,
                'trust_score': m.trust_score,
                'popular': m.popular
            }
            for m in marketplaces
        ]
        
        return jsonify({
            'success': True,
            'marketplaces': marketplace_data,
            'country_code': country_code.upper(),
            'currency': marketplaces[0].currency if marketplaces else 'USD',
            'currency_symbol': GeoMarketplaceConfig.get_currency_symbol(
                marketplaces[0].currency if marketplaces else 'USD'
            )
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
def search_products():
    """Search for products"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        country_code = data.get('country_code', 'US').upper()
        page = data.get('page', 1)
        per_page = data.get('per_page', 20)
        sort_by = data.get('sort_by', 'overall_rank')
        sort_order = data.get('sort_order', 'desc')
        budget = data.get('budget', None)  # Optional budget
        print(f" WEB APP RECEIVED BUDGET: {budget} (type: {type(budget)})")
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Get search engine for country
        engine = get_search_engine(country_code)
        
        # Perform search (run async function in sync context)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(engine.search(query, 100, budget))
        loop.close()
        
        # Convert results to JSON-serializable format
        # Convert results with custom attributes
        results_data = []
        for hit in results:
            hit_dict = asdict(hit)
            if hasattr(hit, 'best_choice_reason'):
                hit_dict['best_choice_reason'] = hit.best_choice_reason
            if hasattr(hit, 'is_best_value'):
                hit_dict['is_best_value'] = hit.is_best_value
            results_data.append(hit_dict)
        
        results_data = _sort_product_results(results_data, sort_by, sort_order)
        
        total_results = len(results_data)
        total_pages = (total_results + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = results_data[start_idx:end_idx]
        
        response_data = {
            'success': True,
            'query': query,
            'country_code': country_code,
            'country_name': engine.country_name,
            'currency': engine.currency,
            'currency_symbol': engine.currency_symbol,
            'total_results': total_results,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'results': paginated_results,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        
        # Add budget analysis if budget provided
        if budget and budget > 0:
            advisor = BudgetAdvisor()
            analysis = advisor.analyze_budget(results, budget, engine.currency)
            response_data['budget_analysis'] = advisor.format_analysis_for_display(analysis)
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/filter', methods=['POST'])
def filter_results():
    """Filter search results"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        filter_type = data.get('filter_type', '')
        filter_value = data.get('filter_value', {})
        
        filtered = results
        
        if filter_type == 'price':
            min_price = filter_value.get('min', 0)
            max_price = filter_value.get('max', float('inf'))
            filtered = [r for r in filtered if min_price <= r['price'] <= max_price]
        
        elif filter_type == 'source':
            source = filter_value.get('source', '').lower()
            filtered = [r for r in filtered if source in r['source'].lower()]
        
        elif filter_type == 'rating':
            min_rating = filter_value.get('min', 0)
            filtered = [r for r in filtered if r.get('rating', 0) >= min_rating]
        
        return jsonify({
            'success': True,
            'filtered_results': filtered,
            'count': len(filtered)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sort', methods=['POST'])
def sort_results():
    """Sort search results"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        sort_by = data.get('sort_by', 'overall_rank')
        order = data.get('order', 'desc')
        
        reverse = (order == 'desc')
        
        if sort_by == 'price':
            sorted_results = sorted(results, key=lambda x: x['price'], reverse=reverse)
        elif sort_by == 'rating':
            sorted_results = sorted(results, key=lambda x: x.get('rating', 0), reverse=reverse)
        elif sort_by == 'trust':
            sorted_results = sorted(results, key=lambda x: x['trust_score'], reverse=reverse)
        elif sort_by == 'quality':
            sorted_results = sorted(results, key=lambda x: x['quality_score'], reverse=reverse)
        elif sort_by == 'value':
            sorted_results = sorted(results, key=lambda x: x['value_score'], reverse=reverse)
        else:  # overall_rank
            sorted_results = sorted(results, key=lambda x: x['overall_rank'], reverse=reverse)
        
        return jsonify({
            'success': True,
            'sorted_results': sorted_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# Mobile CPI Integration
import os

class MobileCPISearchEngine:
    def __init__(self):
        self.mobile_index = []
        self.load_mobile_index()
    
    def load_mobile_index(self):
        try:
            if os.path.exists('mobile_cpi_index.json'):
                with open('mobile_cpi_index.json', 'r', encoding='utf-8') as f:
                    self.mobile_index = json.load(f)
                print(f'Loaded {len(self.mobile_index)} mobile phones with CPI scores')
        except Exception as e:
            print(f'Error loading mobile CPI index: {e}')
            self.mobile_index = []
    
    def search_mobiles(self, query, max_results=100, price_min=0, price_max=float('inf'), min_cpi=0, 
                      sort_by='overall_cpi', sort_order='desc'):
        if not self.mobile_index:
            return []
        query_lower = query.lower().strip()
        results = []
        # Generic queries that should return all phones within filters
        generic_queries = ['mobile', 'phone', 'mobile phone', 'smartphone', 'cell phone', 'cellphone']
        is_generic = query_lower in generic_queries
        for phone in self.mobile_index:
            # If generic query, match all phones; otherwise do specific matching
            if is_generic:
                matches = True
            else:
                matches = query_lower in phone['name'].lower() or query_lower in phone['brand'].lower()
            if matches:
                if price_min <= phone['price'] <= price_max and phone['cpi_scores']['overall_cpi'] >= min_cpi:
                    results.append(phone)
        # Apply sorting
        results = self._sort_results(results, sort_by, sort_order)
        return results[:max_results]
    
    def _sort_results(self, results, sort_by, sort_order):
        reverse = (sort_order == 'desc')
        
        # Two-level sorting: primary criterion first, then overall_cpi as tiebreaker
        if sort_by == 'price':
            # For price, use overall_cpi as tiebreaker (higher CPI is better for same price)
            results.sort(key=lambda x: (x['price'], -x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'battery_score':
            # Sort by battery_score first, then overall_cpi as tiebreaker
            results.sort(key=lambda x: (x['cpi_scores'].get('battery_score', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'display_score':
            results.sort(key=lambda x: (x['cpi_scores'].get('display_score', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'camera_score':
            results.sort(key=lambda x: (x['cpi_scores'].get('camera_score', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'processor_score':
            results.sort(key=lambda x: (x['cpi_scores'].get('processor_score', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'storage_score':
            results.sort(key=lambda x: (x['cpi_scores'].get('storage_score', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        elif sort_by == 'price_value_ratio':
            results.sort(key=lambda x: (x['cpi_scores'].get('price_value_ratio', 0), x['cpi_scores'].get('overall_cpi', 0)), reverse=reverse)
        else:  # default: overall_cpi (no tiebreaker needed)
            results.sort(key=lambda x: x['cpi_scores'].get('overall_cpi', 0), reverse=reverse)
        
        return results
    
    def get_top_phones_by_cpi(self, limit=10):
        if not self.mobile_index:
            return []
        return sorted(self.mobile_index, key=lambda x: x['cpi_scores']['overall_cpi'], reverse=True)[:limit]
    
    def get_best_value_phones(self, limit=10):
        if not self.mobile_index:
            return []
        return sorted(self.mobile_index, key=lambda x: x['cpi_scores']['price_value_ratio'], reverse=True)[:limit]
    
    def get_cpi_statistics(self):
        if not self.mobile_index:
            return {}
        cpi_scores = [phone['cpi_scores']['overall_cpi'] for phone in self.mobile_index]
        prices = [phone['price'] for phone in self.mobile_index]
        brand_counts = {}
        for phone in self.mobile_index:
            brand_counts[phone['brand']] = brand_counts.get(phone['brand'], 0) + 1
        return {
            'total_phones': len(self.mobile_index),
            'avg_cpi_score': round(sum(cpi_scores) / len(cpi_scores), 1),
            'max_cpi_score': round(max(cpi_scores), 1),
            'avg_price': round(sum(prices) / len(prices), 0),
            'price_ranges': {
                'budget': len([p for p in self.mobile_index if p['price'] < 15000]),
                'mid_range': len([p for p in self.mobile_index if 15000 <= p['price'] < 30000]),
                'premium': len([p for p in self.mobile_index if 30000 <= p['price'] < 50000]),
                'ultra_premium': len([p for p in self.mobile_index if p['price'] >= 50000])
            },
            'top_brands': dict(sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }



def _sort_product_results(results, sort_by, sort_order):
    reverse = (sort_order == "desc")
    
    if sort_by == "price":
        results.sort(key=lambda x: x.get("price", 0), reverse=reverse)
    elif sort_by == "rating":
        results.sort(key=lambda x: x.get("rating", 0), reverse=reverse)
    elif sort_by == "trust":
        results.sort(key=lambda x: x.get("trust_score", 0), reverse=reverse)
    elif sort_by == "quality":
        results.sort(key=lambda x: x.get("quality_score", 0), reverse=reverse)
    elif sort_by == "value":
        results.sort(key=lambda x: x.get("value_score", 0), reverse=reverse)
    else:
        results.sort(key=lambda x: x.get("overall_rank", 0), reverse=reverse)
    
    return results



@app.route('/api/extract-specs', methods=['POST'])
def extract_specs():
    """Extract mobile specs using Groq AI (primary) with Gemini fallback + caching"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        snippet = data.get('snippet', '')
        
        if not title:
            return jsonify({'success': False, 'error': 'Title required'})
        
        # Extract base model (without storage/RAM/color variants)
        base_model = extract_base_model(title)
        
        # Check persistent cache first (SearchCacheManager)
        cached_specs = search_cache.get_specs(base_model)
        if cached_specs:
            print(f' Using persistent cache for: {base_model}')
            return jsonify({'success': True, 'specs': cached_specs, 'source': 'persistent_cache'})
        
        # Check in-memory cache (for backward compatibility)
        if base_model in spec_cache:
            print(f' Using memory cache for: {base_model}')
            return jsonify({'success': True, 'specs': spec_cache[base_model], 'source': 'memory_cache'})
        

        # Try database first for known models (faster than AI)
        from mobile_specs_database import get_specs_from_database
        import re
        db_specs = get_specs_from_database(title)
        if db_specs:
            # Extract storage from title (varies per variant)
            storage_match = re.search(r'\b(\d+)\s*(GB|TB)\b', title, re.IGNORECASE)
            if storage_match:
                db_specs['storage'] = storage_match.group(0)
            else:
                db_specs['storage'] = 'Not specified'
            
            # Cache in both memory and persistent cache
            spec_cache[base_model] = db_specs
            search_cache.set_specs(base_model, db_specs)
            print(f' Database specs for: {base_model}')
            return jsonify({'success': True, 'specs': db_specs, 'source': 'database'})
        
        # Try index.json for indexed phones (978 phones with full specs)
        try:
            import json
            with open('mobile_cpi_index.json', 'r', encoding='utf-8') as f:
                indexed_phones = json.load(f)
            
            # Search for matching phone in index
            title_lower = title.lower()
            for phone in indexed_phones:
                phone_name_lower = phone.get('name', '').lower()
                # Check if phone name matches (fuzzy match)
                if all(word in phone_name_lower for word in title_lower.split() if len(word) > 2):
                    # Extract specs from indexed phone
                    index_specs = {
                        'processor': phone.get('processor', 'Not specified'),
                        'battery': phone.get('battery', 'Not specified'),
                        'display': phone.get('display', 'Not specified'),
                        'camera': phone.get('camera', 'Not specified'),
                        'connectivity': phone.get('connectivity', 'Not specified'),
                        'storage': 'Not specified'
                    }
                    
                    # Extract storage from title (varies per variant)
                    storage_match = re.search(r'(\d+)\s*(GB|TB)', title, re.IGNORECASE)
                    if storage_match:
                        index_specs['storage'] = storage_match.group(0)
                    
                    # Cache in both memory and persistent cache
                    spec_cache[base_model] = index_specs
                    search_cache.set_specs(base_model, index_specs)
                    print(f' Index specs for: {base_model}')
                    return jsonify({'success': True, 'specs': index_specs, 'source': 'index'})
        except Exception as e:
            print(f'Index lookup failed: {e}')
        
                # Smart extraction - use phone model knowledge + title
        prompt = f"""You are a mobile phone expert with knowledge of all popular phone models and their specifications.

PRODUCT TITLE: {title}

ADDITIONAL INFO: {snippet}

CRITICAL TASK: Identify the phone model and provide its ACTUAL specifications.

STEP 1 - IDENTIFY THE MODEL:
Look for brand and model name in the title (e.g., "OnePlus Nord 5", "Samsung Galaxy S24", "iPhone 15 Pro", "Redmi Note 13")

STEP 2 - USE YOUR KNOWLEDGE:
If you recognize this phone model, provide its REAL specifications from your knowledge base.
Popular models you should know: OnePlus Nord series, Samsung Galaxy S/A series, iPhone series, Xiaomi Redmi/Mi series, Realme series, Vivo series, Oppo series, etc.

STEP 3 - EXTRACT FROM TITLE:
If specs are mentioned in title, verify they match the model. If not in title, use your knowledge.

STEP 4 - FILL IN SPECS:
- Processor: Use actual chipset for this model (e.g., Nord 5 has Snapdragon 8 Gen 2)
- Battery: Use actual battery capacity for this model
- Display: Use actual display specs for this model
- Camera: Use actual camera setup for this model
- Connectivity: Most 2023+ phones have 5G, older models have 4G
- Storage: Extract from title (this varies per variant)

IMPORTANT RULES:
1. DO NOT say "Not specified" if you know the model - use your knowledge!
2. Only say "Not specified" if you truly don't recognize the phone model
3. For well-known models, provide complete specs even if not in title
4. Be confident - if it's a popular phone, you know its specs!

IMPORTANT PATTERNS TO RECOGNIZE:
- Processor: Look for "Snapdragon", "Dimensity", "Helio", "Exynos", "A15", "A16", "A17" followed by numbers
- Battery: Look for numbers followed by "mAh" (e.g., "5000mAh", "4500mAh")
- Display: Look for numbers followed by "inch" and screen types (AMOLED, LCD, OLED, Super Retina)
- Camera: Look for "MP" (megapixels) - e.g., "50MP", "108MP", "Triple camera", "Quad camera"
- Connectivity: Look for "5G", "4G", "LTE"
- Storage: Extract from title (e.g., "128GB", "256GB") - list all variants if multiple mentioned

Return ONLY valid JSON:
{{"processor": "exact chipset name or Not specified", "battery": "capacity with mAh or Not specified", "display": "size and type or Not specified", "camera": "MP and setup or Not specified", "connectivity": "5G/4G or Not specified", "storage": "all options or Not specified"}}

EXAMPLE 1:
Title: "OnePlus Nord 5 5G (8GB RAM, 128GB Storage) - Snapdragon 8 Gen 2, 50MP Camera"
Output: {{"processor": "Snapdragon 8 Gen 2", "battery": "Not specified", "display": "Not specified", "camera": "50MP", "connectivity": "5G", "storage": "128GB"}}

EXAMPLE 2:
Title: "Samsung Galaxy S24 Ultra 256GB"
Info: "6.8 inch AMOLED, 5000mAh battery, 200MP camera"
Output: {{"processor": "Snapdragon 8 Gen 3", "battery": "5000mAh", "display": "6.8 inch AMOLED", "camera": "200MP", "connectivity": "5G", "storage": "256GB"}}

Now extract for the given product. Return ONLY the JSON, no explanation."""
        
        # Try Groq first (PRIMARY - faster and higher limits)
        try:
            from api_keys_config import GROQ_API_KEY
            from groq import Groq
            
            if GROQ_API_KEY and GROQ_API_KEY != "None":
                groq_client = Groq(api_key=GROQ_API_KEY)
                
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=500
                )
                
                text = response.choices[0].message.content.strip()
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0].strip()
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0].strip()
                
                specs = json.loads(text)
                # Cache the specs in both memory and persistent cache
                spec_cache[base_model] = specs
                search_cache.set_specs(base_model, specs)
                print(f' Groq API extracted specs for: {base_model}')
                return jsonify({'success': True, 'specs': specs, 'source': 'groq'})
        except Exception as e:
            print(f'Groq API failed: {e}')
        
        # Fallback to Gemini with rotation
        try:
            from gemini_search import GeminiProductSearch
            from api_keys_config import GEMINI_API_KEYS
            import random
            
            keys_to_try = GEMINI_API_KEYS.copy()
            random.shuffle(keys_to_try)
            
            for api_key in keys_to_try:
                try:
                    gemini = GeminiProductSearch(api_key=api_key)
                    
                    if gemini.client:
                        response = gemini.client.models.generate_content(
                            model=gemini.working_model or 'gemini-2.0-flash',
                            contents=prompt
                        )
                        
                        text = response.text.strip()
                        if '```json' in text:
                            text = text.split('```json')[1].split('```')[0].strip()
                        elif '```' in text:
                            text = text.split('```')[1].split('```')[0].strip()
                        
                        specs = json.loads(text)
                        # Cache the specs in both memory and persistent cache
                        spec_cache[base_model] = specs
                        search_cache.set_specs(base_model, specs)
                        print(f' Gemini API extracted specs for: {base_model}')
                        return jsonify({'success': True, 'specs': specs, 'source': 'gemini'})
                except Exception as e:
                    print(f'Gemini key failed: {api_key[:20]}...')
                    continue
        except Exception as e:
            print(f'All APIs failed: {e}')
        
        specs = {'processor': 'Not specified', 'battery': 'Not specified', 'display': 'Not specified', 'camera': 'Not specified', 'connectivity': 'Not specified', 'storage': 'Not specified'}
        return jsonify({'success': True, 'specs': specs, 'source': 'fallback'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/api/calculate-cpi', methods=['POST'])
def calculate_cpi():
    """Calculate CPI scores for a product based on its specs"""
    try:
        data = request.get_json()
        specs = data.get('specs', {})
        price = data.get('price', 0)
        title = data.get('title', '')
        
        if not specs:
            return jsonify({'success': False, 'error': 'Specs required'})
        
        # Check cache first (if title provided)
        if title:
            cached_cpi = search_cache.get_cpi(title, price)
            if cached_cpi:
                print(f' Using cached CPI for: {title}')
                return jsonify({'success': True, 'cpi': cached_cpi, 'source': 'cache'})
        
        # Calculate CPI using the calculator
        cpi_data = cpi_calculator.calculate_cpi(specs, price)
        
        # Cache the result (if title provided)
        if title:
            search_cache.set_cpi(title, price, cpi_data)
        
        return jsonify({'success': True, 'cpi': cpi_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


mobile_engine = MobileCPISearchEngine()

@app.route('/mobile')
def mobile_index():
    return render_template('mobile_cpi.html')

@app.route('/api/mobile/search', methods=['POST'])
def search_mobiles():
    try:
        data = request.get_json()
        # Get sorting and pagination parameters
        sort_by = data.get('sort_by', 'overall_cpi')
        sort_order = data.get('sort_order', 'desc')
        page = data.get('page', 1)
        per_page = data.get('per_page', 20)
        
        # Search with sorting (get top 100 results)
        all_results = mobile_engine.search_mobiles(
            query=data.get('query', '').strip(),
            max_results=100,
            price_min=data.get('price_min', 0),
            price_max=data.get('price_max', float('inf')),
            min_cpi=data.get('min_cpi', 0),
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Check if this is a specific model query with no results
        is_specific_model = data.get('query', '').strip() and len(data.get('query', '').strip().split()) >= 2
        
        # If no results for specific model, suggest live search
        if len(all_results) == 0 and is_specific_model:
            return jsonify({
                'success': True,
                'query': data.get('query'),
                'total_results': 0,
                'results': [],
                'live_search_suggestion': True,
                'message': f'No indexed results found. Try the Live Marketplace Search tab for real-time results.'
            })
        
        # Calculate pagination
        total_results = len(all_results)
        total_pages = (total_results + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = all_results[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'query': data.get('query'),
            'total_results': total_results,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'results': paginated_results,
            'sort_by': sort_by,
            'sort_order': sort_order
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mobile/top-cpi', methods=['GET'])
def get_top_cpi_phones():
    try:
        limit = request.args.get('limit', 10, type=int)
        results = mobile_engine.get_top_phones_by_cpi(limit)
        return jsonify({'success': True, 'results': results, 'title': f'Top {len(results)} Phones by CPI Score'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mobile/best-value', methods=['GET'])
def get_best_value_phones():
    try:
        limit = request.args.get('limit', 10, type=int)
        results = mobile_engine.get_best_value_phones(limit)
        return jsonify({'success': True, 'results': results, 'title': f'Top {len(results)} Best Value Phones'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mobile/stats', methods=['GET'])
def get_mobile_stats():
    try:
        stats = mobile_engine.get_cpi_statistics()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
# BEDROCK AI INTEGRATION
try:
    from bedrock_ai_assistant import BedrockShoppingAssistant
    bedrock_ai = BedrockShoppingAssistant(region='us-east-1', model='mistral-small')
    print('✓ Bedrock AI ready')
except:
    bedrock_ai = None

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    if not bedrock_ai or not bedrock_ai.bedrock:
        return jsonify({'success': False, 'error': 'AI not configured'}), 503
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        # Add user message to context for better search extraction
        context['message'] = message
        
        # Check if user is already on mobile page
        on_mobile_page = context.get('page') == 'mobile' or context.get('displayedPhones')
        
        # Get AI response
        result = bedrock_ai.chat(message, context)
        
        # If AI wants to search, do it automatically
        if result.get('ready_to_search') and result.get('search_params'):
            search_params = result['search_params']
            query = search_params.get('query', '')
            budget = search_params.get('budget')
            
            if query:
                # Check if this is a mobile/phone search - redirect to mobile CPI page
                query_lower = query.lower()
                message_lower = message.lower()
                
                # Exclude headphones/earphones from mobile category
                is_headphone = any(word in message_lower for word in ['headphone', 'earphone', 'earbud', 'airpod'])
                
                # Check for mobile keywords
                mobile_keywords = ['phone', 'mobile', 'smartphone', 'iphone', 'samsung', 'oneplus', 'xiaomi', 'realme', 'oppo', 'vivo']
                is_mobile = not is_headphone and any(keyword in query_lower or keyword in message_lower for keyword in mobile_keywords)
                
                # Only redirect if NOT already on mobile page
                if is_mobile and not on_mobile_page:
                    # Return redirect instruction for mobile searches (only from main page)
                    result['redirect'] = True
                    result['redirect_url'] = f'/mobile?query={message}'
                    if budget:
                        result['redirect_url'] += f'&budget={budget}'
                    result['response'] = f"Great! I found mobile phones for you. Taking you to our specialized mobile comparison page where you can see detailed CPI scores, camera ratings, battery performance, and more! "
                    return jsonify({'success': True, **result})
                
                # If already on mobile page, just return the response without redirect
                if is_mobile and on_mobile_page:
                    # AI will answer based on displayedPhones in context
                    return jsonify({'success': True, **result})
                
                # For non-mobile searches, perform regular search
                country_code = context.get('country_code', 'IN')
                engine = get_search_engine(country_code)
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                products = loop.run_until_complete(
                    engine.search(query, max_results=10, budget=budget)
                )
                loop.close()
                
                products_data = []
                for p in products:
                    p_dict = asdict(p)
                    if hasattr(p, 'best_choice_reason'):
                        p_dict['best_choice_reason'] = p.best_choice_reason
                    products_data.append(p_dict)
                
                # Apply intelligent multi-criteria ranking if criteria detected
                ranking_result = bedrock_ai.extract_criteria_and_rank(message, products_data)
                
                result['products'] = ranking_result['ranked_products']
                result['criteria'] = ranking_result['criteria']
                result['suggestions'] = ranking_result['suggestions']
                result['banners'] = ranking_result['banners']
                result['search_performed'] = True
                result['query_used'] = query
        
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/compare', methods=['POST'])
def ai_compare():
    if not bedrock_ai: return jsonify({'error': 'AI not configured'}), 503
    data = request.get_json()
    return jsonify({'comparison': bedrock_ai.compare_products(data.get('products'))})


@app.route('/api/ai/models', methods=['GET'])
def get_ai_models():
    """Get list of available AI models"""
    if not bedrock_ai:
        return jsonify({'success': False, 'error': 'AI not configured'}), 503
    
    try:
        from bedrock_ai_assistant import BedrockShoppingAssistant
        models = BedrockShoppingAssistant.get_available_models()
        return jsonify({'success': True, 'models': models})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/switch-model', methods=['POST'])
def switch_ai_model():
    """Switch AI model"""
    if not bedrock_ai:
        return jsonify({'success': False, 'error': 'AI not configured'}), 503
    
    try:
        data = request.get_json()
        model = data.get('model', 'mistral-large')
        
        success = bedrock_ai.switch_model(model)
        if success:
            return jsonify({'success': True, 'model': model})
        else:
            return jsonify({'success': False, 'error': 'Invalid model'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    return jsonify({'ready': bedrock_ai and bedrock_ai.bedrock, 'model': 'Claude 3.5 Sonnet'})



if __name__ == '__main__':
    import atexit
    
    # Register cache save on app shutdown
    def save_cache_on_exit():
        print('\n Saving cache before shutdown...')
        search_cache.save_cache()
        stats = search_cache.get_stats()
        print(f' Cache saved: {stats["total_entries"]} entries, {stats["total_size_mb"]} MB')
    
    atexit.register(save_cache_on_exit)
    
    print("\n" + "="*80)
    print("=== GEO-AWARE PRODUCT SEARCH - WEB APPLICATION")
    print("="*80)
    print("\n Starting server...")
    print(">>> Open your browser and go to: http://localhost:5000")
    print(">>> Press Ctrl+C to stop the server\n")
    
    # Load cache stats on startup
    stats = search_cache.get_stats()
    print(f' Cache loaded: {stats["total_entries"]} entries, {stats["total_size_mb"]} MB')
    print(f'   Hit rate: {stats["hit_rate_percent"]}% | Usage: {stats["usage_percent"]}%\n')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
