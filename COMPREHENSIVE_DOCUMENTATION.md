Smart Product Finder - Comprehensive Documentation
Version: 2.0
Last Updated: March 7, 2026
Status: Production Ready
Author: Smart Product Finder Team

Table of Contents
Executive Summary
System Architecture
Current Features
Technical Implementation
File Structure & Dependencies
Data Flow Diagrams
API Documentation
Future Features & Monetization
Deployment Guide
Development Roadmap
1. Executive Summary
1.1 Project Overview
Smart Product Finder is an AI-powered, geo-aware e-commerce search platform that aggregates products from multiple marketplaces (Amazon, Flipkart, eBay, Walmart, Snapdeal) and provides intelligent recommendations based on price, quality, ratings, and user preferences.

Mission Statement:
To democratize smart shopping by providing consumers with unbiased, AI-powered product recommendations across all major e-commerce platforms, helping them make informed purchasing decisions while maximizing value for money.

Key Statistics:

978 pre-indexed mobile phones with CPI scores
1,359 NDTV product reviews integrated
1,019 mobile phones in master database
5+ major e-commerce platforms supported
10+ countries with geo-aware search
AI-powered chat assistant (AWS Bedrock Claude 3.5 Sonnet)
Real-time product search via Gemini AI & SerpAPI
1.2 Core Value Propositions
Multi-Marketplace Aggregation

Single search across Amazon, Flipkart, eBay, Walmart, Snapdeal
Eliminates need to visit multiple websites
Comprehensive price comparison
AI-Powered Intelligence

Natural language product queries
Smart recommendations based on preferences
Budget-aware suggestions
Product comparison analysis
Mobile CPI Scoring System

Proprietary Calculated Performance Index for 978+ phones
Multi-factor scoring (processor, display, camera, battery, storage, connectivity)
Objective quality assessment
Price-to-value ratio analysis
Geo-Aware Search

Auto-detects user location
Shows relevant local marketplaces
Displays prices in local currency
Country-specific product availability
Budget Optimization

Smart budget analysis
Better deal recommendations
Upgrade suggestions within reach
Savings potential calculator
Real-Time Data

Live product prices
Current ratings and reviews
Stock availability
Direct marketplace links
1.3 Technology Stack
Component	Technology	Version	Purpose
Backend	Python	3.14.3	Core application logic
Web Framework	Flask	3.1.2	REST API server
AI Assistant	AWS Bedrock Claude	3.5 Sonnet	Conversational AI
Search API	Google Gemini AI	2.0 Flash	AI-powered product search
Search API	SerpAPI	Latest	Google Shopping integration
Frontend	HTML5, CSS3, JavaScript	ES6+	User interface
HTTP Client	aiohttp	3.13.3	Async HTTP requests
Web Scraping	BeautifulSoup4	4.14.3	HTML parsing
AWS SDK	boto3	1.42.59	AWS services integration
CORS	Flask-CORS	6.0.2	Cross-origin requests
HTTP Requests	requests	2.32.5	Synchronous HTTP
XML Parser	lxml	6.0.2	Fast XML/HTML parsing
1.4 Target Audience
Primary Users:

Price-Conscious Shoppers: Looking for best deals across platforms
Tech Enthusiasts: Researching mobile phones and gadgets
Busy Professionals: Need quick, reliable product recommendations
First-Time Buyers: Require guidance in product selection
Secondary Users:

Comparison Shoppers: Want to compare products side-by-side
Deal Hunters: Looking for discounts and offers
Gift Buyers: Need recommendations for others
2. System Architecture
2.1 High-Level Architecture Diagram
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────┐      ┌──────────────────────────┐        │
│  │   Main Search Page       │      │   Mobile CPI Page        │        │
│  │   (index.html)           │      │   (mobile_cpi.html)      │        │
│  │                          │      │                          │        │
│  │ • Live Product Search    │      │ • 978 Indexed Phones     │        │
│  │ • AI Chat Assistant      │      │ • CPI Score Filtering    │        │
│  │ • Multi-Marketplace      │      │ • Local JSON Search      │        │
│  │ • Budget Filters         │      │ • AI Chat Assistant      │        │
│  │ • Sorting & Pagination   │      │ • Advanced Filters       │        │
│  │ • Country Selection      │      │ • Quick Actions          │        │
│  └──────────────────────────┘      └──────────────────────────┘        │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │              Frontend JavaScript (app.js)                 │          │
│  │  • AJAX API calls  • Dynamic UI  • Event handlers        │          │
│  └──────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FLASK WEB SERVER LAYER                            │
│                            (web_app.py)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      REST API Endpoints                           │  │
│  │                                                                   │  │
│  │  GET  /                      → Main search page                  │  │
│  │  GET  /mobile                → Mobile CPI page                   │  │
│  │  GET  /api/countries         → Supported countries list          │  │
│  │  GET  /api/marketplaces/:cc  → Country marketplaces              │  │
│  │  POST /api/search            → Live product search               │  │
│  │  POST /api/mobile/search     → Mobile CPI search                 │  │
│  │  POST /api/ai/chat           → AI assistant chat                 │  │
│  │  POST /api/ai/compare        → AI product comparison             │  │
│  │  GET  /api/ai/status         → AI service status                 │  │
│  │  GET  /api/mobile/top-cpi    → Top CPI phones                    │  │
│  │  GET  /api/mobile/best-value → Best value phones                 │  │
│  │  GET  /api/mobile/stats      → Mobile statistics                 │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS LOGIC LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ GeoProductSearch │  │ MobileCPISearch  │  │ BedrockAI        │     │
│  │ Engine           │  │ Engine           │  │ Assistant        │     │
│  │                  │  │                  │  │                  │     │
│  │ • Multi-market   │  │ • Local search   │  │ • Chat           │     │
│  │ • Gemini AI      │  │ • CPI scoring    │  │ • Compare        │     │
│  │ • SerpAPI        │  │ • Filtering      │  │ • Recommend      │     │
│  │ • Ranking        │  │ • Sorting        │  │ • Context memory │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Budget Advisor   │  │ Marketplace      │  │ Mobile CPI       │     │
│  │                  │  │ Config           │  │ Generator        │     │
│  │ • Analysis       │  │                  │  │                  │     │
│  │ • Recommendations│  │ • Geo detection  │  │ • Score calc     │     │
│  │ • Warnings       │  │ • Currency       │  │ • Index builder  │     │
│  │ • Savings calc   │  │ • Trust scores   │  │ • Data export    │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA ACCESS LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ mobile_cpi_      │  │ mobiles_2025.csv │  │ ndtv_data_       │     │
│  │ index.json       │  │                  │  │ final.csv        │     │
│  │                  │  │                  │  │                  │     │
│  │ 978 phones       │  │ 1,019 phones     │  │ 1,359 reviews    │     │
│  │ with CPI scores  │  │ master data      │  │ NDTV data        │     │
│  │ Fast local search│  │ Source data      │  │ Review content   │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL SERVICES LAYER                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Gemini AI        │  │ SerpAPI          │  │ AWS Bedrock      │     │
│  │ (Google)         │  │ (Google Shopping)│  │ (Claude 3.5)     │     │
│  │                  │  │                  │  │                  │     │
│  │ • Product search │  │ • Real URLs      │  │ • Chat AI        │     │
│  │ • AI search      │  │ • Live prices    │  │ • Recommendations│     │
│  │ • Web scraping   │  │ • Ratings        │  │ • Comparisons    │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Amazon.in        │  │ Flipkart.com     │  │ eBay.in          │     │
│  │ (Target)         │  │ (Target)         │  │ (Target)         │     │
│  │                  │  │                  │  │                  │     │
│  │ • Product pages  │  │ • Product pages  │  │ • Product pages  │     │
│  │ • Prices         │  │ • Prices         │  │ • Prices         │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐                            │
│  │ Walmart.com      │  │ Snapdeal.com     │                            │
│  │ (Target)         │  │ (Target)         │                            │
│  │                  │  │                  │                            │
│  │ • Product pages  │  │ • Product pages  │                            │
│  └──────────────────┘  └──────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────┘
2.2 Component Interaction Flow
Request-Response Pattern:

