# -*- coding: utf-8 -*-
"""
Geo-Location Aware Product Search Engine
Automatically searches country-specific marketplaces
"""

import asyncio
import random
from typing import List, Optional
from dataclasses import dataclass
from smart_product_finder import ProductHit, ResultsPresenter
from geo_marketplace_config import GeoMarketplaceConfig, Marketplace
from gemini_search import GeminiProductSearch
from serpapi_search import SerpAPISearch

# Real web scraping imports


class GeoProductSearchEngine:
    """Product search engine with geo-location awareness"""
    
    def __init__(self, country_code: Optional[str] = None, auto_detect: bool = True):
        """
        Initialize geo-aware search engine
        
        Args:
            country_code: ISO country code (e.g., 'IN', 'US'). If None, auto-detect
            auto_detect: If True, automatically detect country from IP
        """
        if country_code:
            self.country_code = country_code.upper()
        elif auto_detect:
            self.country_code = self._detect_country()
        else:
            self.country_code = 'US'  # Default
        
        # Get marketplaces for this country
        self.marketplaces = GeoMarketplaceConfig.get_marketplaces_for_country(
            self.country_code, 
            popular_only=True
        )
        
        if not self.marketplaces:
            print(f"??  No marketplaces found for {self.country_code}, using US defaults")
            self.country_code = 'US'
            self.marketplaces = GeoMarketplaceConfig.get_marketplaces_for_country('US')
        
        # Get currency info
        self.currency = self.marketplaces[0].currency
        self.currency_symbol = GeoMarketplaceConfig.get_currency_symbol(self.currency)
        self.country_name = self.marketplaces[0].country_name
        
        # Initialize Gemini AI search (primary method)
        self.gemini_search = GeminiProductSearch()
        self.serpapi_search = SerpAPISearch()
    
    def _detect_country(self) -> str:
        """Detect user's country from IP address"""
        # In production, use GeoIP service
        # For now, return default
        return GeoMarketplaceConfig.detect_country_from_ip()
    
    async def search(self, query: str, max_results: int = 50, budget: float = None) -> List[ProductHit]:
        """
        Search for products in country-specific marketplaces
        
        Args:
            query: Product search query
            max_results: Maximum number of results
        """
        print(f"\n?? Searching in: {self.country_name} ({self.country_code})")
        print(f"?? Currency: {self.currency} ({self.currency_symbol})")
        print(f"?? Query: '{query}'")
        print(f"?? Scanning {len(self.marketplaces)} local marketplaces...\n")
        
        # Display marketplaces being searched
        for marketplace in self.marketplaces:
            print(f"   � {marketplace.name} ({marketplace.domain})")
        print()
        
        # Search all marketplaces concurrently
        tasks = [
            self._search_marketplace(marketplace, query, budget) 
            for marketplace in self.marketplaces
        ]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_hits = [hit for marketplace_hits in results for hit in marketplace_hits]
        
        # Calculate scores and rank
        ranked_hits = self._rank_products(all_hits)
        
        print(f"? Found {len(ranked_hits)} products across all marketplaces\n")
        
        return ranked_hits[:max_results]
    
    async def _search_marketplace(self, marketplace: Marketplace, query: str, budget: float = None) -> List[ProductHit]:
        """Search using ONLY Gemini AI - no mock data, no other APIs"""
        
        # Only call once for first marketplace (searches ALL marketplaces)
        if marketplace == self.marketplaces[0]:
            # METHOD 1: Try SerpAPI first (REAL URLs from Google Shopping)
            try:
                print(f" Searching with SerpAPI (Google Shopping)...")
                serpapi_results = await self.serpapi_search.search_products(
                    query=query,
                    country=self.country_name,
                    max_results=15,
                    budget=budget,
                    # currency=self.currency
                )
                if serpapi_results:
                    print(f" SerpAPI found {len(serpapi_results)} REAL products")
                    return serpapi_results
            except Exception as e:
                print(f"  SerpAPI failed: {e}")
            
            # METHOD 2: Fallback to Gemini AI
            try:
                print(f" Falling back to Gemini AI...")
                gemini_results = await self.gemini_search.search_products(
                    query=query,
                    country=self.country_name,
                    max_results=15,
                    budget=budget,
                    # currency=self.currency
                )
                if gemini_results:
                    print(f" Gemini AI found {len(gemini_results)} REAL products")
                    return gemini_results
                else:
                    print(f"  Gemini AI returned no results")
                    return []
            except Exception as e:
                print(f" Gemini AI error: {e}")
                return []
        
        # For other marketplaces, return empty (Gemini already searched all)
        return []

    def _generate_mock_results(self, marketplace: Marketplace, query: str) -> List[ProductHit]:
        """Generate realistic mock product data for marketplace"""
        results = []
        num_results = random.randint(2, 6)
        
        price_ranges = {
            'INR': (500, 50000), 'USD': (10, 1000), 'GBP': (10, 800), 'EUR': (10, 900),
            'CAD': (15, 1200), 'AUD': (15, 1200), 'JPY': (1000, 100000), 'CNY': (50, 5000),
            'AED': (50, 4000), 'SGD': (15, 1500), 'BRL': (50, 5000), 'MXN': (200, 20000),
        }
        
        min_price, max_price = price_ranges.get(marketplace.currency, (10, 1000))
        
        # More realistic brand variations
        brands = ['TechPro', 'SmartChoice', 'Premium', 'Elite', 'ProMax', 'UltraFit', 'NextGen', 'PowerPlus', 'MaxCore', 'SwiftTech']
        models = ['Pro', 'Plus', 'Ultra', 'Max', 'Elite', 'Prime', 'Advance', 'Premium', 'X', 'XL']
        colors = ['Black', 'White', 'Silver', 'Blue', 'Red', 'Gray', 'Gold', 'Rose Gold']
        specs = ['64GB', '128GB', '256GB', '512GB', '8GB RAM', '16GB RAM', '32GB', 'WiFi', '5G', '4K', 'HD', 'FHD']
        
        features_pool = ['Premium quality', 'Advanced tech', 'Ergonomic design', 'Durable', 'Energy efficient', 'Easy to use', 'Portable', 'Professional', 'Latest model', 'Best performance', 'Warranty', 'Fast shipping']
        
        # Product-specific image URLs (using placeholder.com with product-relevant text)
        query_lower = query.lower()
        image_category = 'product'
        if 'phone' in query_lower or 'mobile' in query_lower:
            image_category = 'smartphone'
        elif 'laptop' in query_lower or 'computer' in query_lower:
            image_category = 'laptop'
        elif 'headphone' in query_lower or 'earphone' in query_lower or 'earbud' in query_lower:
            image_category = 'headphones'
        elif 'watch' in query_lower:
            image_category = 'smartwatch'
        elif 'camera' in query_lower:
            image_category = 'camera'
        elif 'tablet' in query_lower:
            image_category = 'tablet'
        elif 'mouse' in query_lower:
            image_category = 'mouse'
        elif 'keyboard' in query_lower:
            image_category = 'keyboard'
        
        for i in range(num_results):
            price = round(random.uniform(min_price, max_price), 2)
            brand = random.choice(brands)
            model = random.choice(models)
            product_rating = round(random.uniform(3.5, 5.0), 1)
            seller_rating = round(random.uniform(3.5, 5.0), 1)
            review_count = random.randint(50, 5000)
            
            # Create more varied, realistic titles
            title_variations = [
                f"{brand} {query.title()} {model}",
                f"{brand} {query.title()} {model} - {random.choice(colors)}",
                f"{brand} {model} {query.title()} ({random.choice(specs)})",
                f"{query.title()} {brand} {model} {random.choice(specs)}",
                f"{brand} {query.title()} - {model} Series {random.choice(colors)}"
            ]
            title = random.choice(title_variations)
            
            # More realistic descriptions
            selected_features = random.sample(features_pool, k=random.randint(3, 5))
            description = f"High-quality {query} from {brand}. Features: {', '.join(selected_features)}. Perfect for daily use with excellent performance and reliability."
            
            # Use placeholder.com with product category text for more relevant images
            image_url = f"https://via.placeholder.com/400x400/4A90E2/FFFFFF?text={image_category.replace(' ', '+')}"
            
            hit = ProductHit(
                name=title,
                price=price,
                
                url=f"https://{marketplace.domain}/product/{random.randint(10000, 99999)}",
                
                
                
                
                image_url=image_url,
                description=description
            )
            
            reasons = []
            if product_rating >= 4.5:
                reasons.append(f"Highly rated ({product_rating}/5.0)")
            if review_count >= 1000:
                reasons.append(f"Trusted by {review_count:,} customers")
            if seller_rating >= 4.5:
                reasons.append(f"Reliable seller ({seller_rating}/5.0)")
            if marketplace.trust_score >= 0.9:
                reasons.append(f"Verified {marketplace.name} seller")
            if price <= (min_price + (max_price - min_price) * 0.3):
                reasons.append("Great value for money")
            elif price >= (min_price + (max_price - min_price) * 0.7):
                reasons.append("Premium quality product")
            
            hit.best_choice_reason = "  ".join(reasons) if reasons else "Quality product from trusted marketplace"
            results.append(hit)
        
        return results


    def _rank_products(self, hits: List[ProductHit]) -> List[ProductHit]:
        """Calculate scores and rank products"""
        if not hits:
            return []
        
        # Pass budget to all hits FIRST
        budget = getattr(self, 'current_budget', None)
        print(f" Setting budget on {len(hits)} products: {budget}")
        for hit in hits:
            hit.search_budget = budget
        
        # Then calculate individual scores
        for hit in hits:
            hit.trust_score = self._calculate_trust_score(hit)
            hit.quality_score = self._calculate_quality_score(hit)
            hit.value_score = self._calculate_value_score(hit, hits)
            hit.overall_rank = self._calculate_overall_rank(hit)
        
        # Sort by overall rank (descending)
        # Best value products now rank at TOP due to 50% value weight
        ranked = sorted(hits, key=lambda x: x.overall_rank, reverse=True)
        
        return ranked
    
    def _calculate_trust_score(self, hit: ProductHit) -> float:
        """Calculate seller trustworthiness score"""
        score = 0.0
        
        # Seller rating (40%)
        if hit.rating:
            score += (hit.rating / 5.0) * 40
        
        # Review count (30%)
        if hit.reviews_count > 0:
            import math
            review_score = min(math.log10(hit.reviews_count + 1) / 4, 1.0)
            score += review_score * 30
        
        # Marketplace trust (30%)
        marketplace = GeoMarketplaceConfig.get_marketplace_info(
            hit.url.split('/')[2] if '/' in hit.url else ''
        )
        if marketplace:
            score += marketplace.trust_score * 30
        else:
            score += 0.7 * 30  # Default trust
        
        return round(score, 2)
    
    def _calculate_quality_score(self, hit: ProductHit) -> float:
        """Calculate product quality score"""
        score = 0.0
        
        # Product rating (60%)
        if hit.rating:
            score += (hit.rating / 5.0) * 60
        
        # Review reliability (40%)
        if hit.reviews_count > 0:
            import math
            review_reliability = min(math.log10(hit.reviews_count + 1) / 4, 1.0)
            score += review_reliability * 40
        
        return round(score, 2)
    
    def _calculate_value_score(self, hit: ProductHit, all_hits: List[ProductHit]) -> float:
        """Calculate value with TIER-BASED QUALITY EXPECTATIONS"""
        same_currency_hits = [h for h in all_hits if h.currency == hit.currency]
        
        if len(same_currency_hits) < 2:
            return 50.0
        
        prices = [h.price for h in same_currency_hits if h.price > 0]
        if not prices:
            return 50.0
        
        min_price = min(prices)
        max_price = max(prices)
        
        if max_price == min_price:
            return 50.0
        
        rating = hit.rating or 4.0
        budget = getattr(hit, 'search_budget', None)
        
        if budget and budget > 0:
            # TIER-BASED QUALITY EXPECTATIONS
            # Higher budget = Higher quality expectations
            
            # Define quality tiers based on budget
            if budget >= 20000:
                # Premium tier: Expect 4.5+ rating
                min_expected_rating = 4.5
                tier = "Premium"
            elif budget >= 15000:
                # Mid-high tier: Expect 4.3+ rating
                min_expected_rating = 4.3
                tier = "Mid-High"
            elif budget >= 10000:
                # Mid tier: Expect 4.0+ rating
                min_expected_rating = 4.0
                tier = "Mid"
            else:
                # Budget tier: Expect 3.8+ rating
                min_expected_rating = 3.8
                tier = "Budget"
            
            # Check if product meets tier expectations
            meets_expectations = rating >= min_expected_rating
            
            # Price positioning score - FAVOR UNDER BUDGET
            budget_utilization = hit.price / budget
            
            if budget_utilization <= 0.85:
                # BEST: Under budget (up to 85% of budget)
                # Lower price = higher score
                price_score = 100 - (budget_utilization * 15)  # 100 at 0%, 87 at 85%
            elif 0.85 < budget_utilization <= 1.0:
                # Good: 85-100% of budget (close to budget)
                price_score = 90
            elif budget_utilization < 0.7:
                # Very cheap - still good value
                price_score = 95
            elif 1.0 < budget_utilization <= 1.1:
                # Slightly over but acceptable
                price_score = 90
            else:
                # Way over budget
                price_score = 20
            
            # Quality expectation multiplier
            if meets_expectations:
                # Meets or exceeds tier expectations
                if rating >= min_expected_rating + 0.3:
                    quality_mult = 1.4  # Exceeds expectations!
                else:
                    quality_mult = 1.2  # Meets expectations
            else:
                # Below tier expectations - HEAVY PENALTY
                rating_gap = min_expected_rating - rating
                if rating_gap > 0.5:
                    quality_mult = 0.5  # Way below expectations
                else:
                    quality_mult = 0.7  # Slightly below
            
            value_score = price_score * quality_mult
            
        else:
            # No budget - traditional calculation
            normalized_price = (hit.price - min_price) / (max_price - min_price)
            price_score = (1 - normalized_price) * 100
            
            if rating >= 4.5:
                quality_mult = 1.3
            elif rating >= 4.0:
                quality_mult = 1.1
            else:
                quality_mult = 0.9
            
            value_score = price_score * quality_mult
        
        value_score = min(value_score, 100)
        return round(value_score, 2)
    
    def _calculate_overall_rank(self, hit: ProductHit) -> float:
        """Calculate weighted overall ranking score"""
        weights = {
            'trust': 0.20,
            'quality': 0.40,
            'value': 0.40
        }
        
        overall = (
            hit.trust_score * weights['trust'] +
            hit.quality_score * weights['quality'] +
            hit.value_score * weights['value']
        )
        
        return round(overall, 2)
    
    def get_location_info(self) -> dict:
        """Get current location configuration"""
        return {
            'country_code': self.country_code,
            'country_name': self.country_name,
            'currency': self.currency,
            'currency_symbol': self.currency_symbol,
            'marketplaces': [
                {
                    'name': m.name,
                    'domain': m.domain,
                    'trust_score': m.trust_score
                }
                for m in self.marketplaces
            ]
        }


async def demo_geo_search():
    """Demonstrate geo-aware search"""
    
    # Demo 1: Search in India
    print("\n" + "="*100)
    print("DEMO 1: SEARCHING IN INDIA")
    print("="*100)
    
    engine_india = GeoProductSearchEngine(country_code='IN')
    results_india = await engine_india.search("wireless headphones", max_results=10)
    
    presenter = ResultsPresenter()
    presenter.display_results(results_india[:5])
    
    # Demo 2: Search in US
    print("\n" + "="*100)
    print("DEMO 2: SEARCHING IN UNITED STATES")
    print("="*100)
    
    engine_us = GeoProductSearchEngine(country_code='US')
    results_us = await engine_us.search("wireless headphones", max_results=10)
    
    presenter.display_results(results_us[:5])
    
    # Demo 3: Search in UK
    print("\n" + "="*100)
    print("DEMO 3: SEARCHING IN UNITED KINGDOM")
    print("="*100)
    
    engine_uk = GeoProductSearchEngine(country_code='GB')
    results_uk = await engine_uk.search("wireless headphones", max_results=10)
    
    presenter.display_results(results_uk[:5])


if __name__ == "__main__":
    asyncio.run(demo_geo_search())

