"""
AI-Powered Product Discovery & Comparison Engine
Searches multiple sources, ranks by price, seller trust, and quality
"""

import asyncio
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import re


@dataclass
class ProductHit:
    """Represents a single product finding"""
    title: str
    price: float
    currency: str
    url: str
    source: str
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    product_rating: Optional[float] = None
    review_count: int = 0
    image_url: Optional[str] = None
    description: Optional[str] = None
    
    # Computed scores
    trust_score: float = 0.0
    quality_score: float = 0.0
    value_score: float = 0.0
    overall_rank: float = 0.0


class ProductSearchEngine:
    """Main engine for product discovery"""
    
    def __init__(self):
        self.sources = [
            'amazon', 'ebay', 'walmart', 'etsy', 
            'aliexpress', 'target', 'bestbuy'
        ]
    
    async def search(self, query: str, max_results: int = 50) -> List[ProductHit]:
        """
        Search for products across multiple sources
        
        Args:
            query: Vague or specific product description
            max_results: Maximum number of results to return
        """
        print(f"🔍 Searching for: '{query}'")
        print(f"📡 Scanning sources: {', '.join(self.sources)}\n")
        
        # Enhance query with AI understanding
        enhanced_query = self._enhance_query(query)
        print(f"🤖 Enhanced query: '{enhanced_query}'\n")
        
        # Search all sources concurrently
        tasks = [
            self._search_source(source, enhanced_query) 
            for source in self.sources
        ]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_hits = [hit for source_hits in results for hit in source_hits]
        
        # Calculate scores and rank
        ranked_hits = self._rank_products(all_hits)
        
        return ranked_hits[:max_results]
    
    def _enhance_query(self, query: str) -> str:
        """Use AI to understand vague descriptions and enhance query"""
        # Simulate AI query enhancement
        # In production, use OpenAI/Claude API for better understanding
        
        enhancements = {
            'laptop': 'laptop computer notebook',
            'phone': 'smartphone mobile phone',
            'headphones': 'headphones earphones audio',
            'watch': 'watch smartwatch timepiece',
            'shoes': 'shoes sneakers footwear',
            'bag': 'bag backpack handbag',
            'camera': 'camera digital photography',
        }
        
        query_lower = query.lower()
        for key, enhanced in enhancements.items():
            if key in query_lower:
                return enhanced
        
        return query
    
    async def _search_source(self, source: str, query: str) -> List[ProductHit]:
        """Search a specific marketplace source"""
        # Simulate API calls with realistic data
        await asyncio.sleep(0.5)  # Simulate network delay
        
        # Mock data generation (in production, use real APIs/scraping)
        return self._generate_mock_results(source, query)
    
    def _generate_mock_results(self, source: str, query: str) -> List[ProductHit]:
        """Generate realistic mock product data"""
        import random
        
        results = []
        num_results = random.randint(3, 8)
        
        for i in range(num_results):
            price = round(random.uniform(29.99, 599.99), 2)
            
            hit = ProductHit(
                title=f"{query.title()} - {source.title()} Listing #{i+1}",
                price=price,
                currency="USD",
                url=f"https://{source}.com/product/{random.randint(10000, 99999)}",
                source=source.title(),
                seller_name=f"Seller_{random.randint(1000, 9999)}",
                seller_rating=round(random.uniform(3.5, 5.0), 1),
                product_rating=round(random.uniform(3.0, 5.0), 1),
                review_count=random.randint(10, 5000),
                image_url=f"https://placeholder.com/300x300?text={source}",
                description=f"High quality {query} from trusted {source} seller"
            )
            results.append(hit)
        
        return results
    
    def _rank_products(self, hits: List[ProductHit]) -> List[ProductHit]:
        """Calculate scores and rank products"""
        if not hits:
            return []
        
        # Calculate individual scores
        for hit in hits:
            hit.trust_score = self._calculate_trust_score(hit)
            hit.quality_score = self._calculate_quality_score(hit)
            hit.value_score = self._calculate_value_score(hit, hits)
            hit.overall_rank = self._calculate_overall_rank(hit)
        
        # Sort by overall rank (descending)
        ranked = sorted(hits, key=lambda x: x.overall_rank, reverse=True)
        
        return ranked
    
    def _calculate_trust_score(self, hit: ProductHit) -> float:
        """Calculate seller trustworthiness score (0-100)"""
        score = 0.0
        
        # Seller rating contribution (40%)
        if hit.seller_rating:
            score += (hit.seller_rating / 5.0) * 40
        
        # Review count contribution (30%)
        if hit.review_count > 0:
            # Logarithmic scale for review count
            import math
            review_score = min(math.log10(hit.review_count + 1) / 4, 1.0)
            score += review_score * 30
        
        # Source reputation (30%)
        source_trust = {
            'Amazon': 0.95, 'Walmart': 0.90, 'Target': 0.90,
            'BestBuy': 0.88, 'Ebay': 0.75, 'Etsy': 0.80,
            'AliExpress': 0.65
        }
        score += source_trust.get(hit.source, 0.5) * 30
        
        return round(score, 2)
    
    def _calculate_quality_score(self, hit: ProductHit) -> float:
        """Calculate product quality score (0-100)"""
        score = 0.0
        
        # Product rating (60%)
        if hit.product_rating:
            score += (hit.product_rating / 5.0) * 60
        
        # Number of reviews indicates reliability (40%)
        if hit.review_count > 0:
            import math
            review_reliability = min(math.log10(hit.review_count + 1) / 4, 1.0)
            score += review_reliability * 40
        
        return round(score, 2)
    
    def _calculate_value_score(self, hit: ProductHit, all_hits: List[ProductHit]) -> float:
        """Calculate value for money score (0-100)"""
        prices = [h.price for h in all_hits if h.price > 0]
        if not prices:
            return 50.0
        
        min_price = min(prices)
        max_price = max(prices)
        
        if max_price == min_price:
            return 50.0
        
        # Lower price = higher value score
        # Normalize to 0-100 scale (inverted)
        normalized = (hit.price - min_price) / (max_price - min_price)
        value_score = (1 - normalized) * 100
        
        return round(value_score, 2)
    
    def _calculate_overall_rank(self, hit: ProductHit) -> float:
        """Calculate weighted overall ranking score"""
        # Weighted combination
        weights = {
            'trust': 0.30,
            'quality': 0.35,
            'value': 0.35
        }
        
        overall = (
            hit.trust_score * weights['trust'] +
            hit.quality_score * weights['quality'] +
            hit.value_score * weights['value']
        )
        
        return round(overall, 2)