User Request → Frontend (HTML/JS)
AJAX Call → Flask REST API
Route Handler → Business Logic Layer
Search Engine → External APIs (Gemini/SerpAPI) OR Local Data (JSON/CSV)
Data Processing → Ranking, Filtering, Sorting
Response → JSON to Frontend
UI Update → Display results to user
2.3 Key Design Decisions
Decision	Rationale	Benefits
Flask over Django	Lightweight, flexible, perfect for REST APIs	Faster development, less overhead
Async/await	Concurrent marketplace searches	5x faster search results
JSON for mobile data	Fast local search, no database overhead	Sub-second search response
AWS Bedrock	Enterprise-grade AI, pay-per-use	High-quality AI, cost-effective
Gemini AI primary	Free tier, good quality, web search	Zero cost for development
SerpAPI fallback	Real Google Shopping URLs	Actual marketplace links
No database	Simplicity, portability	Easy deployment, no DB management
Dataclasses	Type safety, clarity	Fewer bugs, better IDE support
2.4 Architecture Patterns
Primary Pattern: Layered Architecture (N-Tier)

Design Principles:

Separation of Concerns: Each layer has distinct responsibilities
Modularity: Components can be developed and tested independently
Scalability: Layers can be scaled horizontally
Maintainability: Clear boundaries make updates easier
Testability: Each layer can be unit tested in isolation
3. Current Features
3.1 Main Search Page Features
3.1.1 Live Product Search
Multi-Marketplace Aggregation: Searches Amazon, Flipkart, eBay, Walmart, Snapdeal simultaneously
Real-Time Data: Live prices, ratings, reviews from actual marketplaces
Geo-Aware: Auto-detects user country, shows relevant marketplaces
Currency Conversion: Displays prices in local currency (INR, USD, EUR, etc.)
Smart Ranking: Products ranked by trust, quality, and value scores
Direct Links: Click to go directly to product page on marketplace
3.1.2 AI Chat Assistant
Conversational Interface: Natural language product queries

"Find me a good laptop under 50000"
"Which phone has the best camera?"
"Compare iPhone 15 and Samsung S24"
Smart Recommendations: Based on user preferences and budget

Analyzes conversation context
Remembers previous queries
Provides personalized suggestions
Product Comparison: Side-by-side feature analysis

Compares specs, prices, ratings
Highlights pros and cons
Recommends best choice
Follow-up Questions: Contextual conversation history

"Show me cheaper options"
"What about better battery life?"
"Any premium alternatives?"
Quick Actions: Pre-defined queries

Cheaper Options
Premium Alternatives
Compare Products
Best Deals
3.1.3 Search Filters & Controls
Budget Range: Min/max price filtering
Marketplace Selection: Choose specific platforms
Country Selection: Change target country
Sorting Options:
Price (low to high, high to low)
Rating (highest first)
Reviews (most reviewed)
Relevance (best match)
Pagination: Navigate through results (20 per page)
3.1.4 Product Display
Product Cards: Clean, informative layout

Product image
Title and description
Price in local currency
Marketplace badge
Rating stars and review count
Seller information
"View Product" button
Trust Indicators:

Seller rating
Product rating
Review count
Marketplace trust score
3.2 Mobile CPI Page Features
3.2.1 CPI Scoring System
978 Indexed Phones: Pre-calculated CPI scores for fast search
Multi-Factor Scoring:
Processor Performance (0-100): Chipset, cores, clock speed
Display Quality (0-100): Resolution, refresh rate, size, type
Camera Capability (0-100): Megapixels, features, video quality
Battery Life (0-100): Capacity, charging speed, efficiency
Storage Capacity (0-100): RAM, internal storage, expandability
Connectivity Features (0-100): 5G, WiFi 6, Bluetooth, NFC
Overall CPI Score (0-100): Weighted average of all factors
CPI Formula:

Overall CPI = (Processor × 0.25) + (Display × 0.15) + (Camera × 0.20) + 
              (Battery × 0.20) + (Storage × 0.10) + (Connectivity × 0.10)
Price-Value Ratio:

Price-Value Ratio = Overall CPI / (Price / 1000)
Higher ratio = Better value for money
3.2.2 Advanced Filtering
Price Range: ₹0 - ₹200,000+ with slider
Brand Filter: Samsung, Apple, OnePlus, Xiaomi, Realme, Vivo, Oppo, etc.
CPI Score: Minimum score threshold (0-100)
Search: Name, brand, processor, features
Sorting Options:
CPI Score (highest first)
Price (low to high, high to low)
Name (A-Z, Z-A)
Brand (A-Z)
3.2.3 Mobile-Specific AI Chat
Battery-Focused Queries: "Best phone with 5000mAh battery"
Camera-Focused Queries: "Phone with best camera under 30000"
Gaming Queries: "Best gaming phone under 25000"
Budget Recommendations: "Best value phone under 15000"
Comparison: "Compare OnePlus 11 vs Samsung S23"
Quick Actions:
Better Battery
Better Camera
Cheaper Options
Compare Phones
3.2.4 Search Results Display
Pagination: Inline with search results heading

"Search Results (Page 1 of 5) (20 phones)"
First | Previous | Next | Last buttons
Phone Cards: Detailed information

Phone image placeholder
Name and brand
Price in ₹
Overall CPI score with color coding
Individual component scores
"View Details" button
3.2.5 Top Phones & Statistics
Top CPI Phones: Highest scoring phones
Best Value Phones: Best price-to-CPI ratio
Statistics Dashboard:
Total phones indexed
Average CPI score
Price range
Brand distribution
3.3 Backend Features
3.3.1 Intelligent Search
Query Enhancement: AI-powered query optimization

Adds context keywords
Improves search relevance
Handles typos and variations
Fallback Strategy: Multi-tier search approach

Try SerpAPI (Google Shopping) - Real product URLs
Fallback to Gemini AI - AI-powered search
Return ranked results
Error Handling: Graceful degradation

API failures handled silently
User sees best available results
No crashes or error pages
Performance Optimization:

Async concurrent searches
Response caching (future)
Efficient data structures
3.3.2 Budget Analysis
Smart Recommendations: Find better deals

Analyzes all search results
Identifies products with better value
Suggests alternatives
Quality Assessment: Budget vs. quality analysis

Excellent: Premium budget, top products
Good: Adequate budget, good options
Fair: Limited budget, decent choices
Limited: Very tight budget, basic options
Upgrade Suggestions: Premium options within reach

Finds products slightly above budget
Shows potential upgrade benefits
Calculates additional cost
Savings Calculator: Potential savings identification

Compares similar products
Shows price differences
Highlights best deals
3.3.3 Geo-Location Features
Auto-Detection: Detects user country from IP

Supported Countries: 10+ countries

India (IN)
United States (US)
United Kingdom (UK)
Canada (CA)
Australia (AU)
Germany (DE)
France (FR)
Japan (JP)
Singapore (SG)
UAE (AE)
Marketplace Mapping: Country-specific marketplaces

Currency Handling: Local currency display

Trust Scores: Marketplace reliability ratings

3.3.4 Data Management
Mobile CPI Index: JSON-based fast search

978 phones pre-indexed
Sub-second search response
No database required
CSV Data Sources:

