
import json
import hashlib
import time
from typing import Dict, Any, Optional
from collections import OrderedDict
import os

class SearchCacheManager:
    def __init__(self, cache_file='cache/search_cache.json', max_size_mb=500):
        self.cache_file = cache_file
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.cache = OrderedDict()
        self.stats = {'hits': 0, 'misses': 0, 'evictions': 0, 'total_size_bytes': 0}
        os.makedirs(os.path.dirname(cache_file) if os.path.dirname(cache_file) else 'cache', exist_ok=True)
        self.load_cache()
    
    def _generate_key(self, data: Dict) -> str:
        sorted_data = json.dumps(data, sort_keys=True)
        return hashlib.md5(sorted_data.encode()).hexdigest()
    
    def _estimate_size(self, data: Any) -> int:
        return len(json.dumps(data).encode('utf-8'))
    
    def _evict_if_needed(self, new_item_size: int):
        while self.stats['total_size_bytes'] + new_item_size > self.max_size_bytes and self.cache:
            oldest_key = next(iter(self.cache))
            removed_item = self.cache.pop(oldest_key)
            removed_size = self._estimate_size(removed_item)
            self.stats['total_size_bytes'] -= removed_size
            self.stats['evictions'] += 1
    
    def get_specs(self, title: str) -> Optional[Dict]:
        key_data = {'type': 'specs', 'title': title.lower()}
        key = self._generate_key(key_data)
        if key in self.cache:
            self.cache.move_to_end(key)
            self.stats['hits'] += 1
            return self.cache[key]['data']
        self.stats['misses'] += 1
        return None
    
    def set_specs(self, title: str, specs: Dict):
        key_data = {'type': 'specs', 'title': title.lower()}
        key = self._generate_key(key_data)
        cache_entry = {'data': specs, 'timestamp': time.time(), 'type': 'specs'}
        entry_size = self._estimate_size(cache_entry)
        self._evict_if_needed(entry_size)
        self.cache[key] = cache_entry
        self.stats['total_size_bytes'] += entry_size
    
    def get_cpi(self, title: str, price: float) -> Optional[Dict]:
        key_data = {'type': 'cpi', 'title': title.lower(), 'price': round(price, 2)}
        key = self._generate_key(key_data)
        if key in self.cache:
            self.cache.move_to_end(key)
            self.stats['hits'] += 1
            return self.cache[key]['data']
        self.stats['misses'] += 1
        return None
    
    def set_cpi(self, title: str, price: float, cpi_data: Dict):
        key_data = {'type': 'cpi', 'title': title.lower(), 'price': round(price, 2)}
        key = self._generate_key(key_data)
        cache_entry = {'data': cpi_data, 'timestamp': time.time(), 'type': 'cpi'}
        entry_size = self._estimate_size(cache_entry)
        self._evict_if_needed(entry_size)
        self.cache[key] = cache_entry
        self.stats['total_size_bytes'] += entry_size
    
    def get_stats(self) -> Dict:
        hit_rate = (self.stats['hits'] / (self.stats['hits'] + self.stats['misses']) * 100) if (self.stats['hits'] + self.stats['misses']) > 0 else 0
        return {
            'total_entries': len(self.cache),
            'total_size_mb': round(self.stats['total_size_bytes'] / (1024 * 1024), 2),
            'max_size_mb': round(self.max_size_bytes / (1024 * 1024), 2),
            'usage_percent': round((self.stats['total_size_bytes'] / self.max_size_bytes) * 100, 2),
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'evictions': self.stats['evictions']
        }
    
    def save_cache(self):
        try:
            cache_data = {'cache': dict(self.cache), 'stats': self.stats, 'timestamp': time.time()}
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            print(f'Cache saved to {self.cache_file}')
        except Exception as e:
            print(f'Error saving cache: {e}')
    
    def load_cache(self):
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                self.cache = OrderedDict(cache_data.get('cache', {}))
                self.stats = cache_data.get('stats', self.stats)
                print(f'Cache loaded: {len(self.cache)} entries, {round(self.stats["total_size_bytes"] / (1024 * 1024), 2)} MB')
        except Exception as e:
            print(f'Error loading cache: {e}')
            self.cache = OrderedDict()
    
    def clear_cache(self):
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'evictions': 0, 'total_size_bytes': 0}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        print('Cache cleared successfully')
    
    def clear_old_entries(self, max_age_hours=24):
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        keys_to_remove = []
        for key, entry in self.cache.items():
            if current_time - entry.get('timestamp', 0) > max_age_seconds:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            removed_item = self.cache.pop(key)
            removed_size = self._estimate_size(removed_item)
            self.stats['total_size_bytes'] -= removed_size
        print(f'Removed {len(keys_to_remove)} old entries')
        return len(keys_to_remove)
