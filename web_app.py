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


app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Global search engine instance
search_engines = {}


def get_search_engine(country_code: str) -> GeoProductSearchEngine:
    """Get or create search engine for country"""
    if country_code not in search_engines:
        search_engines[country_code] = GeoProductSearchEngine(country_code=country_code)
    return search_engines[country_code]


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
            filtered = [r for r in filtered if r.get('product_rating', 0) >= min_rating]
        
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
            sorted_results = sorted(results, key=lambda x: x.get('product_rating', 0), reverse=reverse)
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
        if sort_by == 'price':
            results.sort(key=lambda x: x['price'], reverse=reverse)
        elif sort_by == 'battery_score':
            results.sort(key=lambda x: x['cpi_scores'].get('battery_score', 0), reverse=reverse)
        elif sort_by == 'display_score':
            results.sort(key=lambda x: x['cpi_scores'].get('display_score', 0), reverse=reverse)
        elif sort_by == 'camera_score':
            results.sort(key=lambda x: x['cpi_scores'].get('camera_score', 0), reverse=reverse)
        elif sort_by == 'processor_score':
            results.sort(key=lambda x: x['cpi_scores'].get('processor_score', 0), reverse=reverse)
        elif sort_by == 'storage_score':
            results.sort(key=lambda x: x['cpi_scores'].get('storage_score', 0), reverse=reverse)
        elif sort_by == 'price_value_ratio':
            results.sort(key=lambda x: x['cpi_scores'].get('price_value_ratio', 0), reverse=reverse)
        else:  # default: overall_cpi
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
        results.sort(key=lambda x: x.get("product_rating", 0), reverse=reverse)
    elif sort_by == "trust":
        results.sort(key=lambda x: x.get("trust_score", 0), reverse=reverse)
    elif sort_by == "quality":
        results.sort(key=lambda x: x.get("quality_score", 0), reverse=reverse)
    elif sort_by == "value":
        results.sort(key=lambda x: x.get("value_score", 0), reverse=reverse)
    else:
        results.sort(key=lambda x: x.get("overall_rank", 0), reverse=reverse)
    
    return results


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
            query=data.get('query', ''),
            max_results=100,
            price_min=data.get('price_min', 0),
            price_max=data.get('price_max', float('inf')),
            min_cpi=data.get('min_cpi', 0),
            sort_by=sort_by,
            sort_order=sort_order
        )
        
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
    bedrock_ai = BedrockShoppingAssistant(region='us-east-1', model='claude-sonnet')
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
        
        # Get AI response
        result = bedrock_ai.chat(message, context)
        
        # If AI wants to search, do it automatically
        if result.get('ready_to_search') and result.get('search_params'):
            search_params = result['search_params']
            query = search_params.get('query', '')
            budget = search_params.get('budget')
            
            if query:
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
                
                result['products'] = products_data
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

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    return jsonify({'ready': bedrock_ai and bedrock_ai.bedrock, 'model': 'Claude 3.5 Sonnet'})



if __name__ == '__main__':
    print("\n" + "="*80)
    print("=== GEO-AWARE PRODUCT SEARCH - WEB APPLICATION")
    print("="*80)
    print("\n Starting server...")
    print(">>> Open your browser and go to: http://localhost:5000")
    print(">>> Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