mobiles_2025.csv: 1,019 phones master data
ndtv_data_final.csv: 1,359 product reviews
Data Integrity: Validation and error handling

Backup System: AWS S3 automated backups

4. Technical Implementation
4.1 Core Modules
4.1.1 web_app.py - Main Flask Application
Purpose: REST API server and request routing

Key Functions:

@app.route('/')
def index():
    """Serve the main search page"""
    
@app.route('/mobile')
def mobile_index():
    """Serve the mobile CPI page"""
    
@app.route('/api/search', methods=['POST'])
def search_products():
    """Live product search endpoint"""
    
@app.route('/api/mobile/search', methods=['POST'])
def search_mobiles():
    """Mobile CPI search endpoint"""
    
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI assistant chat endpoint"""
    
@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Returns supported countries list"""
    
@app.route('/api/marketplaces/<country_code>', methods=['GET'])
def get_marketplaces(country_code):
    """Returns country-specific marketplaces"""
Dependencies: Flask, Flask-CORS, asyncio, json

Key Features:

CORS enabled for API access
Async event loop for concurrent searches
Error handling and logging
Session management
4.1.2 geo_product_finder.py - Geo-Aware Search Engine
Purpose: Multi-marketplace product search with geo-location awareness

Class: GeoProductSearchEngine

Key Methods:

def __init__(self, country_code: Optional[str] = None, auto_detect: bool = True):
    """Initialize with country-specific configuration"""
    
async def search(self, query: str, max_results: int = 50, budget: float = None) -> List[ProductHit]:
    """Main search method - searches all marketplaces"""
    
async def _search_marketplace(self, marketplace: Marketplace, query: str, budget: float = None) -> List[ProductHit]:
    """Search single marketplace using Gemini/SerpAPI"""
    
def _rank_products(self, hits: List[ProductHit]) -> List[ProductHit]:
    """Apply ranking algorithm to results"""
    
def _calculate_trust_score(self, hit: ProductHit) -> float:
    """Calculate seller/marketplace trust score"""
    
def _calculate_quality_score(self, hit: ProductHit) -> float:
    """Calculate product quality score"""
    
def _calculate_value_score(self, hit: ProductHit, all_hits: List[ProductHit]) -> float:
    """Calculate value for money score"""
Search Strategy:

Try SerpAPI (Google Shopping) - Real product URLs
Fallback to Gemini AI - AI-powered search
Rank and return results
Ranking Algorithm:

overall_rank = (trust_score × 0.3) + (quality_score × 0.4) + (value_score × 0.3)
4.1.3 mobile_cpi_generator.py - CPI Scoring System
Purpose: Generate Calculated Performance Index scores for mobile phones

Class: MobileCPIGenerator

Scoring Components:

Processor Score (0-100):

Chipset brand (Snapdragon, MediaTek, Apple, Exynos)
Number of cores
Clock speed (GHz)
Architecture (nm)
Display Score (0-100):

Resolution (HD, FHD, QHD, 4K)
Refresh rate (60Hz, 90Hz, 120Hz, 144Hz)
Screen size (inches)
Display type (LCD, AMOLED, Super AMOLED)
Camera Score (0-100):

Primary camera megapixels
Number of cameras
Features (OIS, Night mode, 8K video)
Front camera quality
Battery Score (0-100):

Battery capacity (mAh)
Fast charging support
Wireless charging
Reverse charging
Storage Score (0-100):

RAM capacity (GB)
Internal storage (GB)
Expandable storage support
Storage type (UFS, eMMC)
Connectivity Score (0-100):

5G support
WiFi version (WiFi 5, WiFi 6, WiFi 6E)
Bluetooth version
NFC support
CPI Formula:

overall_cpi = (
    processor_score * 0.25 +
    display_score * 0.15 +
    camera_score * 0.20 +
    battery_score * 0.20 +
    storage_score * 0.10 +
    connectivity_score * 0.10
)
Price-Value Ratio:

price_value_ratio = overall_cpi / (price / 1000)
4.1.4 bedrock_ai_assistant.py - AI Chat Assistant
Purpose: Conversational AI for product recommendations

Class: BedrockShoppingAssistant

Key Methods:

def __init__(self, region='us-east-1', model='claude-sonnet'):
    """Initialize AWS Bedrock client"""
    
def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict:
    """Main chat interface with context memory"""
    
def compare_products(self, products: List[Dict]) -> str:
    """Compare multiple products side-by-side"""
    
def get_personalized_recommendations(self, search_history: List[str], budget: float, preferences: Dict) -> Dict:
    """Get personalized product recommendations"""
    
def _extract_search_params(self, response: str, context: Optional[Dict]) -> Optional[Dict]:
    """Parse AI response for search parameters"""
AI Model: AWS Bedrock Claude 3.5 Sonnet

Features:

Conversational memory (maintains context across messages)
Search parameter extraction from natural language
Product comparison analysis
Budget-aware recommendations
Personalized suggestions based on history
System Prompt:

You are a helpful shopping assistant. Help users find the best products 
based on their needs, budget, and preferences. Be concise, friendly, and 
provide actionable recommendations.
4.1.5 gemini_search.py - Gemini AI Search
Purpose: Use Google Gemini AI for product search

Class: GeminiProductSearch

Models Supported (with automatic fallback):

gemini-2.0-flash (primary)
gemini-2.5-flash
gemini-2.5-pro
gemini-1.5-flash
gemini-1.5-pro
Query Optimization Templates:

QUERY_TEMPLATES = {
    "mobile": "best {query} under {budget} with good camera battery life and performance reviews ratings",
    "laptop": "best {query} under {budget} with good performance battery life and build quality reviews",
    "headphone": "best {query} under {budget} with good sound quality comfort and battery life reviews",
    "default": "best {query} under {budget} with high ratings good reviews and value for money"
}
Key Methods:

async def search_products(self, query: str, country: str = "India", max_results: int = 10, 
                         budget: float = None, currency: str = "INR") -> List[ProductHit]:
    """Search for products using Gemini AI"""
    
def _optimize_query(self, query: str, budget: float = None, currency: str = "INR") -> str:
    """Enhance user query for better search results"""
    
def _is_valid_product_url(self, url: str) -> bool:
    """Validate product URL is real, not placeholder"""
Features:

Automatic model fallback if primary fails
Query optimization based on product category
URL validation to filter fake/placeholder links
Budget-aware search
Returns structured product data
4.1.6 serpapi_search.py - SerpAPI Integration
Purpose: Get real product URLs from Google Shopping

Class: SerpAPISearch

Key Methods:

async def search_products(self, query: str, country: str = "India", max_results: int = 10,
                         budget: float = None, currency: str = "INR") -> List[ProductHit]:
    """Search for products using Google Shopping via SerpAPI"""
Features:

Real product URLs from Google Shopping
Actual marketplace links (Amazon, Flipkart, eBay)
Live prices and ratings
Product thumbnails
Budget filtering
API Endpoint: https://serpapi.com/search

Parameters:

engine: "google_shopping"
q: Search query
gl: Country code (in, us, uk, etc.)
hl: Language (en)
num: Number of results
4.1.7 budget_advisor.py - Budget Intelligence
Purpose: Analyze user budget and provide smart recommendations

Class: BudgetAdvisor

Analysis Components:

def analyze_budget(self, budget: float, products: List[ProductHit], 
                   currency: str = "INR") -> BudgetAnalysis:
    """Comprehensive budget analysis"""
Budget Quality Levels:

Excellent (>80% of max price): Premium products available
Good (60-80%): Good selection of quality products
Fair (40-60%): Decent options available
Limited (<40%): Basic options only
Recommendations:

