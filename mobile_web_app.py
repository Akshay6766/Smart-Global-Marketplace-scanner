"""
Mobile-focused Web Application with CPI Integration
Flask backend with mobile phone CPI scores
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from typing import List, Dict


app = Flask(__name__)
CORS(app)


class MobileCPISearchEngine:
    """Mobile phone search with CPI scores"""
    
    def __init__(self):
        self.mobile_index = []
        self.load_mobile_index()
    
    def load_mobile_index(self):
        """Load mobile CPI index"""
        try:
            if os.path.exists('mobile_cpi_index.json'):
                with open('mobile_cpi_index.json', 'r', encoding='utf-8') as f:
                    self.mobile_index = json.load(f)
                print(f"✅ Loaded {len(self.mobile_index)} mobile phones with CPI scores")
            else:
                print("⚠️  Mobile CPI index not found. Please run mobile CPI generator first.")
        except Exception as e:
            print(f"❌ Error loading mobile CPI index: {e}")
            self.mobile_index = []
    
    def search_mobiles(self, query: str, max_results: int = 20, 
                      price_min: float = 0, price_max: float = float('inf'),
                      min_cpi: float = 0) -> List[Dict]:
        """Search mobile phones with filters"""
        if not self.mobile_index:
            return []
        
        query_lower = query.lower()
        results = []
        
        for phone in self.mobile_index:
            # Check if query matches
            matches = (
                query_lower in phone['name'].lower() or
                query_lower in phone['brand'].lower() or
                any(query_lower in keyword for keyword in phone.get('search_keywords', []))
            )
            
            if matches:
                # Apply filters
                if (price_min <= phone['price'] <= price_max and 
                    phone['cpi_scores']['overall_cpi'] >= min_cpi):
                    results.append(phone)
        
        # Sort by CPI score (best first)
        results.sort(key=lambda x: x['cpi_scores']['overall_cpi'], reverse=True)
        return results[:max_results]
    
    def get_top_phones_by_cpi(self, limit: int = 10) -> List[Dict]:
        """Get top phones by CPI score"""
        if not self.mobile_index:
            return []
        
        sorted_phones = sorted(
            self.mobile_index, 
            key=lambda x: x['cpi_scores']['overall_cpi'], 
            reverse=True
        )
        return sorted_phones[:limit]
    
    def get_best_value_phones(self, limit: int = 10) -> List[Dict]:
        """Get best value phones by price-value ratio"""
        if not self.mobile_index:
            return []
        
        sorted_phones = sorted(
            self.mobile_index, 
            key=lambda x: x['cpi_scores']['price_value_ratio'], 
            reverse=True
        )
        return sorted_phones[:limit]
    
    def get_phones_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        """Get phones in price range, sorted by CPI"""
        if not self.mobile_index:
            return []
        
        filtered_phones = [
            phone for phone in self.mobile_index 
            if min_price <= phone['price'] <= max_price
        ]
        
        # Sort by CPI
        filtered_phones.sort(key=lambda x: x['cpi_scores']['overall_cpi'], reverse=True)
        return filtered_phones


# Initialize mobile search engine
mobile_engine = MobileCPISearchEngine()


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('mobile_index.html')


@app.route('/api/mobile/search', methods=['POST'])
def search_mobiles():
    """Search mobile phones with CPI scores"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 20)
        price_min = data.get('price_min', 0)
        price_max = data.get('price_max', float('inf'))
        min_cpi = data.get('min_cpi', 0)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Search mobiles
        results = mobile_engine.search_mobiles(
            query=query,
            max_results=max_results,
            price_min=price_min,
            price_max=price_max,
            min_cpi=min_cpi
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'total_results': len(results),
            'results': results,
            'filters_applied': {
                'price_min': price_min,
                'price_max': price_max if price_max != float('inf') else None,
                'min_cpi': min_cpi
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/mobile/top-cpi', methods=['GET'])
def get_top_cpi_phones():
    """Get top phones by CPI score"""
    try:
        limit = request.args.get('limit', 10, type=int)
        results = mobile_engine.get_top_phones_by_cpi(limit)
        
        return jsonify({
            'success': True,
            'results': results,
            'title': f'Top {len(results)} Phones by CPI Score'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/mobile/best-value', methods=['GET'])
def get_best_value_phones():
    """Get best value phones"""
    try:
        limit = request.args.get('limit', 10, type=int)
        results = mobile_engine.get_best_value_phones(limit)
        
        return jsonify({
            'success': True,
            'results': results,
            'title': f'Top {len(results)} Best Value Phones'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/mobile/price-range', methods=['POST'])
def get_phones_by_price():
    """Get phones by price range"""
    try:
        data = request.get_json()
        min_price = data.get('min_price', 0)
        max_price = data.get('max_price', 100000)
        
        results = mobile_engine.get_phones_by_price_range(min_price, max_price)
        
        return jsonify({
            'success': True,
            'results': results,
            'price_range': f'₹{min_price:,} - ₹{max_price:,}',
            'total_results': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/mobile/stats', methods=['GET'])
def get_mobile_stats():
    """Get mobile phone statistics"""
    try:
        if not mobile_engine.mobile_index:
            return jsonify({
                'success': False,
                'error': 'No mobile data available'
            }), 404
        
        phones = mobile_engine.mobile_index
        
        # Calculate statistics
        cpi_scores = [phone['cpi_scores']['overall_cpi'] for phone in phones]
        prices = [phone['price'] for phone in phones]
        
        # Brand distribution
        brand_counts = {}
        for phone in phones:
            brand = phone['brand']
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        # Price ranges
        budget_phones = len([p for p in phones if p['price'] < 15000])
        mid_range_phones = len([p for p in phones if 15000 <= p['price'] < 30000])
        premium_phones = len([p for p in phones if 30000 <= p['price'] < 50000])
        ultra_premium_phones = len([p for p in phones if p['price'] >= 50000])
        
        stats = {
            'total_phones': len(phones),
            'avg_cpi_score': round(sum(cpi_scores) / len(cpi_scores), 1),
            'max_cpi_score': round(max(cpi_scores), 1),
            'min_cpi_score': round(min(cpi_scores), 1),
            'avg_price': round(sum(prices) / len(prices), 0),
            'price_ranges': {
                'budget': budget_phones,
                'mid_range': mid_range_phones,
                'premium': premium_phones,
                'ultra_premium': ultra_premium_phones
            },
            'top_brands': dict(sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*80)
    print("=== MOBILE PHONE SEARCH WITH CPI SCORES")
    print("="*80)
    print(f"\n📱 Loaded {len(mobile_engine.mobile_index)} mobile phones")
    print("🔍 Features:")
    print("   • Search by name, brand, specs")
    print("   • CPI scores for all phones")
    print("   • Price and CPI filtering")
    print("   • Best value recommendations")
    print("   • Top phones by CPI")
    print("\n Starting server...")
    print(">>> Open your browser and go to: http://localhost:5001")
    print(">>> Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)