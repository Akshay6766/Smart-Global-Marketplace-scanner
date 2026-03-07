"""
Interactive Product Search CLI
User-friendly command-line interface for product discovery
"""

import asyncio
from smart_product_finder import ProductSearchEngine, ResultsPresenter


class InteractiveCLI:
    """Interactive command-line interface"""
    
    def __init__(self):
        self.engine = ProductSearchEngine()
        self.presenter = ResultsPresenter()
        self.last_results = []
    
    async def run(self):
        """Main interactive loop"""
        self.print_welcome()
        
        while True:
            print("\n" + "="*100)
            command = input("\n🔍 Enter product description (or 'help' for commands): ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using Product Discovery Engine!")
                break
            
            if command.lower() == 'help':
                self.print_help()
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
        print("🤖 AI-POWERED PRODUCT DISCOVERY ENGINE")
        print("="*100)
        print("\n✨ Features:")
        print("   • Search with vague descriptions")
        print("   • Multi-source aggregation")
        print("   • Intelligent ranking (price, trust, quality)")
        print("   • Export results (JSON/CSV)")
        print("\n💡 Try: 'wireless headphones', 'laptop for gaming', 'running shoes'")
        print("📝 Type 'help' for all commands")
    
    def print_help(self):
        """Print help information"""
        print("\n📚 AVAILABLE COMMANDS:")
        print("="*100)
        print("\n🔍 SEARCH:")
        print("   Just type your product description (e.g., 'wireless headphones')")
        print("\n📊 FILTERS:")
        print("   filter price <min> <max>  - Filter by price range")
        print("   filter source <name>      - Filter by marketplace source")
        print("   filter rating <min>       - Filter by minimum rating")
        print("\n🔄 SORTING:")
        print("   sort price               - Sort by price (low to high)")
        print("   sort rating              - Sort by rating (high to low)")
        print("   sort trust               - Sort by trust score")
        print("   sort quality             - Sort by quality score")
        print("\n💾 EXPORT:")
        print("   export json <filename>   - Export to JSON")
        print("   export csv <filename>    - Export to CSV")
        print("\n❌ EXIT:")
        print("   exit, quit, q            - Exit the program")
        print("="*100)
    
    async def search(self, query: str):
        """Perform product search"""
        try:
            print(f"\n⏳ Searching for '{query}'...")
            self.last_results = await self.engine.search(query, max_results=15)
            
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
        filename = parts[2] if len(parts) > 2 else f"results.{format_type}"
        
        try:
            if format_type == 'json':
                self.presenter.export_json(self.last_results, filename)
            elif format_type == 'csv':
                self.presenter.export_csv(self.last_results, filename)
            else:
                print(f"\n⚠️  Unknown format: {format_type}. Use 'json' or 'csv'")
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
                print(f"\n🔍 Filtered by price: ${min_price} - ${max_price}")
            
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
            print("\n⚠️  Usage: sort price, sort rating, sort trust, sort quality")
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
            
            elif sort_type == 'quality':
                sorted_results.sort(key=lambda x: x.quality_score, reverse=True)
                print("\n🔄 Sorted by quality score")
            
            else:
                print(f"\n⚠️  Unknown sort type: {sort_type}")
                return
            
            self.presenter.display_results(sorted_results[:10])
            print(f"\n💡 Showing top 10 of {len(sorted_results)} results")
        
        except Exception as e:
            print(f"\n❌ Sort failed: {e}")


async def main():
    """Run interactive CLI"""
    cli = InteractiveCLI()
    await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