Better deals within budget
Upgrade options (slightly above budget)
Savings potential
Quality vs. price analysis
4.1.8 geo_marketplace_config.py - Marketplace Configuration
Purpose: Manage country-specific marketplace configurations

Class: GeoMarketplaceConfig

Supported Marketplaces:

MARKETPLACES = {
    'IN': [  # India
        Marketplace('Amazon India', 'amazon.in', 'IN', 'India', 'INR', 0.95, True),
        Marketplace('Flipkart', 'flipkart.com', 'IN', 'India', 'INR', 0.90, True),
        Marketplace('Snapdeal', 'snapdeal.com', 'IN', 'India', 'INR', 0.75, True),
    ],
    'US': [  # United States
        Marketplace('Amazon US', 'amazon.com', 'US', 'United States', 'USD', 0.95, True),
        Marketplace('eBay', 'ebay.com', 'US', 'United States', 'USD', 0.85, True),
        Marketplace('Walmart', 'walmart.com', 'US', 'United States', 'USD', 0.90, True),
    ],
    # ... more countries
}
Currency Symbols:

CURRENCY_SYMBOLS = {
    'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 
    'CAD': 'C$', 'AUD': 'A$', 'JPY': '¥', 'SGD': 'S$'
}
4.2 Data Structures
4.2.1 ProductHit (smart_product_finder.py)
@dataclass
class ProductHit:
    title: str                      # Product name
    price: float                    # Price in local currency
    currency: str                   # Currency code (INR, USD, etc.)
    url: str                        # Product page URL
    source: str                     # Marketplace name
    seller_name: Optional[str]      # Seller/brand name
    seller_rating: Optional[float]  # Seller rating (0-5)
    product_rating: Optional[float] # Product rating (0-5)
    review_count: int               # Number of reviews
    image_url: Optional[str]        # Product image URL
    description: Optional[str]      # Product description
    trust_score: float              # Calculated trust (0-1)
    quality_score: float            # Calculated quality (0-1)
    value_score: float              # Calculated value (0-1)
    overall_rank: float             # Final ranking score
    best_choice_reason: Optional[str] # Why this is recommended
4.2.2 Marketplace (geo_marketplace_config.py)
@dataclass
class Marketplace:
    name: str           # Marketplace name
    domain: str         # Domain (amazon.in, flipkart.com)
    country_code: str   # ISO country code
    country_name: str   # Country name
    currency: str       # Currency code
    trust_score: float  # Marketplace trust (0-1)
    popular: bool       # Is popular marketplace
4.2.3 Mobile CPI Score (mobile_cpi_generator.py)
@dataclass
class MobileCPIScore:
    processor_score: float      # 0-100
    display_score: float        # 0-100
    camera_score: float         # 0-100
    battery_score: float        # 0-100
    storage_score: float        # 0-100
    connectivity_score: float   # 0-100
    overall_cpi: float          # 0-100
    price_value_ratio: float    # CPI per ₹1000
4.2.4 Budget Analysis (budget_advisor.py)
@dataclass
class BudgetAnalysis:
    budget: float                    # User's budget
    currency: str                    # Currency code
    quality: str                     # Budget quality level
    products_in_budget: int          # Count of products within budget
    better_deals: List[ProductHit]   # Better value products
    upgrade_options: List[ProductHit] # Premium options nearby
    savings_potential: float         # Potential savings amount
    recommendation: str              # Text recommendation
5. File Structure & Dependencies
5.1 Complete File Tree
Smart-product-finder/
│
├── Core Application Files
│   ├── web_app.py                      # Main Flask application (500 lines)
│   ├── geo_product_finder.py           # Geo-aware search engine (440 lines)
│   ├── mobile_cpi_generator.py         # CPI scoring system (350 lines)
│   ├── bedrock_ai_assistant.py         # AI chat assistant (370 lines)
│   ├── gemini_search.py                # Gemini AI search (350 lines)
│   ├── serpapi_search.py               # SerpAPI integration (200 lines)
│   ├── smart_product_finder.py         # Base search engine (320 lines)
│   ├── budget_advisor.py               # Budget intelligence (330 lines)
│   ├── geo_marketplace_config.py       # Marketplace config (250 lines)
│   └── api_keys_config.py              # API keys (placeholders)
│
├── Data Files
│   ├── mobile_cpi_index.json           # 978 phones with CPI scores (985 KB)
│   ├── mobiles_2025.csv                # 1,019 phones master data (444 KB)
│   └── ndtv_data_final.csv             # 1,359 product reviews (156 KB)
│
├── Frontend Files
│   ├── templates/
│   │   ├── index.html                  # Main search page (450 lines)
│   │   └── mobile_cpi.html             # Mobile CPI page (550 lines)
│   └── static/
│       ├── app.js                      # Frontend JavaScript (800 lines)
│       └── style.css                   # Styling (600 lines)
│
├── Utility & Helper Files
│   ├── mobile_cpi_integration.py       # CPI integration helper
│   ├── web_search_integration.py       # Web search helper
│   ├── geo_interactive_search.py       # Interactive search CLI
│   ├── interactive_search.py           # Basic search CLI
│   ├── live_product_search.py          # Live search tester
│   └── minimal_cpi.py                  # Minimal CPI calculator
│
├── Testing Files
│   ├── test_bedrock.py                 # Bedrock AI tests
│   └── test_bedrock_simple.py          # Simple Bedrock test
│
├── Deployment Files
│   ├── requirements.txt                # Python dependencies
│   ├── Procfile                        # Heroku/EB process file
│   ├── deploy.sh                       # Deployment script (Linux)
│   ├── deploy.bat                      # Deployment script (Windows)
│   ├── .ebignore                       # EB ignore patterns
│   ├── .gitignore                      # Git ignore patterns
│   ├── .ebextensions/                  # AWS EB configuration
│   └── .elasticbeanstalk/              # EB environment config
│
├── Backup & Maintenance
│   └── backup_to_aws_s3_auto.py        # Automated S3 backup
│
└── Documentation
    ├── README.md                       # Quick start guide
    ├── DESIGN.md                       # Design document
    ├── SECURITY_README.md              # Security setup guide
    ├── API_KEYS_GUIDE.md               # API keys explanation
    ├── AWS_DEPLOYMENT_GUIDE.md         # AWS deployment guide
    ├── GEN_AI_INTEGRATION_GUIDE.md     # AI integration guide
    ├── README_DEPLOYMENT.md            # Deployment instructions
    ├── GITHUB_READY_CHECKLIST.md       # Pre-push checklist
    └── COMPREHENSIVE_DOCUMENTATION.md  # This file
5.2 Module Dependencies Diagram
┌─────────────────────────────────────────────────────────────────┐
│                         web_app.py                               │
│                     (Main Flask Application)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────────────────┐
                              │                                 │
                              ▼                                 ▼
┌──────────────────────────────────────┐    ┌──────────────────────────────┐
│     geo_product_finder.py            │    │  mobile_cpi_generator.py     │
│   (Geo-Aware Search Engine)          │    │    (CPI Scoring System)      │
└──────────────────────────────────────┘    └──────────────────────────────┘
                │                                        │
                ├────────────┬───────────┐              │
                │            │           │              │
                ▼            ▼           ▼              ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐ ┌──────────────┐
│ gemini_search.py │ │serpapi_      │ │geo_marketplace_  │ │mobile_cpi_   │
│                  │ │search.py     │ │config.py         │ │index.json    │
└──────────────────┘ └──────────────┘ └──────────────────┘ └──────────────┘
                │            │                   │
                └────────────┴───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              smart_product_finder.py                             │
│              (Base ProductHit class)                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              bedrock_ai_assistant.py                             │
│              (AI Chat Assistant)                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS Bedrock API                             │
│                   (Claude 3.5 Sonnet)                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   budget_advisor.py                              │
│                 (Budget Intelligence)                            │
└─────────────────────────────────────────────────────────────────┘
5.3 Import Dependencies
web_app.py imports:

