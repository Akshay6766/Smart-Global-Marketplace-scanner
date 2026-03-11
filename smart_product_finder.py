
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import json

@dataclass
class ProductHit:
    """Represents a product search result"""

    # Core attributes
    name: str = ""
    title: str = ""
    price: float = 0.0
    currency: str = "INR"
    url: str = ""
    source: str = ""
    
    # Product details
    brand: str = ""
    image_url: str = ""
    description: str = ""
    specifications: Dict[str, Any] = None
    
    # Ratings and reviews
    rating: float = 0.0
    product_rating: float = 0.0
    reviews_count: int = 0
    review_count: int = 0
    
    # Seller information
    seller_name: str = ""
    seller_rating: float = 0.0
    
    # Calculated scores
    trust_score: float = 0.0
    quality_score: float = 0.0
    value_score: float = 0.0
    overall_rank: float = 0.0
    
    # Additional attributes
    best_choice_reason: str = ""
    is_best_value: bool = False
    search_budget: float = None
    
    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}
        # Sync name and title
        if not self.title and self.name:
            self.title = self.name
        if not self.name and self.title:
            self.name = self.title
        # Sync rating fields
        if not self.product_rating and self.rating:
            self.product_rating = self.rating
        if not self.rating and self.product_rating:
            self.rating = self.product_rating
        # Sync review count fields
        if not self.review_count and self.reviews_count:
            self.review_count = self.reviews_count
        if not self.reviews_count and self.review_count:
            self.reviews_count = self.review_count

class ResultsPresenter:
    """Formats and presents search results"""
    
    def __init__(self):
        pass
    
    def format_results(self, results: List[ProductHit]) -> List[Dict]:
        """Format results for API response"""
        return [
            {
                "name": hit.name,
                "title": hit.title,
                "price": hit.price,
                "currency": hit.currency,
                "url": hit.url,
                "source": hit.source,
                "brand": hit.brand,
                "image_url": hit.image_url,
                "description": hit.description,
                "specifications": hit.specifications,
                "rating": hit.rating,
                "product_rating": hit.product_rating,
                "reviews_count": hit.reviews_count,
                "review_count": hit.review_count,
                "seller_name": hit.seller_name,
                "seller_rating": hit.seller_rating,
                "trust_score": hit.trust_score,
                "quality_score": hit.quality_score,
                "value_score": hit.value_score,
                "overall_rank": hit.overall_rank,
                "best_choice_reason": hit.best_choice_reason,
                "is_best_value": hit.is_best_value,
                "search_budget": hit.search_budget
            }
            for hit in results
        ]
    
    def to_json(self, results: List[ProductHit]) -> str:
        """Convert results to JSON string"""
        formatted = self.format_results(results)
        return json.dumps(formatted, indent=2)

class ProductSearchEngine:
    """Basic product search engine"""
    
    def __init__(self):
        self.results_presenter = ResultsPresenter()
    
    def search(self, query: str, max_results: int = 20, **kwargs) -> List[ProductHit]:
        """Perform product search"""
        return []
    
    def get_product_details(self, product_id: str) -> Optional[ProductHit]:
        """Get detailed information for a specific product"""
        return None