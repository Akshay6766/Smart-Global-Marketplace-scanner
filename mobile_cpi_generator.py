"""
Mobile Phone CPI Generator - Creates comprehensive index with spec scores
"""

import pandas as pd
import json
import re
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class MobileCPIScore:
    processor_score: float = 0.0
    display_score: float = 0.0
    camera_score: float = 0.0
    battery_score: float = 0.0
    storage_score: float = 0.0
    connectivity_score: float = 0.0
    overall_cpi: float = 0.0
    price_value_ratio: float = 0.0


class MobileCPIGenerator:
    def __init__(self):
        self.processor_rankings = {
            'snapdragon 8 elite': 100,
            'snapdragon 8s gen4': 95,
            'dimensity 9300 plus': 92,
            'dimensity 9300': 85,
            'dimensity 8450': 82,
            'dimensity 8350': 80,
            'dimensity 7400': 75,
            'dimensity 7300': 72,
            'snapdragon 7s gen3': 70,
            'snapdragon 7s gen2': 68,
            'dimensity 6300': 60,
            'exynos 1380': 65,
        }
    
    def extract_processor_score(self, processor: str) -> float:
        processor_lower = processor.lower()
        
        # Find processor in rankings
        for proc_name, score in self.processor_rankings.items():
            if proc_name in processor_lower:
                return score
        
        # Default scoring
        if 'snapdragon' in processor_lower:
            return 70
        elif 'dimensity' in processor_lower:
            return 65
        elif 'exynos' in processor_lower:
            return 60
        return 50
    
    def extract_display_score(self, display: str) -> float:
        display_lower = display.lower()
        score = 60  # Base score
        
        # Resolution scoring
        if '2800' in display_lower or '2772' in display_lower:
            score += 25
        elif '2400' in display_lower or '2340' in display_lower:
            score += 20
        elif '1604' in display_lower or '1600' in display_lower:
            score += 10
        
        # Refresh rate scoring
        if '120 hz' in display_lower:
            score += 15
        elif '90 hz' in display_lower:
            score += 10
        
        return min(score, 100)
    
    def extract_camera_score(self, camera: str) -> float:
        camera_lower = camera.lower()
        score = 50  # Base score
        
        # Main camera MP
        main_mp_match = re.search(r'(\d+)\s*mp.*?rear', camera_lower)
        if main_mp_match:
            main_mp = int(main_mp_match.group(1))
            if main_mp >= 50:
                score += 25
            elif main_mp >= 48:
                score += 20
            elif main_mp >= 32:
                score += 15
        
        # Camera count
        if 'triple' in camera_lower:
            score += 15
        elif 'dual' in camera_lower:
            score += 10
        
        # Front camera
        front_mp_match = re.search(r'(\d+)\s*mp.*?front', camera_lower)
        if front_mp_match:
            front_mp = int(front_mp_match.group(1))
            if front_mp >= 32:
                score += 10
            elif front_mp >= 20:
                score += 5
        
        return min(score, 100)
    
    def extract_battery_score(self, battery: str) -> float:
        battery_lower = battery.lower()
        score = 50  # Base score
        
        # Battery capacity
        capacity_match = re.search(r'(\d+)\s*mah', battery_lower)
        if capacity_match:
            capacity = int(capacity_match.group(1))
            if capacity >= 6000:
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
            if charging >= 80:
                score += 20
            elif charging >= 60:
                score += 15
            elif charging >= 40:
                score += 10
        
        return min(score, 100)
    
    def extract_storage_score(self, storage: str) -> float:
        storage_lower = storage.lower()
        score = 40  # Base score
        
        # RAM
        ram_match = re.search(r'(\d+)\s*gb\s*ram', storage_lower)
        if ram_match:
            ram = int(ram_match.group(1))
            if ram >= 12:
                score += 30
            elif ram >= 8:
                score += 25
            elif ram >= 6:
                score += 20
            elif ram >= 4:
                score += 15
        
        # Storage
        storage_match = re.search(r'(\d+)\s*gb\s*inbuilt', storage_lower)
        if storage_match:
            storage_gb = int(storage_match.group(1))
            if storage_gb >= 512:
                score += 30
            elif storage_gb >= 256:
                score += 25
            elif storage_gb >= 128:
                score += 20
        
        return min(score, 100)
    
    def extract_connectivity_score(self, connectivity: str) -> float:
        connectivity_lower = connectivity.lower()
        score = 50
        
        if '5g' in connectivity_lower:
            score += 25
        elif '4g' in connectivity_lower:
            score += 15
        
        if 'wi-fi' in connectivity_lower:
            score += 10
        if 'nfc' in connectivity_lower:
            score += 10
        if 'ir blaster' in connectivity_lower:
            score += 5
        
        return min(score, 100)
    
    def calculate_price_value_ratio(self, price: float, overall_cpi: float) -> float:
        if price <= 0:
            return 0
        return min((overall_cpi / (price / 1000)) * 10, 100)
    
    def generate_search_keywords(self, name: str, processor: str, price: float) -> List[str]:
        keywords = []
        
        # Name components
        name_words = name.lower().split()
        keywords.extend(name_words)
        
        # Processor keywords
        processor_words = processor.lower().split()
        keywords.extend([word for word in processor_words if len(word) > 2])
        
        # Price range keywords
        if price < 15000:
            keywords.extend(['budget', 'affordable'])
        elif price < 30000:
            keywords.extend(['mid-range', 'value'])
        elif price < 50000:
            keywords.extend(['premium', 'flagship'])
        else:
            keywords.extend(['ultra-premium', 'luxury'])
        
        return list(set(keywords))
    
    def process_mobile_data(self, csv_file: str):
        print(" Processing mobile phone data...")
        df = pd.read_csv(csv_file)
        
        mobile_index = []
        
        for idx, row in df.iterrows():
            try:
                # Calculate CPI scores
                processor_score = self.extract_processor_score(row['processor'])
                display_score = self.extract_display_score(row['display'])
                camera_score = self.extract_camera_score(row['camera'])
                battery_score = self.extract_battery_score(row['battery'])
                storage_score = self.extract_storage_score(row['storage'])
                connectivity_score = self.extract_connectivity_score(row['sim'])
                
                # Overall CPI (weighted average)
                overall_cpi = (
                    processor_score * 0.25 +
                    display_score * 0.20 +
                    camera_score * 0.20 +
                    battery_score * 0.15 +
                    storage_score * 0.15 +
                    connectivity_score * 0.05
                )
                
                price_value_ratio = self.calculate_price_value_ratio(row['price'], overall_cpi)
                
                # Create entry
                cpi_scores = MobileCPIScore(
                    processor_score=round(processor_score, 1),
                    display_score=round(display_score, 1),
                    camera_score=round(camera_score, 1),
                    battery_score=round(battery_score, 1),
                    storage_score=round(storage_score, 1),
                    connectivity_score=round(connectivity_score, 1),
                    overall_cpi=round(overall_cpi, 1),
                    price_value_ratio=round(price_value_ratio, 1)
                )
                
                search_keywords = self.generate_search_keywords(
                    row['Name'], row['processor'], row['price']
                )
                
                mobile_entry = {
                    'name': row['Name'],
                    'brand': row['Name'].split()[0],
                    'price': float(row['price']),
                    'rating': float(row['rating']),
                    'spec_score': float(row['Spec Score']),
                    'image_url': row['img'],
                    'tag': row['tag'],
                    'processor': row['processor'],
                    'storage': row['storage'],
                    'battery': row['battery'],
                    'display': row['display'],
                    'camera': row['camera'],
                    'connectivity': row['sim'],
                    'cpi_scores': asdict(cpi_scores),
                    'search_keywords': search_keywords
                }
                
                mobile_index.append(mobile_entry)
                
                if (idx + 1) % 100 == 0:
                    print(f"   Processed {idx + 1} phones...")
                    
            except Exception as e:
                print(f"  Error processing {row.get('Name', 'Unknown')}: {e}")
                continue
        
        print(f" Processed {len(mobile_index)} mobile phones")
        return mobile_index
    
    def save_index_files(self, mobile_index: List[Dict]):
        print(" Saving mobile phone index files...")
        
        # Complete index
        with open('mobile_phone_index_complete.json', 'w', encoding='utf-8') as f:
            json.dump(mobile_index, f, indent=2, ensure_ascii=False)
        
        # CPI-focused index for web app
        cpi_index = []
        for phone in mobile_index:
            cpi_entry = {
                'name': phone['name'],
                'brand': phone['brand'],
                'price': phone['price'],
                'rating': phone['rating'],
                'image_url': phone['image_url'],
                'tag': phone['tag'],
                'cpi_scores': phone['cpi_scores'],
                'search_keywords': phone['search_keywords'],
                'specs_summary': {
                    'processor': phone['processor'],
                    'storage': phone['storage'],
                    'battery': phone['battery'],
                    'display': phone['display'],
                    'camera': phone['camera']
                }
            }
            cpi_index.append(cpi_entry)
        
        with open('mobile_cpi_index.json', 'w', encoding='utf-8') as f:
            json.dump(cpi_index, f, indent=2, ensure_ascii=False)
        
        print(" Index files saved:")
        print("    mobile_phone_index_complete.json")
        print("    mobile_cpi_index.json")


def main():
    print(" Mobile Phone CPI Index Generator")
    print("="*50)
    
    generator = MobileCPIGenerator()
    mobile_index = generator.process_mobile_data('mobiles_2025.csv')
    generator.save_index_files(mobile_index)
    
    print("\n Mobile phone CPI index generation complete!")


if __name__ == "__main__":
    main()