class ResultsPresenter:
    """Format and display search results"""
    
    @staticmethod
    def display_results(hits: List[ProductHit], show_detailed: bool = False):
        """Display ranked product results"""
        if not hits:
            print("❌ No results found")
            return
        
        print(f"\n{'='*100}")
        print(f"📊 FOUND {len(hits)} PRODUCTS - RANKED BY OVERALL SCORE")
        print(f"{'='*100}\n")
        
        for idx, hit in enumerate(hits, 1):
            ResultsPresenter._display_product(idx, hit, show_detailed)
    
    @staticmethod
    def _display_product(rank: int, hit: ProductHit, detailed: bool):
        """Display single product result"""
        # Rank badge
        badge = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        
        print(f"{badge} RANK {rank} | Overall Score: {hit.overall_rank}/100")
        print(f"{'─'*100}")
        
        # Basic info
        print(f"📦 {hit.title}")
        print(f"💰 Price: ${hit.price:.2f} {hit.currency}")
        print(f"🏪 Source: {hit.source}")
        print(f"🔗 URL: {hit.url}")
        
        if hit.seller_name:
            print(f"👤 Seller: {hit.seller_name}")
        
        # Ratings
        if hit.product_rating:
            stars = '⭐' * int(hit.product_rating)
            print(f"⭐ Product Rating: {stars} {hit.product_rating}/5.0 ({hit.review_count} reviews)")
        
        if hit.seller_rating:
            stars = '⭐' * int(hit.seller_rating)
            print(f"👍 Seller Rating: {stars} {hit.seller_rating}/5.0")
        
        # Scores
        print(f"\n📈 SCORES:")
        print(f"   🛡️  Trust Score:   {ResultsPresenter._score_bar(hit.trust_score)} {hit.trust_score}/100")
        print(f"   ✨ Quality Score: {ResultsPresenter._score_bar(hit.quality_score)} {hit.quality_score}/100")
        print(f"   💎 Value Score:   {ResultsPresenter._score_bar(hit.value_score)} {hit.value_score}/100")
        
        if detailed and hit.description:
            print(f"\n📝 {hit.description}")
        
        print(f"\n{'='*100}\n")
    
    @staticmethod
    def _score_bar(score: float, width: int = 20) -> str:
        """Create visual score bar"""
        filled = int((score / 100) * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}]"
    
    @staticmethod
    def export_json(hits: List[ProductHit], filename: str = "search_results.json"):
        """Export results to JSON"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_results': len(hits),
            'products': [asdict(hit) for hit in hits]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results exported to {filename}")
    
    @staticmethod
    def export_csv(hits: List[ProductHit], filename: str = "search_results.csv"):
        """Export results to CSV"""
        import csv
        
        if not hits:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(hits[0]).keys())
            writer.writeheader()
            for hit in hits:
                writer.writerow(asdict(hit))
        
        print(f"✅ Results exported to {filename}")


async def main():
    """Main execution"""
    print("\n" + "="*100)
    print("🤖 AI-POWERED PRODUCT DISCOVERY ENGINE")
    print("="*100 + "\n")
    
    # Initialize engine
    engine = ProductSearchEngine()
    presenter = ResultsPresenter()
    
    # Example searches
    queries = [
        "wireless headphones with noise cancellation",
        # "laptop for programming",
        # "running shoes"
    ]
    
    for query in queries:
        # Search
        results = await engine.search(query, max_results=10)
        
        # Display
        presenter.display_results(results, show_detailed=False)
        
        # Export
        presenter.export_json(results, f"results_{query.replace(' ', '_')[:30]}.json")
        presenter.export_csv(results, f"results_{query.replace(' ', '_')[:30]}.csv")
        
        print("\n" + "="*100 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
