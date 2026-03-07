"""
Intelligent Budget Advisor
Analyzes products within budget and suggests better deals
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from smart_product_finder import ProductHit


@dataclass
class BudgetAnalysis:
    """Budget analysis results"""
    budget: float
    currency: str
    within_budget: List[ProductHit]
    best_in_budget: Optional[ProductHit]
    avg_score_in_budget: float
    budget_quality: str  # 'excellent', 'good', 'fair', 'poor'
    
    # Recommendations
    has_better_deals: bool
    recommended_products: List[ProductHit]
    recommended_budget: Optional[float]
    savings_message: Optional[str]
    upgrade_message: Optional[str]


class BudgetAdvisor:
    """Intelligent budget analysis and recommendations"""
    
    # Score thresholds
    EXCELLENT_SCORE = 85
    GOOD_SCORE = 75
    FAIR_SCORE = 65
    POOR_SCORE = 50
    
    # Budget flexibility (how much above budget to consider)
    BUDGET_FLEXIBILITY = 0.40  # 40% above budget
    MIN_SCORE_IMPROVEMENT = 15  # Minimum score improvement to recommend
    
    def analyze_budget(
        self, 
        products: List[ProductHit], 
        budget: float,
        currency: str
    ) -> BudgetAnalysis:
        """
        Analyze products based on user's budget
        
        Args:
            products: List of all products
            budget: User's maximum budget
            currency: Currency code
        """
        # Filter products within budget
        within_budget = [p for p in products if p.price <= budget]
        
        # Calculate average score within budget
        avg_score = self._calculate_avg_score(within_budget)
        
        # Find best product within budget
        best_in_budget = max(within_budget, key=lambda x: x.overall_rank) if within_budget else None
        
        # Determine budget quality
        budget_quality = self._assess_budget_quality(avg_score, best_in_budget)
        
        # Check for better deals slightly above budget
        max_price = budget * (1 + self.BUDGET_FLEXIBILITY)
        above_budget = [p for p in products if budget < p.price <= max_price]
        
        # Find significantly better deals
        has_better_deals, recommended = self._find_better_deals(
            best_in_budget, 
            above_budget, 
            budget
        )
        
        # Generate recommendations
        recommended_budget = None
        savings_message = None
        upgrade_message = None
        
        if has_better_deals and recommended:
            recommended_budget = recommended[0].price
            upgrade_message = self._generate_upgrade_message(
                best_in_budget,
                recommended[0],
                budget,
                currency
            )
        
        # Check for savings opportunities
        if within_budget and len(within_budget) > 1:
            savings_message = self._generate_savings_message(
                within_budget,
                budget,
                currency
            )
        
        return BudgetAnalysis(
            budget=budget,
            currency=currency,
            within_budget=within_budget,
            best_in_budget=best_in_budget,
            avg_score_in_budget=avg_score,
            budget_quality=budget_quality,
            has_better_deals=has_better_deals,
            recommended_products=recommended,
            recommended_budget=recommended_budget,
            savings_message=savings_message,
            upgrade_message=upgrade_message
        )
    
    def _calculate_avg_score(self, products: List[ProductHit]) -> float:
        """Calculate average overall score"""
        if not products:
            return 0.0
        return sum(p.overall_rank for p in products) / len(products)
    
    def _assess_budget_quality(
        self, 
        avg_score: float, 
        best_product: Optional[ProductHit]
    ) -> str:
        """Assess quality of products within budget"""
        if not best_product:
            return 'none'
        
        best_score = best_product.overall_rank
        
        if best_score >= self.EXCELLENT_SCORE:
            return 'excellent'
        elif best_score >= self.GOOD_SCORE:
            return 'good'
        elif best_score >= self.FAIR_SCORE:
            return 'fair'
        else:
            return 'poor'
    
    def _find_better_deals(
        self,
        best_in_budget: Optional[ProductHit],
        above_budget: List[ProductHit],
        budget: float
    ) -> tuple[bool, List[ProductHit]]:
        """Find significantly better deals above budget"""
        if not best_in_budget or not above_budget:
            return False, []
        
        best_score = best_in_budget.overall_rank
        
        # Find products with significantly better scores
        better_deals = [
            p for p in above_budget
            if p.overall_rank >= best_score + self.MIN_SCORE_IMPROVEMENT
        ]
        
        # Sort by score (descending) and price (ascending)
        better_deals.sort(key=lambda x: (-x.overall_rank, x.price))
        
        # Return top 3 recommendations
        return len(better_deals) > 0, better_deals[:3]
    
    def _generate_upgrade_message(
        self,
        current_best: Optional[ProductHit],
        recommended: ProductHit,
        budget: float,
        currency: str
    ) -> str:
        """Generate upgrade recommendation message"""
        if not current_best:
            return ""
        
        price_diff = recommended.price - budget
        price_diff_percent = (price_diff / budget) * 100
        score_diff = recommended.overall_rank - current_best.overall_rank
        
        from geo_marketplace_config import GeoMarketplaceConfig
        symbol = GeoMarketplaceConfig.get_currency_symbol(currency)
        
        message = f"💡 **Smart Recommendation**: For just {symbol}{price_diff:.2f} more "
        message += f"({price_diff_percent:.0f}% above budget), you can get a product with "
        message += f"{score_diff:.0f} points higher score!\n\n"
        message += f"**Current Best in Budget**: {current_best.title}\n"
        message += f"   • Price: {symbol}{current_best.price:.2f}\n"
        message += f"   • Score: {current_best.overall_rank}/100\n\n"
        message += f"**Recommended Upgrade**: {recommended.title}\n"
        message += f"   • Price: {symbol}{recommended.price:.2f}\n"
        message += f"   • Score: {recommended.overall_rank}/100\n"
        message += f"   • Trust: {recommended.trust_score}/100 "
        message += f"| Quality: {recommended.quality_score}/100 "
        message += f"| Value: {recommended.value_score}/100"
        
        return message
    
    def _generate_savings_message(
        self,
        within_budget: List[ProductHit],
        budget: float,
        currency: str
    ) -> str:
        """Generate savings opportunity message"""
        # Find products with good scores well below budget
        budget_threshold = budget * 0.75  # 25% below budget
        good_deals = [
            p for p in within_budget
            if p.price <= budget_threshold and p.overall_rank >= self.GOOD_SCORE
        ]
        
        if not good_deals:
            return ""
        
        best_deal = max(good_deals, key=lambda x: x.overall_rank)
        savings = budget - best_deal.price
        savings_percent = (savings / budget) * 100
        
        from geo_marketplace_config import GeoMarketplaceConfig
        symbol = GeoMarketplaceConfig.get_currency_symbol(currency)
        
        message = f"💰 **Savings Opportunity**: You can save {symbol}{savings:.2f} "
        message += f"({savings_percent:.0f}%) and still get a great product!\n\n"
        message += f"**Best Value Deal**: {best_deal.title}\n"
        message += f"   • Price: {symbol}{best_deal.price:.2f}\n"
        message += f"   • Score: {best_deal.overall_rank}/100\n"
        message += f"   • You save: {symbol}{savings:.2f}"
        
        return message
    
    def get_budget_warning(self, analysis: BudgetAnalysis) -> Optional[Dict]:
        """Generate budget warning if needed"""
        if analysis.budget_quality == 'poor':
            return {
                'type': 'warning',
                'title': '⚠️ Low Quality Products in Budget',
                'message': f'Products within your budget have an average score of {analysis.avg_score_in_budget:.1f}/100. '
                          f'Consider increasing your budget for better quality options.',
                'severity': 'high'
            }
        elif analysis.budget_quality == 'fair':
            return {
                'type': 'info',
                'title': 'ℹ️ Fair Quality Products',
                'message': f'Products within your budget have an average score of {analysis.avg_score_in_budget:.1f}/100. '
                          f'You may find better options with a slightly higher budget.',
                'severity': 'medium'
            }
        elif analysis.budget_quality == 'none':
            return {
                'type': 'error',
                'title': '❌ No Products Found',
                'message': 'No products found within your budget. Try increasing your budget or searching for different products.',
                'severity': 'high'
            }
        
        return None
    
    def format_analysis_for_display(self, analysis: BudgetAnalysis) -> Dict:
        """Format analysis for web display"""
        from geo_marketplace_config import GeoMarketplaceConfig
        symbol = GeoMarketplaceConfig.get_currency_symbol(analysis.currency)
        
        result = {
            'budget': analysis.budget,
            'currency': analysis.currency,
            'currency_symbol': symbol,
            'products_in_budget': len(analysis.within_budget),
            'avg_score': round(analysis.avg_score_in_budget, 1),
            'budget_quality': analysis.budget_quality,
            'quality_label': self._get_quality_label(analysis.budget_quality),
            'quality_color': self._get_quality_color(analysis.budget_quality),
        }
        
        # Add best in budget
        if analysis.best_in_budget:
            result['best_in_budget'] = {
                'title': analysis.best_in_budget.title,
                'price': analysis.best_in_budget.price,
                'score': analysis.best_in_budget.overall_rank,
                'url': analysis.best_in_budget.url
            }
        
        # Add warning
        warning = self.get_budget_warning(analysis)
        if warning:
            result['warning'] = warning
        
        # Add recommendations
        if analysis.has_better_deals:
            result['has_recommendations'] = True
            result['upgrade_message'] = analysis.upgrade_message
            result['recommended_products'] = [
                {
                    'title': p.title,
                    'price': p.price,
                    'score': p.overall_rank,
                    'url': p.url,
                    'price_diff': p.price - analysis.budget,
                    'score_improvement': p.overall_rank - (analysis.best_in_budget.overall_rank if analysis.best_in_budget else 0)
                }
                for p in analysis.recommended_products
            ]
        
        # Add savings message
        if analysis.savings_message:
            result['savings_message'] = analysis.savings_message
        
        return result
    
    def _get_quality_label(self, quality: str) -> str:
        """Get human-readable quality label"""
        labels = {
            'excellent': '🌟 Excellent Deals',
            'good': '👍 Good Deals',
            'fair': '😐 Fair Deals',
            'poor': '⚠️ Limited Options',
            'none': '❌ No Options'
        }
        return labels.get(quality, 'Unknown')
    
    def _get_quality_color(self, quality: str) -> str:
        """Get color code for quality"""
        colors = {
            'excellent': '#10b981',  # Green
            'good': '#3b82f6',       # Blue
            'fair': '#f59e0b',       # Orange
            'poor': '#ef4444',       # Red
            'none': '#6b7280'        # Gray
        }
        return colors.get(quality, '#6b7280')


# Example usage
if __name__ == "__main__":
    print("Budget Advisor Module")
    print("=" * 60)
    print("\nThis module provides intelligent budget analysis:")
    print("• Analyzes products within budget")
    print("• Identifies quality of available options")
    print("• Recommends better deals slightly above budget")
    print("• Suggests savings opportunities")
    print("• Provides warnings for low-quality options")