Flask, Flask-CORS
asyncio, json
geo_product_finder.GeoProductSearchEngine
geo_marketplace_config.GeoMarketplaceConfig
smart_product_finder.ProductHit
budget_advisor.BudgetAdvisor
bedrock_ai_assistant.BedrockShoppingAssistant
geo_product_finder.py imports:

asyncio, random
smart_product_finder.ProductHit
geo_marketplace_config.GeoMarketplaceConfig, Marketplace
gemini_search.GeminiProductSearch
serpapi_search.SerpAPISearch
mobile_cpi_generator.py imports:

csv, json, re
dataclasses.dataclass
typing.List, Dict
bedrock_ai_assistant.py imports:

boto3
json
typing.List, Dict, Optional
6. Data Flow Diagrams
6.1 Main Search Flow
┌─────────────┐
│    User     │
│  Types      │
│  "laptop"   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend (index.html + app.js)                             │
│  • Captures search query                                    │
│  • Validates input                                          │
│  • Shows loading spinner                                    │
└──────┬──────────────────────────────────────────────────────┘
       │ AJAX POST /api/search
       │ { query: "laptop", country: "IN", budget: 50000 }
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API (web_app.py)                                     │
│  • Receives request                                         │
│  • Validates parameters                                     │
│  • Creates search engine instance                           │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  GeoProductSearchEngine (geo_product_finder.py)             │
│  • Detects country (India)                                  │
│  • Gets marketplaces (Amazon.in, Flipkart, Snapdeal)       │
│  • Initiates concurrent searches                            │
└──────┬──────────────────────────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  SerpAPI     │  │  Gemini AI   │  │  Fallback    │
│  Search      │  │  Search      │  │  (if needed) │
│              │  │              │  │              │
│ • Google     │  │ • AI-powered │  │ • Mock data  │
│   Shopping   │  │   search     │  │              │
│ • Real URLs  │  │ • Web scrape │  │              │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Product Ranking Algorithm                                  │
│  • Calculate trust_score (seller + marketplace)             │
│  • Calculate quality_score (rating + reviews)               │
│  • Calculate value_score (price vs. others)                 │
│  • overall_rank = trust×0.3 + quality×0.4 + value×0.3      │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Budget Advisor (budget_advisor.py)                         │
│  • Analyze budget quality                                   │
│  • Find better deals                                        │
│  • Suggest upgrades                                         │
│  • Calculate savings                                        │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API Response                                         │
│  • JSON with products array                                 │
│  • Budget analysis                                          │
│  • Metadata (count, page, etc.)                             │
└──────┬──────────────────────────────────────────────────────┘
       │ JSON Response
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend (app.js)                                          │
│  • Parse JSON response                                      │
│  • Render product cards                                     │
│  • Update pagination                                        │
│  • Hide loading spinner                                     │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│    User     │
│  Sees       │
│  Results    │
└─────────────┘
6.2 AI Chat Flow
┌─────────────┐
│    User     │
│  Types      │
│  "Best      │
│  phone?"    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend Chat Interface                                    │
│  • Captures message                                         │
│  • Adds to chat history (UI)                                │
│  • Shows typing indicator                                   │
└──────┬──────────────────────────────────────────────────────┘
       │ AJAX POST /api/ai/chat
       │ { message: "Best phone?", context: {...} }
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API (web_app.py)                                     │
│  • Receives chat message                                    │
│  • Extracts context (previous messages, budget, etc.)       │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  BedrockShoppingAssistant (bedrock_ai_assistant.py)         │
│  • Maintains conversation history                           │
│  • Builds system prompt                                     │
│  • Adds user message to context                             │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS Bedrock API                                            │
│  • Claude 3.5 Sonnet model                                  │
│  • Processes conversation                                   │
│  • Generates intelligent response                           │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Response Processing                                        │
│  • Parse AI response                                        │
│  • Extract search parameters (if any)                       │
│  • Extract suggestions                                      │
│  • Determine if search needed                               │
└──────┬──────────────────────────────────────────────────────┘
       │
       ├─── If search needed ───┐
       │                        │
       ▼                        ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│  No Search       │    │  Trigger Product Search          │
│  Return response │    │  • Extract query, budget         │
│  only            │    │  • Call GeoProductSearchEngine   │
└──────┬───────────┘    │  • Get products                  │
       │                │  • Add to response               │
       │                └──────┬───────────────────────────┘
       │                       │
       └───────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API Response                                         │
│  • AI response text                                         │
│  • Suggestions array                                        │
│  • Products array (if search performed)                     │
│  • ready_to_search flag                                     │
└──────┬──────────────────────────────────────────────────────┘
       │ JSON Response
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend Chat Interface                                    │
│  • Display AI message                                       │
│  • Show products (if any)                                   │
│  • Show suggestions as buttons                              │
│  • Update conversation history                              │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│    User     │
│  Sees AI    │
│  Response   │
└─────────────┘
6.3 Mobile CPI Search Flow
┌─────────────┐
│    User     │
│  Searches   │
│  "Samsung"  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend (mobile_cpi.html)                                 │
│  • Captures search query                                    │
│  • Gets filter values (price, brand, CPI)                   │
│  • Gets sort preference                                     │
└──────┬──────────────────────────────────────────────────────┘
       │ AJAX POST /api/mobile/search
       │ { query: "Samsung", price_min: 10000, price_max: 30000,
       │   min_cpi: 70, sort_by: "overall_cpi" }
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API (web_app.py)                                     │
│  • Receives search request                                  │
│  • Validates parameters                                     │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  MobileCPISearchEngine (web_app.py)                         │
│  • Loads mobile_cpi_index.json (if not loaded)              │
│  • 978 phones in memory                                     │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Search & Filter Logic                                      │
│  • Match query against name/brand                           │
│  • Filter by price range                                    │
│  • Filter by minimum CPI score                              │
│  • Filter by brand (if specified)                           │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Sorting Logic                                              │
│  • Sort by: overall_cpi, price, name, brand                 │
│  • Order: ascending or descending                           │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Pagination                                                 │
│  • Calculate total pages                                    │
│  • Get current page results (20 per page)                   │
│  • Generate page metadata                                   │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Flask API Response                                         │
│  • Phones array (20 items)                                  │
│  • Total count                                              │
│  • Page number                                              │
│  • Total pages                                              │
└──────┬──────────────────────────────────────────────────────┘
       │ JSON Response (< 50ms)
       ▼
┌─────────────────────────────────────────────────────────────┐
│  Frontend (mobile_cpi.html)                                 │
│  • Render phone cards                                       │
│  • Update pagination controls                               │
│  • Update result count                                      │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│    User     │
│  Sees       │
│  Results    │
└─────────────┘
7. API Documentation
7.1 REST API Endpoints
7.1.1 GET / - Main Search Page
Description: Serves the main product search page

Response: HTML page

Example:

GET http://localhost:5000/
7.1.2 GET /mobile - Mobile CPI Page
Description: Serves the mobile CPI search page

Response: HTML page

Example:

GET http://localhost:5000/mobile
7.1.3 GET /api/countries - Get Supported Countries
Description: Returns list of all supported countries

Response:

{
  "success": true,
  "countries": [
    {
      "code": "IN",
      "name": "India",
      "currency": "INR",
      "currency_symbol": "₹"
    },
    {
      "code": "US",
      "name": "United States",
      "currency": "USD",
      "currency_symbol": "$"
    }
  ]
}
7.1.4 GET /api/marketplaces/:country_code - Get Country Marketplaces
Description: Returns marketplaces for specific country

