"""
Interactive Geo-Aware Product Search CLI
Allows users to select country and search local marketplaces
"""

import asyncio
from geo_product_finder import GeoProductSearchEngine
from geo_marketplace_config import GeoMarketplaceConfig
from smart_product_finder import ResultsPresenter


class GeoInteractiveCLI:
    """Interactive CLI with geo-location support"""
    
    def __init__(self):
        self.engine = None
        self.presenter = ResultsPresenter()
        self.last_results = []
        self.country_code = None
    
    async def run(self):
        """Main interactive loop"""
        self.print_welcome()
        
        # Country selection
        await self.select_country()
        
        # Search loop
        while True:
            print("\n" + "="*100)
            command = input("\n🔍 Enter product description (or 'help' for commands): ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using Geo Product Search!")
                break
            
            if command.lower() == 'help':
                self.print_help()
                continue
            
            if command.lower() == 'country':
                await self.select_country()
                continue
            
            if command.lower() == 'info':
                self.show_location_info()
                continue
            
            if command.lower().startswith('export'):
                self.handle_export(command)
                continue
            
            if command.lower().startswith('filter'):
                self.handle_filter(command)
                continue
            
            if command.lower().startswith('sort'):
                self.handle_sort(command)
                continue
            
            # Perform search
            await self.search(command)
    
    def print_welcome(self):
        """Print welcome message"""
        print("\n" + "="*100)
        print("🌍 GEO-AWARE PRODUCT SEARCH ENGINE")
        print("="*100)
        print("\n✨ Features:")
        print("   • Automatic country detection")
        print("   • Search local marketplaces")
        print("   • Country-specific pricing")
        print("   • Multi-currency support")
        print("\n🌏 Supported Countries:")
        
        countries = GeoMarketplaceConfig.get_all_supported_countries()
        for i, country in enumerate(countries[:10], 1):
            print(f"   {i}. {country['name']} ({country['code']}) - {country['marketplace_count']} marketplaces")
        
        if len(countries) > 10:
            print(f"   ... and {len(countries) - 10} more countries")
    
    async def select_country(self):
        """Allow user to select country"""
        print("\n" + "="*100)
        print("🌍 SELECT YOUR COUNTRY")
        print("="*100)
        
        countries = GeoMarketplaceConfig.get_all_supported_countries()
        
        # Display countries in columns
        print("\nAvailable Countries:\n")
        for i, country in enumerate(countries, 1):
            symbol = GeoMarketplaceConfig.get_currency_symbol(country['currency'])
            print(f"{i:2d}. {country['name']:20s} ({country['code']}) - {country['currency']} {symbol}")
        
        print("\n" + "="*100)
        
        while True:
            choice = input("\nEnter country number or code (or 'auto' for auto-detect): ").strip()
            
            if choice.lower() == 'auto':
                self.country_code = GeoMarketplaceConfig.detect_country_from_ip()
                print(f"🌍 Auto-detected: {self.country_code}")
                break
            
            # Try as number
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(countries):
                    self.country_code = countries[idx]['code']
                    break
            except ValueError:
                pass
            
            # Try as country code
            choice_upper = choice.upper()
            if any(c['code'] == choice_upper for c in countries):
                self.country_code = choice_upper
                break
            
            print("❌ Invalid choice. Please try again.")
        
        # Initialize engine with selected country
        self.engine = GeoProductSearchEngine(country_code=self.country_code)
        
        print(f"\n✅ Selected: {self.engine.country_name} ({self.engine.country_code})")
        print(f"💱 Currency: {self.engine.currency} ({self.engine.currency_symbol})")
        print(f"🛒 Marketplaces: {len(self.engine.marketplaces)}")
        
        for marketplace in self.engine.marketplaces:
            print(f"   • {marketplace.name}")
    
    def show_location_info(self):
        """Show current location configuration"""
        if not self.engine:
            print("\n⚠️  No country selected yet")
            return
        
        info = self.engine.get_location_info()
        
        print("\n" + "="*100)
        print("📍 CURRENT LOCATION SETTINGS")
        print("="*100)
        print(f"\n🌍 Country: {info['country_name']} ({info['country_code']})")
        print(f"💱 Currency: {info['currency']} ({info['currency_symbol']})")
        print(f"\n🛒 Active Marketplaces ({len(info['marketplaces'])}):")
        
        for i, marketplace in enumerate(info['marketplaces'], 1):
            print(f"   {i}. {marketplace['name']}")
            print(f"      Domain: {marketplace['domain']}")
            print(f"      Trust: {marketplace['trust_score']*100:.0f}/100")
    
    def print_help(self):
        """Print help information"""
        print("\n📚 AVAILABLE COMMANDS:")
        print("="*100)
        print("\n🔍 SEARCH:")
        print("   Just type your product description")
        print("\n🌍 LOCATION:")
        print("   country                  - Change country/region")
        print("   info                     - Show current location settings")
        print("\n📊 FILTERS:")
        print("   filter price <min> <max> - Filter by price range")
        print("   filter source <name>     - Filter by marketplace")
        print("   filter rating <min>      - Filter by minimum rating")
        print("\n🔄 SORTING:")
        print("   sort price              - Sort by price")
        print("   sort rating             - Sort by rating")
        print("   sort trust              - Sort by trust score")
        print("\n💾 EXPORT:")
        print("   export json <filename>  - Export to JSON")
        print("   export csv <filename>   - Export to CSV")
        print("\n❌ EXIT:")
        print("   exit, quit, q           - Exit the program")
        print("="*100)
    
    async def search(self, query: str):
        """Perform product search"""
        if not self.engine:
            print("\n⚠️  Please select a country first")
            await self.select_country()
        
        try:
            print(f"\n⏳ Searching for '{query}'...")
            self.last_results = await self.engine.search(query, max_results=20)
            
            if self.last_results:
                self.presenter.display_results(self.last_results[:10])
                print(f"\n💡 Showing top 10 of {len(self.last_results)} results")
                print("💡 Use 'export' to save all results or 'filter' to refine")
            else:
                print("\n❌ No results found. Try a different search term.")
        
        except Exception as e:
            print(f"\n❌ Error during search: {e}")
    
    def handle_export(self, command: str):
        """Handle export commands"""
        if not self.last_results:
            print("\n⚠️  No results to export. Perform a search first.")
            return
        
        parts = command.split()
        
        if len(parts) < 2:
            print("\n⚠️  Usage: export json <filename> or export csv <filename>")
            return
        
        format_type = parts[1].lower()
        filename = parts[2] if len(parts) > 2 else f"results_{self.country_code}.{format_type}"
        
        try:
            if format_type == 'json':
                self.presenter.export_json(self.last_results, filename)
            elif format_type == 'csv':
                self.presenter.export_csv(self.last_results, filename)
            else:
                print(f"\n⚠️  Unknown format: {format_type}")
        except Exception as e:
            print(f"\n❌ Export failed: {e}")
    
    def handle_filter(self, command: str):
        """Handle filter commands"""
        if not self.last_results:
            print("\n⚠️  No results to filter. Perform a search first.")
            return
        
        parts = command.split()
        
        if len(parts) < 2:
            print("\n⚠️  Usage: filter price <min> <max>, filter source <name>, filter rating <min>")
            return
        
        filter_type = parts[1].lower()
        filtered = self.last_results
        
        try:
            if filter_type == 'price' and len(parts) >= 4:
                min_price = float(parts[2])
                max_price = float(parts[3])
                filtered = [h for h in filtered if min_price <= h.price <= max_price]
                print(f"\n🔍 Filtered by price: {self.engine.currency_symbol}{min_price} - {self.engine.currency_symbol}{max_price}")
            
            elif filter_type == 'source' and len(parts) >= 3:
                source = parts[2].lower()
                filtered = [h for h in filtered if source in h.source.lower()]
                print(f"\n🔍 Filtered by source: {source}")
            
            elif filter_type == 'rating' and len(parts) >= 3:
                min_rating = float(parts[2])
                filtered = [h for h in filtered if h.product_rating and h.product_rating >= min_rating]
                print(f"\n🔍 Filtered by rating: {min_rating}+")
            
            else:
                print("\n⚠️  Invalid filter command")
                return
            
            if filtered:
                self.presenter.display_results(filtered[:10])
                print(f"\n💡 Showing {min(10, len(filtered))} of {len(filtered)} filtered results")
            else:
                print("\n❌ No results match the filter criteria")
        
        except Exception as e:
            print(f"\n❌ Filter failed: {e}")
    
    def handle_sort(self, command: str):
        """Handle sort commands"""
        if not self.last_results:
            print("\n⚠️  No results to sort. Perform a search first.")
            return
        
        parts = command.split()
        
        if len(parts) < 2:
            print("\n⚠️  Usage: sort price, sort rating, sort trust")
            return
        
        sort_type = parts[1].lower()
        sorted_results = self.last_results.copy()
        
        try:
            if sort_type == 'price':
                sorted_results.sort(key=lambda x: x.price)
                print("\n🔄 Sorted by price (low to high)")
            
            elif sort_type == 'rating':
                sorted_results.sort(key=lambda x: x.product_rating or 0, reverse=True)
                print("\n🔄 Sorted by rating (high to low)")
            
            elif sort_type == 'trust':
                sorted_results.sort(key=lambda x: x.trust_score, reverse=True)
                print("\n🔄 Sorted by trust score")
            
            else:
                print(f"\n⚠️  Unknown sort type: {sort_type}")
                return
            
            self.presenter.display_results(sorted_results[:10])
            print(f"\n💡 Showing top 10 of {len(sorted_results)} results")
        
        except Exception as e:
            print(f"\n❌ Sort failed: {e}")


async def main():
    """Run interactive CLI"""
    cli = GeoInteractiveCLI()
    await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
