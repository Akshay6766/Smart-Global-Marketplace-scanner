"""
Live CPI Calculator for Marketplace Products
Calculates CPI scores for live search results using the same logic as indexed phones
"""

import re
from typing import Dict


class LiveCPICalculator:
    """Calculate CPI scores for live marketplace products"""
    
    def __init__(self):
        self.processor_rankings = {
            'snapdragon 8 elite': 100,
            'snapdragon 8 gen 3': 95,
            'snapdragon 8s gen 3': 90,
            'snapdragon 8 gen 2': 88,
            'snapdragon 8+ gen 1': 85,
            'snapdragon 7+ gen 3': 80,
            'snapdragon 7s gen 3': 75,
            'snapdragon 7s gen 2': 70,
            'snapdragon 7 gen 3': 72,
            'snapdragon 7 gen 1': 68,
            'snapdragon 695': 60,
            'dimensity 9300': 92,
            'dimensity 9200': 88,
            'dimensity 8450': 82,
            'dimensity 8350': 80,
            'dimensity 8200': 78,
            'dimensity 7400': 75,
            'dimensity 7300': 72,
            'dimensity 7050': 70,
            'dimensity 6300': 60,
            'exynos 2400': 90,
            'exynos 1480': 75,
            'exynos 1380': 70,
            'a17 pro': 98,
            'a16': 92,
            'a15': 88,
            'tensor g3': 85,
            'tensor g2': 80,
        }
    
    def extract_processor_score(self, processor: str) -> float:
        """Score processor from 0-100"""
        if not processor or processor == 'Not specified':
            return 50
        
        processor_lower = processor.lower()
        
        # Find processor in rankings
        for proc_name, score in self.processor_rankings.items():
            if proc_name in processor_lower:
                return score
        
        # Default scoring by brand
        if 'snapdragon' in processor_lower:
            return 70
        elif 'dimensity' in processor_lower:
            return 65
        elif 'exynos' in processor_lower:
            return 60
        elif 'helio' in processor_lower:
            return 55
        elif 'bionic' in processor_lower or 'apple' in processor_lower:
            return 85
        
        return 50
    
    def extract_display_score(self, display: str) -> float:
        """Score display from 0-100"""
        if not display or display == 'Not specified':
            return 50
        
        display_lower = display.lower()
        score = 50  # Base score
        
        # Screen size scoring
        size_match = re.search(r'(\d+\.?\d*)\s*inch', display_lower)
        if size_match:
            size = float(size_match.group(1))
            if size >= 6.7:
                score += 15
            elif size >= 6.5:
                score += 12
            elif size >= 6.0:
                score += 10
        
        # Display type scoring
        if 'amoled' in display_lower or 'oled' in display_lower:
            score += 20
        elif 'lcd' in display_lower:
            score += 10
        
        # Refresh rate scoring
        if '144' in display_lower and 'hz' in display_lower:
            score += 15
        elif '120' in display_lower and 'hz' in display_lower:
            score += 12
        elif '90' in display_lower and 'hz' in display_lower:
            score += 8
        
        return min(score, 100)
    
    def extract_camera_score(self, camera: str) -> float:
        """Score camera from 0-100"""
        if not camera or camera == 'Not specified':
            return 50
        
        camera_lower = camera.lower()
        score = 40  # Base score
        
        # Main camera MP
        mp_matches = re.findall(r'(\d+)\s*mp', camera_lower)
        if mp_matches:
            main_mp = max([int(mp) for mp in mp_matches])
            if main_mp >= 200:
                score += 35
            elif main_mp >= 108:
                score += 30
            elif main_mp >= 64:
                score += 25
            elif main_mp >= 50:
                score += 20
            elif main_mp >= 48:
                score += 15
        
        # Camera count
        if 'quad' in camera_lower:
            score += 15
        elif 'triple' in camera_lower:
            score += 12
        elif 'dual' in camera_lower:
            score += 8
        
        return min(score, 100)
    
    def extract_battery_score(self, battery: str) -> float:
        """Score battery from 0-100"""
        if not battery or battery == 'Not specified':
            return 50
        
        battery_lower = battery.lower()
        score = 40  # Base score
        
        # Battery capacity
        capacity_match = re.search(r'(\d+)\s*mah', battery_lower)
        if capacity_match:
            capacity = int(capacity_match.group(1))
            if capacity >= 6000:
                score += 35
            elif capacity >= 5500:
                score += 30
            elif capacity >= 5000:
                score += 25
            elif capacity >= 4500:
                score += 20
            elif capacity >= 4000:
                score += 15
        
        # Charging speed
        charging_match = re.search(r'(\d+)w', battery_lower)
        if charging_match:
            charging = int(charging_match.group(1))
            if charging >= 100:
                score += 25
            elif charging >= 80:
                score += 20
            elif charging >= 60:
                score += 15
            elif charging >= 40:
                score += 10
        
        return min(score, 100)
    
    def extract_storage_score(self, storage: str) -> float:
        """Score storage from 0-100 with proper unit handling (KB, MB, GB, TB)"""
        if not storage or storage == 'Not specified':
            return 50
        
        storage_lower = storage.lower()
        score = 30  # Base score
        
        # Helper function to convert storage to GB
        def convert_to_gb(value: float, unit: str) -> float:
            unit = unit.lower()
            if 'tb' in unit:
                return value * 1024  # 1 TB = 1024 GB
            elif 'gb' in unit:
                return value
            elif 'mb' in unit:
                return value / 1024  # 1 GB = 1024 MB
            elif 'kb' in unit:
                return value / (1024 * 1024)  # 1 GB = 1024*1024 KB
            return value  # Assume GB if no unit
        
        # Extract storage capacity with unit handling
        storage_match = re.search(r'(\d+)\s*(tb|gb|mb|kb)?(?:\s*(?:inbuilt|storage|rom))?', storage_lower)
        if storage_match:
            storage_value = int(storage_match.group(1))
            storage_unit = storage_match.group(2) or 'gb'  # Default to GB
            storage_gb = convert_to_gb(storage_value, storage_unit)
            
            if storage_gb >= 1024:  # 1 TB or more
                score += 40
            elif storage_gb >= 512:
                score += 40
            elif storage_gb >= 256:
                score += 35
            elif storage_gb >= 128:
                score += 25
            elif storage_gb >= 64:
                score += 15
            elif storage_gb >= 32:
                score += 10
            elif storage_gb >= 16:
                score += 5
            # Less than 16 GB (or MB values) gets no bonus
        
        # RAM bonus (if mentioned) with unit handling
        ram_match = re.search(r'(\d+)\s*(tb|gb|mb|kb)?\s*ram', storage_lower)
        if ram_match:
            ram_value = int(ram_match.group(1))
            ram_unit = ram_match.group(2) or 'gb'  # Default to GB
            ram_gb = convert_to_gb(ram_value, ram_unit)
            
            if ram_gb >= 12:
                score += 30
            elif ram_gb >= 8:
                score += 20
            elif ram_gb >= 6:
                score += 10
            elif ram_gb >= 4:
                score += 5
            # Less than 4 GB RAM gets no bonus
        
        return min(score, 100)
    
    def extract_connectivity_score(self, connectivity: str) -> float:
        """Score connectivity from 0-100"""
        if not connectivity or connectivity == 'Not specified':
            return 60  # Assume basic connectivity
        
        connectivity_lower = connectivity.lower()
        score = 40
        
        if '5g' in connectivity_lower:
            score += 30
        elif '4g' in connectivity_lower or 'lte' in connectivity_lower:
            score += 20
        
        if 'wi-fi' in connectivity_lower or 'wifi' in connectivity_lower:
            score += 15
        if 'nfc' in connectivity_lower:
            score += 10
        if 'bluetooth' in connectivity_lower:
            score += 5
        
        return min(score, 100)
    
    def calculate_overall_cpi(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall CPI score"""
        overall = (
            scores['processor'] * 0.25 +
            scores['display'] * 0.20 +
            scores['camera'] * 0.20 +
            scores['battery'] * 0.15 +
            scores['storage'] * 0.15 +
            scores['connectivity'] * 0.05
        )
        return round(overall, 1)
    
    def calculate_price_value_ratio(self, price: float, overall_cpi: float) -> float:
        """Calculate price-to-value ratio"""
        if price <= 0:
            return 0
        # Higher CPI and lower price = better value
        ratio = (overall_cpi / (price / 1000)) * 10
        return round(min(ratio, 100), 1)
    
    def get_cpi_badge(self, overall_cpi: float) -> Dict[str, str]:
        """Get badge info based on CPI score"""
        if overall_cpi >= 85:
            return {'label': 'Flagship', 'color': '#9333ea'}
        elif overall_cpi >= 75:
            return {'label': 'Premium', 'color': '#3b82f6'}
        elif overall_cpi >= 65:
            return {'label': 'Mid-Range', 'color': '#10b981'}
        elif overall_cpi >= 55:
            return {'label': 'Budget', 'color': '#f59e0b'}
        else:
            return {'label': 'Entry', 'color': '#6b7280'}
    
    def calculate_cpi(self, specs: Dict[str, str], price: float = 0) -> Dict:
        """
        Calculate complete CPI scores for a product
        
        Args:
            specs: Dict with keys: processor, battery, display, camera, connectivity, storage
            price: Product price (optional, for value ratio)
        
        Returns:
            Dict with all CPI scores and badge info
        """
        # Calculate individual scores
        scores = {
            'processor': self.extract_processor_score(specs.get('processor', '')),
            'display': self.extract_display_score(specs.get('display', '')),
            'camera': self.extract_camera_score(specs.get('camera', '')),
            'battery': self.extract_battery_score(specs.get('battery', '')),
            'storage': self.extract_storage_score(specs.get('storage', '')),
            'connectivity': self.extract_connectivity_score(specs.get('connectivity', ''))
        }
        
        # Calculate overall CPI
        overall_cpi = self.calculate_overall_cpi(scores)
        
        # Calculate price-value ratio
        price_value_ratio = self.calculate_price_value_ratio(price, overall_cpi)
        
        # Get badge
        badge = self.get_cpi_badge(overall_cpi)
        
        return {
            'scores': {
                'processor': round(scores['processor'], 1),
                'display': round(scores['display'], 1),
                'camera': round(scores['camera'], 1),
                'battery': round(scores['battery'], 1),
                'storage': round(scores['storage'], 1),
                'connectivity': round(scores['connectivity'], 1)
            },
            'overall_cpi': overall_cpi,
            'price_value_ratio': price_value_ratio,
            'badge': badge
        }