Parameters:

country_code (path): ISO country code (IN, US, UK, etc.)
Response:

{
  "success": true,
  "country_code": "IN",
  "currency": "INR",
  "currency_symbol": "₹",
  "marketplaces": [
    {
      "name": "Amazon India",
      "domain": "amazon.in",
      "currency": "INR",
      "trust_score": 0.95,
      "popular": true
    },
    {
      "name": "Flipkart",
      "domain": "flipkart.com",
      "currency": "INR",
      "trust_score": 0.90,
      "popular": true
    }
  ]
}
7.1.5 POST /api/search - Live Product Search
Description: Search for products across multiple marketplaces

Request Body:

{
  "query": "laptop",
  "country_code": "IN",
  "page": 1,
  "per_page": 20,
  "sort_by": "overall_rank",
  "sort_order": "desc",
  "budget": 50000
}
Response:

{
  "success": true,
  "products": [
    {
      "title": "Dell Inspiron 15 Laptop",
      "price": 45999,
      "currency": "INR",
      "url": "https://amazon.in/dp/B0XXXXX",
      "source": "Amazon",
      "seller_name": "Appario Retail",
      "seller_rating": 4.5,
      "product_rating": 4.3,
      "review_count": 2847,
      "image_url": "https://...",
      "description": "Intel i5, 8GB RAM, 512GB SSD",
      "trust_score": 0.92,
      "quality_score": 0.86,
      "value_score": 0.88,
      "overall_rank": 0.89,
      "best_choice_reason": "Within budget • 4.3/5.0 • 2847 reviews • Amazon"
    }
  ],
  "total": 45,
  "page": 1,
  "per_page": 20,
  "total_pages": 3,
  "budget_analysis": {
    "quality": "Good",
    "recommendation": "You have a good budget with many quality options available."
  }
}
Error Response:

{
  "success": false,
  "error": "Invalid country code"
}
7.1.6 POST /api/mobile/search - Mobile CPI Search
Description: Search mobile phones with CPI scores

Request Body:

{
  "query": "Samsung",
  "price_min": 10000,
  "price_max": 30000,
  "min_cpi": 70,
  "brand": "Samsung",
  "sort_by": "overall_cpi",
  "sort_order": "desc",
  "page": 1,
  "per_page": 20
}
Response:

{
  "success": true,
  "phones": [
    {
      "name": "Samsung Galaxy M34 5G",
      "brand": "Samsung",
      "price": 16999,
      "processor": "Exynos 1280",
      "display": "6.5\" FHD+ 120Hz Super AMOLED",
      "camera": "50MP + 8MP + 2MP",
      "battery": "6000mAh",
      "storage": "6GB RAM, 128GB",
      "connectivity": "5G, WiFi 6, Bluetooth 5.2",
      "cpi_scores": {
        "processor_score": 75,
        "display_score": 85,
        "camera_score": 78,
        "battery_score": 95,
        "storage_score": 70,
        "connectivity_score": 85,
        "overall_cpi": 81.5,
        "price_value_ratio": 4.79
      },
      "search_keywords": ["samsung", "galaxy", "m34", "5g", "budget"]
    }
  ],
  "total": 45,
  "page": 1,
  "per_page": 20,
  "total_pages": 3
}
7.1.7 POST /api/ai/chat - AI Assistant Chat
Description: Chat with AI shopping assistant

Request Body:

{
  "message": "I need a good phone under 20000 with great camera",
  "context": {
    "country_code": "IN",
    "budget": 20000,
    "previous_messages": [
      {"role": "user", "content": "Hi"},
      {"role": "assistant", "content": "Hello! How can I help you find products today?"}
    ]
  }
}
Response:

{
  "success": true,
  "response": "Based on your budget of ₹20,000 and camera requirement, I recommend the Samsung Galaxy M34 5G with 50MP camera and the Realme 11 Pro with 100MP camera. Both offer excellent camera quality in your budget.",
  "suggestions": [
    "Show me Samsung Galaxy M34",
    "Compare these phones",
    "What about better battery life?"
  ],
  "ready_to_search": true,
  "search_params": {
    "query": "Samsung Galaxy M34 Realme 11 Pro",
    "budget": 20000
  },
  "products": [
    {
      "title": "Samsung Galaxy M34 5G",
      "price": 16999,
      "currency": "INR",
      "url": "https://amazon.in/dp/B0C4SD8XD9",
      "source": "Amazon",
      "product_rating": 4.3,
      "review_count": 2847,
      "best_choice_reason": "Within budget • 4.3/5.0 • 2847 reviews • Amazon"
    }
  ],
  "search_performed": true,
  "query_used": "Samsung Galaxy M34 Realme 11 Pro"
}
Error Response:

{
  "success": false,
  "error": "AI not configured"
}
7.1.8 POST /api/ai/compare - AI Product Comparison
Description: Compare multiple products using AI

Request Body:

{
  "products": [
    {
      "title": "Samsung Galaxy M34 5G",
      "price": 16999,
      "specs": "50MP camera, 6000mAh battery, Exynos 1280"
    },
    {
      "title": "Realme 11 Pro",
      "price": 19999,
      "specs": "100MP camera, 5000mAh battery, Dimensity 7050"
    }
  ]
}
Response:

{
  "comparison": "**Samsung Galaxy M34 5G vs Realme 11 Pro**\n\n**Camera**: Realme 11 Pro wins with 100MP vs 50MP\n**Battery**: Samsung M34 wins with 6000mAh vs 5000mAh\n**Processor**: Realme 11 Pro has better Dimensity 7050\n**Price**: Samsung M34 is ₹3000 cheaper\n\n**Recommendation**: If camera is priority, go for Realme 11 Pro. If battery life and value matter more, choose Samsung M34."
}
7.1.9 GET /api/ai/status - AI Service Status
Description: Check if AI assistant is available

Response:

{
  "ready": true,
  "model": "Claude 3.5 Sonnet"
}
7.1.10 GET /api/mobile/top-cpi - Top CPI Phones
Description: Get phones with highest CPI scores

Query Parameters:

limit (optional): Number of results (default: 10)
Response:

{
  "success": true,
  "phones": [
    {
      "name": "iPhone 15 Pro Max",
      "brand": "Apple",
      "price": 159900,
      "cpi_scores": {
        "overall_cpi": 95.5
      }
    }
  ]
}
7.1.11 GET /api/mobile/best-value - Best Value Phones
Description: Get phones with best price-to-CPI ratio

Query Parameters:

limit (optional): Number of results (default: 10)
Response:

{
  "success": true,
  "phones": [
    {
      "name": "Poco X6 Pro",
      "brand": "Poco",
      "price": 24999,
      "cpi_scores": {
        "overall_cpi": 82.5,
        "price_value_ratio": 3.30
      }
    }
  ]
}
7.1.12 GET /api/mobile/stats - Mobile Statistics
Description: Get statistics about mobile phone database

Response:

{
  "success": true,
  "stats": {
    "total_phones": 978,
    "avg_cpi": 72.5,
    "avg_price": 28450,
    "price_range": {
      "min": 5999,
      "max": 189900
    },
    "brands": 25,
    "top_brands": ["Samsung", "Xiaomi", "Realme", "Apple", "OnePlus"]
  }
}
7.2 Error Codes
Status Code	Error	Description
200	Success	Request successful
400	Bad Request	Invalid parameters
404	Not Found	Resource not found
500	Internal Server Error	Server error
503	Service Unavailable	AI service not configured
8. Future Features & Monetization
8.1 Affiliate Marketing Integration
8.1.1 Amazon Associates Program
Implementation Plan:

