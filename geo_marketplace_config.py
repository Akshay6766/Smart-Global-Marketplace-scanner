"""
Geo-Location Based Marketplace Configuration
Automatically selects marketplaces based on user's country
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Marketplace:
    """Represents a marketplace with country-specific details"""
    name: str
    domain: str
    country_code: str
    country_name: str
    currency: str
    trust_score: float
    popular: bool = True


class GeoMarketplaceConfig:
    """Configuration for country-specific marketplaces"""
    
    # Comprehensive marketplace database
    MARKETPLACES = {
        # India
        'IN': [
            Marketplace('Amazon India', 'amazon.in', 'IN', 'India', 'INR', 0.95, True),
            Marketplace('Flipkart', 'flipkart.com', 'IN', 'India', 'INR', 0.92, True),
            Marketplace('Myntra', 'myntra.com', 'IN', 'India', 'INR', 0.88, True),
            Marketplace('Snapdeal', 'snapdeal.com', 'IN', 'India', 'INR', 0.82, True),
            Marketplace('Ajio', 'ajio.com', 'IN', 'India', 'INR', 0.85, True),
            Marketplace('Tata CLiQ', 'tatacliq.com', 'IN', 'India', 'INR', 0.87, True),
            Marketplace('Meesho', 'meesho.com', 'IN', 'India', 'INR', 0.80, True),
            Marketplace('Paytm Mall', 'paytmmall.com', 'IN', 'India', 'INR', 0.78),
            Marketplace('ShopClues', 'shopclues.com', 'IN', 'India', 'INR', 0.75),
            Marketplace('Nykaa', 'nykaa.com', 'IN', 'India', 'INR', 0.90),  # Beauty
            Marketplace('FirstCry', 'firstcry.com', 'IN', 'India', 'INR', 0.88),  # Kids
            Marketplace('Pepperfry', 'pepperfry.com', 'IN', 'India', 'INR', 0.85),  # Furniture
        ],
        
        # United States
        'US': [
            Marketplace('Amazon', 'amazon.com', 'US', 'United States', 'USD', 0.95, True),
            Marketplace('eBay', 'ebay.com', 'US', 'United States', 'USD', 0.85, True),
            Marketplace('Walmart', 'walmart.com', 'US', 'United States', 'USD', 0.92, True),
            Marketplace('Target', 'target.com', 'US', 'United States', 'USD', 0.90, True),
            Marketplace('Best Buy', 'bestbuy.com', 'US', 'United States', 'USD', 0.88, True),
            Marketplace('Etsy', 'etsy.com', 'US', 'United States', 'USD', 0.82, True),
            Marketplace('Newegg', 'newegg.com', 'US', 'United States', 'USD', 0.85),
            Marketplace('Costco', 'costco.com', 'US', 'United States', 'USD', 0.91),
            Marketplace('Home Depot', 'homedepot.com', 'US', 'United States', 'USD', 0.89),
            Marketplace('Wayfair', 'wayfair.com', 'US', 'United States', 'USD', 0.84),
        ],
        
        # United Kingdom
        'GB': [
            Marketplace('Amazon UK', 'amazon.co.uk', 'GB', 'United Kingdom', 'GBP', 0.95, True),
            Marketplace('eBay UK', 'ebay.co.uk', 'GB', 'United Kingdom', 'GBP', 0.85, True),
            Marketplace('Argos', 'argos.co.uk', 'GB', 'United Kingdom', 'GBP', 0.90, True),
            Marketplace('John Lewis', 'johnlewis.com', 'GB', 'United Kingdom', 'GBP', 0.92, True),
            Marketplace('Currys', 'currys.co.uk', 'GB', 'United Kingdom', 'GBP', 0.87),
            Marketplace('ASOS', 'asos.com', 'GB', 'United Kingdom', 'GBP', 0.86),
            Marketplace('Very', 'very.co.uk', 'GB', 'United Kingdom', 'GBP', 0.84),
        ],
        
        # Canada
        'CA': [
            Marketplace('Amazon Canada', 'amazon.ca', 'CA', 'Canada', 'CAD', 0.95, True),
            Marketplace('eBay Canada', 'ebay.ca', 'CA', 'Canada', 'CAD', 0.85, True),
            Marketplace('Walmart Canada', 'walmart.ca', 'CA', 'Canada', 'CAD', 0.92, True),
            Marketplace('Best Buy Canada', 'bestbuy.ca', 'CA', 'Canada', 'CAD', 0.88, True),
            Marketplace('Canadian Tire', 'canadiantire.ca', 'CA', 'Canada', 'CAD', 0.89),
        ],
        
        # Australia
        'AU': [
            Marketplace('Amazon Australia', 'amazon.com.au', 'AU', 'Australia', 'AUD', 0.95, True),
            Marketplace('eBay Australia', 'ebay.com.au', 'AU', 'Australia', 'AUD', 0.85, True),
            Marketplace('Kogan', 'kogan.com', 'AU', 'Australia', 'AUD', 0.82, True),
            Marketplace('Catch', 'catch.com.au', 'AU', 'Australia', 'AUD', 0.80, True),
            Marketplace('JB Hi-Fi', 'jbhifi.com.au', 'AU', 'Australia', 'AUD', 0.88),
        ],
        
        # Germany
        'DE': [
            Marketplace('Amazon Germany', 'amazon.de', 'DE', 'Germany', 'EUR', 0.95, True),
            Marketplace('eBay Germany', 'ebay.de', 'DE', 'Germany', 'EUR', 0.85, True),
            Marketplace('Otto', 'otto.de', 'DE', 'Germany', 'EUR', 0.88, True),
            Marketplace('MediaMarkt', 'mediamarkt.de', 'DE', 'Germany', 'EUR', 0.87),
            Marketplace('Saturn', 'saturn.de', 'DE', 'Germany', 'EUR', 0.86),
        ],
        
        # France
        'FR': [
            Marketplace('Amazon France', 'amazon.fr', 'FR', 'France', 'EUR', 0.95, True),
            Marketplace('eBay France', 'ebay.fr', 'FR', 'France', 'EUR', 0.85, True),
            Marketplace('Cdiscount', 'cdiscount.com', 'FR', 'France', 'EUR', 0.88, True),
            Marketplace('Fnac', 'fnac.com', 'FR', 'France', 'EUR', 0.90),
        ],
        
        # Japan
        'JP': [
            Marketplace('Amazon Japan', 'amazon.co.jp', 'JP', 'Japan', 'JPY', 0.95, True),
            Marketplace('Rakuten', 'rakuten.co.jp', 'JP', 'Japan', 'JPY', 0.92, True),
            Marketplace('Yahoo! Shopping', 'shopping.yahoo.co.jp', 'JP', 'Japan', 'JPY', 0.88, True),
            Marketplace('Mercari', 'mercari.com', 'JP', 'Japan', 'JPY', 0.82),
        ],
        
        # China
        'CN': [
            Marketplace('Taobao', 'taobao.com', 'CN', 'China', 'CNY', 0.90, True),
            Marketplace('JD.com', 'jd.com', 'CN', 'China', 'CNY', 0.92, True),
            Marketplace('Tmall', 'tmall.com', 'CN', 'China', 'CNY', 0.91, True),
            Marketplace('Pinduoduo', 'pinduoduo.com', 'CN', 'China', 'CNY', 0.85),
        ],
        
        # UAE
        'AE': [
            Marketplace('Amazon UAE', 'amazon.ae', 'AE', 'UAE', 'AED', 0.95, True),
            Marketplace('Noon', 'noon.com', 'AE', 'UAE', 'AED', 0.90, True),
            Marketplace('Namshi', 'namshi.com', 'AE', 'UAE', 'AED', 0.85),
        ],
        
        # Singapore
        'SG': [
            Marketplace('Amazon Singapore', 'amazon.sg', 'SG', 'Singapore', 'SGD', 0.95, True),
            Marketplace('Lazada', 'lazada.sg', 'SG', 'Singapore', 'SGD', 0.88, True),
            Marketplace('Shopee', 'shopee.sg', 'SG', 'Singapore', 'SGD', 0.86, True),
            Marketplace('Qoo10', 'qoo10.sg', 'SG', 'Singapore', 'SGD', 0.82),
        ],
        
        # Brazil
        'BR': [
            Marketplace('Amazon Brazil', 'amazon.com.br', 'BR', 'Brazil', 'BRL', 0.95, True),
            Marketplace('Mercado Livre', 'mercadolivre.com.br', 'BR', 'Brazil', 'BRL', 0.90, True),
            Marketplace('Magazine Luiza', 'magazineluiza.com.br', 'BR', 'Brazil', 'BRL', 0.88),
        ],
        
        # Mexico
        'MX': [
            Marketplace('Amazon Mexico', 'amazon.com.mx', 'MX', 'Mexico', 'MXN', 0.95, True),
            Marketplace('Mercado Libre', 'mercadolibre.com.mx', 'MX', 'Mexico', 'MXN', 0.90, True),
            Marketplace('Liverpool', 'liverpool.com.mx', 'MX', 'Mexico', 'MXN', 0.88),
        ],
    }
    
    # Currency symbols
    CURRENCY_SYMBOLS = {
        'USD': '$', 'INR': '₹', 'GBP': '£', 'EUR': '€', 
        'CAD': 'C$', 'AUD': 'A$', 'JPY': '¥', 'CNY': '¥',
        'AED': 'د.إ', 'SGD': 'S$', 'BRL': 'R$', 'MXN': 'MX$'
    }
    
    @classmethod
    def get_marketplaces_for_country(cls, country_code: str, popular_only: bool = True) -> List[Marketplace]:
        """
        Get marketplaces for a specific country
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'IN', 'US')
            popular_only: If True, return only popular marketplaces
        """
        marketplaces = cls.MARKETPLACES.get(country_code.upper(), [])
        
        if popular_only:
            marketplaces = [m for m in marketplaces if m.popular]
        
        return marketplaces
    
    @classmethod
    def get_all_supported_countries(cls) -> List[Dict[str, str]]:
        """Get list of all supported countries"""
        countries = []
        seen = set()
        
        for country_code, marketplaces in cls.MARKETPLACES.items():
            if marketplaces and country_code not in seen:
                seen.add(country_code)
                countries.append({
                    'code': country_code,
                    'name': marketplaces[0].country_name,
                    'currency': marketplaces[0].currency,
                    'marketplace_count': len(marketplaces)
                })
        
        return sorted(countries, key=lambda x: x['name'])
    
    @classmethod
    def get_currency_symbol(cls, currency_code: str) -> str:
        """Get currency symbol for currency code"""
        return cls.CURRENCY_SYMBOLS.get(currency_code, currency_code)
    
    @classmethod
    def detect_country_from_ip(cls) -> str:
        """
        Detect country from IP address
        In production, use a GeoIP service
        """
        # Placeholder - in production use:
        # - MaxMind GeoIP2
        # - ipapi.co
        # - ip-api.com
        # - ipinfo.io
        
        # For now, return default
        return 'US'
    
    @classmethod
    def get_marketplace_info(cls, domain: str) -> Optional[Marketplace]:
        """Get marketplace info by domain"""
        for marketplaces in cls.MARKETPLACES.values():
            for marketplace in marketplaces:
                if marketplace.domain == domain:
                    return marketplace
        return None


def display_supported_countries():
    """Display all supported countries"""
    countries = GeoMarketplaceConfig.get_all_supported_countries()
    
    print("\n" + "="*80)
    print("🌍 SUPPORTED COUNTRIES")
    print("="*80 + "\n")
    
    for country in countries:
        symbol = GeoMarketplaceConfig.get_currency_symbol(country['currency'])
        print(f"🇮🇳 {country['name']} ({country['code']})")
        print(f"   Currency: {country['currency']} ({symbol})")
        print(f"   Marketplaces: {country['marketplace_count']}")
        print()


def display_country_marketplaces(country_code: str):
    """Display marketplaces for a specific country"""
    marketplaces = GeoMarketplaceConfig.get_marketplaces_for_country(country_code, popular_only=False)
    
    if not marketplaces:
        print(f"❌ No marketplaces found for country code: {country_code}")
        return
    
    country_name = marketplaces[0].country_name
    currency = marketplaces[0].currency
    symbol = GeoMarketplaceConfig.get_currency_symbol(currency)
    
    print("\n" + "="*80)
    print(f"🛒 MARKETPLACES IN {country_name.upper()}")
    print("="*80 + "\n")
    print(f"Currency: {currency} ({symbol})")
    print(f"Total Marketplaces: {len(marketplaces)}\n")
    
    for i, marketplace in enumerate(marketplaces, 1):
        popular_badge = "⭐" if marketplace.popular else "  "
        print(f"{popular_badge} {i}. {marketplace.name}")
        print(f"      Domain: {marketplace.domain}")
        print(f"      Trust Score: {marketplace.trust_score * 100:.0f}/100")
        print()


if __name__ == "__main__":
    # Display all supported countries
    display_supported_countries()
    
    # Display India marketplaces
    print("\n" + "="*80 + "\n")
    display_country_marketplaces('IN')
    
    # Display US marketplaces
    print("\n" + "="*80 + "\n")
    display_country_marketplaces('US')
