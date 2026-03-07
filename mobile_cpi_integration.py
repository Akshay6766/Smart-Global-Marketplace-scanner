import json
import os
from typing import List, Dict

class MobileCPISearchEngine:
    def __init__(self, index_file='mobile_cpi_index.json'):
        self.mobile_index = []
        self.load_index(index_file)
    
    def load_index(self, index_file):
        try:
            if os.path.exists(index_file):
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.mobile_index = json.load(f)
                print(f'Loaded {len(self.mobile_index)} mobile phones with CPI scores')
            else:
                print(f'Mobile CPI index file not found: {index_file}')
                self.mobile_index = []
        except Exception as e:
            print(f'Error loading mobile CPI index: {e}')
            self.mobile_index = []
    
    def search_mobiles(self, query, max_results=20, price_min=0, price_max=float('inf'), min_cpi=0):
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
                matches = (query_lower in phone['name'].lower() or 
                          query_lower in phone['brand'].lower() or
                          any(query_lower in keyword for keyword in phone.get('search_keywords', [])))
            
            if matches:
                if (price_min <= phone['price'] <= price_max and 
                    phone['cpi_scores']['overall_cpi'] >= min_cpi):
                    results.append(phone)
        
        results.sort(key=lambda x: x['cpi_scores']['overall_cpi'], reverse=True)
        return results[:max_results]
    
    def get_top_phones_by_cpi(self, limit=10):
        if not self.mobile_index:
            return []
        
        sorted_phones = sorted(self.mobile_index, key=lambda x: x['cpi_scores']['overall_cpi'], reverse=True)
        return sorted_phones[:limit]
    
    def get_best_value_phones(self, limit=10):
        if not self.mobile_index:
            return []
        
        sorted_phones = sorted(self.mobile_index, key=lambda x: x['cpi_scores']['price_value_ratio'], reverse=True)
        return sorted_phones[:limit]
    
    def get_cpi_statistics(self):
        if not self.mobile_index:
            return {}
        
        cpi_scores = [phone['cpi_scores']['overall_cpi'] for phone in self.mobile_index]
        prices = [phone['price'] for phone in self.mobile_index]
        
        brand_counts = {}
        for phone in self.mobile_index:
            brand = phone['brand']
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        budget_phones = len([p for p in self.mobile_index if p['price'] < 15000])
        mid_range_phones = len([p for p in self.mobile_index if 15000 <= p['price'] < 30000])
        premium_phones = len([p for p in self.mobile_index if 30000 <= p['price'] < 50000])
        ultra_premium_phones = len([p for p in self.mobile_index if p['price'] >= 50000])
        
        return {
            'total_phones': len(self.mobile_index),
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

if __name__ == '__main__':
    print('Testing Mobile CPI Search Engine')
    search_engine = MobileCPISearchEngine()
    
    if search_engine.mobile_index:
        print(f'Loaded {len(search_engine.mobile_index)} phones')
        top_phones = search_engine.get_top_phones_by_cpi(3)
        print('Top 3 phones by CPI:')
        for phone in top_phones:
            print(f"  {phone['name']} - CPI: {phone['cpi_scores']['overall_cpi']}")
    else:
        print('No mobile index loaded')