# affiliate_manager.py
class AffiliateManager:
    def __init__(self):
        self.amazon_tag = "smartprodfind-21"  # Amazon Associate ID
        self.flipkart_tag = "smartprodfind-flipkart"
        
    def add_affiliate_tag(self, url: str, marketplace: str) -> str:
        """Add affiliate tracking tag to product URL"""
        if "amazon" in marketplace.lower():
            return self._add_amazon_tag(url)
        elif "flipkart" in marketplace.lower():
            return self._add_flipkart_tag(url)
        return url
    
    def _add_amazon_tag(self, url: str) -> str:
        """Add Amazon affiliate tag"""
        if "?" in url:
            return f"{url}&tag={self.amazon_tag}"
        return f"{url}?tag={self.amazon_tag}"
    
    def _add_flipkart_tag(self, url: str) -> str:
        """Add Flipkart affiliate tag"""
        if "?" in url:
            return f"{url}&affid={self.flipkart_tag}"
        return f"{url}?affid={self.flipkart_tag}"
Revenue Model:

Amazon Associates: 1-10% commission per sale
Flipkart Affiliate: 2-15% commission per sale
eBay Partner Network: 1-4% commission
Estimated Revenue: ₹50,000 - ₹2,00,000/month (with 10,000 daily users)
Features:

Automatic affiliate link injection
Click tracking and analytics
Commission dashboard
Performance reports
8.1.2 Multi-Marketplace Affiliate Integration
Supported Programs:

Marketplace	Commission Rate	Cookie Duration	Sign-up Link
Amazon India	1-10%	24 hours	https://affiliate-program.amazon.in
Flipkart	2-15%	24 hours	https://affiliate.flipkart.com
eBay	1-4%	24 hours	https://partnernetwork.ebay.com
Snapdeal	2-12%	30 days	https://affiliate.snapdeal.com
Myntra	5-15%	30 days	https://www.myntra.com/affiliate
Implementation:

# Enhanced product URL with affiliate tracking
def enhance_product_url(product: ProductHit) -> ProductHit:
    """Add affiliate tracking to product URL"""
    affiliate_manager = AffiliateManager()
    product.url = affiliate_manager.add_affiliate_tag(
        product.url, 
        product.source
    )
    # Add click tracking
    product.url = add_click_tracking(product.url, product.id)
    return product
8.2 Payment Gateway Integration for Exclusive Offers
8.2.1 Problem Statement
Many users face challenges accessing credit card offers and bank discounts:

Don't have specific credit cards
Miss out on exclusive bank offers
Can't access marketplace-specific discounts
Lose cashback opportunities
8.2.2 Solution: Smart Product Finder Payment Service
Concept: We act as intermediary to help users access exclusive offers

How It Works:

User wants to buy: iPhone 15 Pro (₹1,29,900)
Marketplace offer: ₹10,000 off with HDFC Credit Card
User problem: Doesn't have HDFC card

Our Solution:
1. User pays us ₹1,25,900 (saves ₹4,000)
2. We purchase using our HDFC card (₹1,19,900)
3. We earn ₹6,000 margin
4. Product shipped directly to user
5. Everyone wins!
Implementation Architecture:

┌─────────────────────────────────────────────────────────────┐
│                    User Interface                            │
│  • Product selection                                         │
│  • Offer comparison                                          │
│  • Payment option: "Buy with Offer Assistance"              │
└──────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Payment Gateway Integration                     │
│  • Razorpay / Stripe / PayU                                 │
│  • Secure payment processing                                │
│  • Escrow service                                           │
└──────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Order Management System                         │
│  • Order placement on marketplace                           │
│  • Tracking integration                                     │
│  • Delivery coordination                                    │
└──────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Customer Support                                │
│  • Order status updates                                     │
│  • Issue resolution                                         │
│  • Refund processing                                        │
└──────────────────────────────────────────────────────────────┘
Payment Gateway Integration:

# payment_service.py
from razorpay import Client

class PaymentService:
    def __init__(self):
        self.razorpay = Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))
        
    def create_order(self, amount: float, product_id: str, user_id: str):
        """Create payment order"""
        order = self.razorpay.order.create({
            'amount': int(amount * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': f'order_{product_id}_{user_id}',
            'notes': {
                'product_id': product_id,
                'user_id': user_id,
                'service': 'offer_assistance'
            }
        })
        return order
    
    def verify_payment(self, order_id: str, payment_id: str, signature: str):
        """Verify payment signature"""
        params = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        return self.razorpay.utility.verify_payment_signature(params)
Revenue Model:

Service Fee: 2-5% of product price
Offer Margin: Difference between offer price and user price
Estimated Revenue: ₹1,00,000 - ₹5,00,000/month
8.2.3 Offer Assistance Features
1. Bank Offer Aggregation

class BankOfferManager:
    def get_available_offers(self, product_price: float, marketplace: str):
        """Get all available bank offers"""
        offers = [
            {
                'bank': 'HDFC',
                'discount': 10000,
                'min_purchase': 100000,
                'card_type': 'Credit Card',
                'valid_until': '2026-03-31'
            },
            {
                'bank': 'SBI',
                'discount': 7500,
                'min_purchase': 100000,
                'card_type': 'Debit Card',
                'valid_until': '2026-03-31'
            }
        ]
        return offers
    
    def calculate_user_savings(self, product_price: float, offer: dict):
        """Calculate how much user saves using our service"""
        offer_price = product_price - offer['discount']
        our_price = offer_price + (offer_price * 0.03)  # 3% service fee
        user_savings = product_price - our_price
        return {
            'original_price': product_price,
            'offer_price': offer_price,
            'our_price': our_price,
            'user_savings': user_savings,
            'our_margin': our_price - offer_price
        }
2. Cashback Tracking

class CashbackTracker:
    def track_cashback(self, order_id: str, user_id: str, amount: float):
        """Track cashback earned on purchase"""
        cashback = {
            'order_id': order_id,
            'user_id': user_id,
            'amount': amount,
            'status': 'pending',
            'expected_credit_date': datetime.now() + timedelta(days=90)
        }
        return cashback
3. Price Drop Protection

class PriceDropProtection:
    def monitor_price(self, product_id: str, purchase_price: float):
        """Monitor price drops after purchase"""
        # If price drops within 7 days, refund difference
        pass
8.3 Subscription Tiers
8.3.1 Free Tier
Features:

Basic product search
Limited AI chat (10 queries/day)
Standard affiliate links
Ads displayed
Revenue: ₹0/month

8.3.2 Smart Tier (₹99/month)
Features:

Unlimited product search
Unlimited AI chat
Ad-free experience
Price drop alerts (email)
Wishlist (up to 50 products)
Basic analytics
Revenue: ₹99/month × 1,000 users = ₹99,000/month

8.3.3 Pro Tier (₹299/month)
Features:

All Smart Tier features
Priority AI support
Advanced price tracking
Cashback tracking
Offer assistance (5 orders/month)
Price history graphs
Comparison reports
Wishlist (unlimited)
API access (1,000 calls/month)
Revenue: ₹299/month × 500 users = ₹1,49,500/month

8.3.4 Business Tier (₹999/month)
Features:

All Pro Tier features
Bulk product search
Custom integrations
Dedicated account manager
White-label option
API access (10,000 calls/month)
Advanced analytics
Team collaboration (5 users)
Revenue: ₹999/month × 100 users = ₹99,900/month

8.4 Additional Monetization Features
8.4.1 Price Drop Alerts
Implementation:

class PriceAlertService:
    def create_alert(self, user_id: str, product_url: str, target_price: float):
        """Create price drop alert"""
        alert = {
            'user_id': user_id,
            'product_url': product_url,
            'current_price': self.get_current_price(product_url),
            'target_price': target_price,
            'created_at': datetime.now(),
            'status': 'active'
        }
        # Check price daily
        schedule_daily_check(alert)
        return alert
    
    def check_price_drop(self, alert: dict):
        """Check if price has dropped"""
        current_price = self.get_current_price(alert['product_url'])
        if current_price <= alert['target_price']:
            self.send_notification(alert['user_id'], alert, current_price)
Revenue: Premium feature (Pro tier)

8.4.2 Product Comparison Reports
Features:

Detailed side-by-side comparison
Pros and cons analysis
Expert recommendations
Price history
User reviews summary
PDF export
Revenue: ₹49 per report OR included in Pro tier

8.4.3 Sponsored Products
Implementation:

class SponsoredProductManager:
    def get_sponsored_products(self, query: str, country: str):
        """Get sponsored products for search query"""
        # Brands pay to appear at top of results
        sponsored = self.db.query(
            "SELECT * FROM sponsored_products "
            "WHERE keywords LIKE %s AND country = %s "
            "AND budget > 0 ORDER BY bid DESC LIMIT 3",
            (f"%{query}%", country)
        )
        return sponsored
Revenue Model:

CPC (Cost Per Click): ₹5-20 per click
CPM (Cost Per 1000 Impressions): ₹100-500
Estimated Revenue: ₹50,000 - ₹2,00,000/month
8.4.4 Marketplace Partnerships
Direct API Integrations:

Amazon Product Advertising API
Flipkart Affiliate API
eBay Finding API
Walmart Open API
Benefits:

Real-time inventory
Accurate pricing
Better commission rates
Exclusive deals
Revenue: Higher commission rates (5-20%)

8.5 B2B Features
8.5.1 White-Label Solution
Offer: Provide our platform to other businesses

Features:

Custom branding
Custom domain
API access
Dedicated support
Pricing: ₹50,000 - ₹2,00,000 one-time + ₹10,000/month maintenance

8.5.2 API as a Service
Offer: Provide product search API to developers

Pricing Tiers:

Starter: 1,000 calls/month - ₹999/month
Growth: 10,000 calls/month - ₹4,999/month
Business: 100,000 calls/month - ₹19,999/month
Enterprise: Unlimited - Custom pricing
API Endpoints:

POST /api/v1/search
POST /api/v1/compare
GET /api/v1/product/:id
GET /api/v1/price-history/:id
POST /api/v1/ai/recommend
8.6 Advanced Features Roadmap
8.6.1 Visual Search
Technology: Computer Vision + AI Feature: Upload product image, find similar products Implementation: TensorFlow + ResNet model

class VisualSearchEngine:
    def search_by_image(self, image_path: str):
        """Search products by image"""
        # Extract features using CNN
        features = self.extract_features(image_path)
        # Find similar products
        similar = self.find_similar(features)
        return similar
8.6.2 Voice Search
Technology: Speech Recognition + NLP Feature: "Alexa, find me a laptop under 50000"

class VoiceSearchEngine:
    def process_voice_query(self, audio_file: str):
        """Process voice search query"""
        # Convert speech to text
        text = self.speech_to_text(audio_file)
        # Extract search parameters
        params = self.extract_params(text)
        # Perform search
        return self.search(params)
8.6.3 AR Product Preview
Technology: ARKit / ARCore Feature: See how product looks in your space Use Cases: Furniture, appliances, decor

8.6.4 Social Shopping
Features:

Share wishlists with friends
Group buying for discounts
Social proof (friends' purchases)
Product recommendations from network
8.6.5 Blockchain-Based Reviews
Technology: Ethereum / Polygon Feature: Verified, tamper-proof product reviews Benefit: Combat fake reviews

8.7 Revenue Projections
Year 1 (2026)
Revenue Source	Monthly	Annual
Affiliate Marketing	₹1,00,000	₹12,00,000
Subscriptions	₹3,50,000	₹42,00,000
Offer Assistance	₹2,00,000	₹24,00,000
Sponsored Products	₹1,00,000	₹12,00,000
Total	₹7,50,000	₹90,00,000
Year 2 (2027)
Revenue Source	Monthly	Annual
Affiliate Marketing	₹5,00,000	₹60,00,000
Subscriptions	₹10,00,000	₹1,20,00,000
Offer Assistance	₹8,00,000	₹96,00,000
Sponsored Products	₹5,00,000	₹60,00,000
B2B/API	₹3,00,000	₹36,00,000
Total	₹31,00,000	₹3,72,00,000
9. Deployment Guide
9.1 Local Development Setup
Prerequisites:

Python 3.14+
pip package manager
Git
Steps:

# Clone repository
git clone https://github.com/yourusername/smart-product-finder.git
cd smart-product-finder

# Install dependencies
pip install -r requirements.txt

# Configure API keys
# Edit api_keys_config.py and add your keys

# Run application
python web_app.py

# Open browser
http://localhost:5000
9.2 AWS Elastic Beanstalk Deployment
Prerequisites:

AWS account
AWS CLI installed
EB CLI installed
Steps:

# Initialize EB
eb init -p python-3.11 smart-product-finder

# Create environment
eb create smart-product-finder-prod

# Deploy
eb deploy

# Open application
eb open
Environment Variables:

eb setenv GEMINI_API_KEY=your_key_here
eb setenv SERPAPI_KEY=your_key_here
eb setenv AWS_REGION=us-east-1
9.3 Docker Deployment
Dockerfile:

FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "web_app:app"]
Docker Compose:

version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SERPAPI_KEY=${SERPAPI_KEY}
    volumes:
      - ./data:/app/data
Deploy:

docker-compose up -d
9.4 Production Considerations
Performance:

Use Gunicorn with 4-8 workers
Enable Redis caching
CDN for static files
Database for user data
Security:

HTTPS only
API rate limiting
Input validation
SQL injection prevention
XSS protection
Monitoring:

AWS CloudWatch
Sentry for error tracking
Google Analytics
Custom metrics dashboard
10. Development Roadmap
Q2 2026 (Apr-Jun)
✅ Launch MVP with basic search
✅ Mobile CPI integration
✅ AI chat assistant
🔄 Affiliate link integration
🔄 User authentication
🔄 Wishlist feature
Q3 2026 (Jul-Sep)
📋 Payment gateway integration
📋 Offer assistance service
📋 Price drop alerts
📋 Subscription tiers
📋 Mobile app (React Native)
📋 Advanced analytics
Q4 2026 (Oct-Dec)
📋 Visual search
📋 Voice search
📋 Browser extension
📋 API marketplace
📋 B2B partnerships
📋 International expansion
2027
📋 AR product preview
📋 Social shopping features
📋 Blockchain reviews
📋 AI personal shopper
📋 White-label platform
📋 IPO preparation
Conclusion
Smart Product Finder is positioned to revolutionize online shopping in India and globally by providing:

Unbiased Product Discovery: Aggregating multiple marketplaces
AI-Powered Intelligence: Smart recommendations and comparisons
Value Optimization: Helping users find best deals
Offer Accessibility: Bridging the gap for exclusive offers
Monetization Opportunities: Multiple revenue streams
Target Market Size:

India e-commerce: $84 billion (2024)
Global e-commerce: $6.3 trillion (2024)
Addressable market: 500 million+ online shoppers
Competitive Advantages:

Multi-marketplace aggregation
Proprietary CPI scoring
AI-powered recommendations
Offer assistance service (unique)
No marketplace bias
Next Steps:

Complete affiliate integrations
Launch payment gateway
Build user base (target: 100,000 users by Dec 2026)
Secure partnerships with marketplaces
Raise seed funding (₹2-5 crores)
Document Version: 2.0
Last Updated: March 7, 2026
Contact: [6766sankar@gmail.com]
Website: [productfinderai.org]

End of Documentation

