# Design Document
## Global Product Search - AI-Powered Smart Shopping Assistant

**Version:** 1.0  
**Date:** February 2026  
**Status:** Production Ready

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Component Design](#2-component-design)
3. [Database Design](#3-database-design)
4. [API Design](#4-api-design)
5. [Algorithm Design](#5-algorithm-design)
6. [UI/UX Design](#6-uiux-design)
7. [Security Design](#7-security-design)
8. [Performance Design](#8-performance-design)
9. [Deployment Architecture](#9-deployment-architecture)
10. [Data Flow](#10-data-flow)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Web App    │  │ Mobile App   │  │   Browser    │         │
│  │  (HTML/CSS)  │  │   (Future)   │  │  Extension   │         │
│  │  JavaScript  │  │              │  │   (Future)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Flask Web Server (Python)                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │   REST     │  │   CORS     │  │   Session  │         │  │
│  │  │   API      │  │  Handler   │  │   Manager  │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BUSINESS LOGIC LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Product    │  │    Budget    │  │     Geo      │         │
│  │    Search    │  │   Advisor    │  │  Marketplace │         │
│  │    Engine    │  │              │  │    Config    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Ranking    │  │   Filtering  │  │   Export     │         │
│  │  Algorithm   │  │   & Sorting  │  │   Handler    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA ACCESS LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │    Redis     │  │   MongoDB    │         │
│  │  (Products)  │  │   (Cache)    │  │ (Analytics)  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES LAYER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   SerpAPI    │  │   Amazon     │  │     eBay     │         │
│  │   (Google    │  │   Product    │  │   Finding    │         │
│  │  Shopping)   │  │     API      │  │     API      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Walmart    │  │   MaxMind    │  │   Sentry     │         │
│  │     API      │  │    GeoIP     │  │   (Error     │         │
│  │              │  │              │  │  Tracking)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Patterns

**Pattern:** Layered Architecture (N-Tier)

**Layers:**
1. **Presentation Layer:** HTML/CSS/JavaScript frontend
2. **Application Layer:** Flask REST API
3. **Business Logic Layer:** Core algorithms and services
4. **Data Access Layer:** Database and cache management
5. **External Services Layer:** Third-party API integrations

**Benefits:**
- Clear separation of concerns
- Easy to test and maintain
- Scalable and modular
- Technology-agnostic layers

### 1.3 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML5, CSS3, JavaScript ES6+ | User interface |
| Backend | Python 3.11+, Flask 3.0 | API server |
| Database | PostgreSQL 14+ | Relational data |
| Cache | Redis 7+ | Performance optimization |
| Analytics | MongoDB 6+ | Unstructured data |
| APIs | SerpAPI, Amazon, eBay | Product data |
| Deployment | Docker, Nginx, Gunicorn | Production hosting |

---

## 2. Component Design

### 2.1 Core Components

#### 2.1.1 Product Search Engine (`smart_product_finder.py`)

**Purpose:** Core search functionality with intelligent ranking

**Class:** `ProductSearchEngine`

**Key Methods:**

```python
async def search(query: str, max_results: int) -> List[ProductHit]
    """Main search method - coordinates all search operations"""
    
def _enhance_query(query: str) -> str
    """AI-powered query enhancement"""
    
async def _search_source(source: str, query: str) -> List[ProductHit]
    """Search individual marketplace"""
    
def _rank_products(hits: List[ProductHit]) -> List[ProductHit]
    """Apply ranking algorithm to results"""
```

**Data Structure:**
```python
@dataclass
class ProductHit:
    title: str
    price: float
    currency: str
    url: str
    source: str
    seller_name: Optional[str]
    seller_rating: Optional[float]
    product_rating: Optional[float]
    review_count: int
    image_url: Optional[str]
    description: Optional[str]
    trust_score: float
    quality_score: float
    value_score: float
    overall_rank: float
```

**Design Decisions:**
- Async/await for concurrent marketplace searches
- Dataclass for type safety and clarity
- Modular scoring system for easy adjustment
- Mock data generation for development/testing

#### 2.1.2 Geo-Aware Search Engine (`geo_product_finder.py`)

**Purpose:** Country-specific marketplace search

**Class:** `GeoProductSearchEngine`

**Key Methods:**
```python
def __init__(country_code: Optional[str], auto_detect: bool)
    """Initialize with country-specific configuration"""
    
async def search(query: str, max_results: int) -> List[ProductHit]
    """Search country-specific marketplaces"""
    
def get_location_info() -> dict
    """Return current location configuration"""
```

**Design Decisions:**
- Automatic country detection via IP geolocation
- Currency-aware pricing and display
- Marketplace trust scores per country
- Fallback to US if country not supported


#### 2.1.3 Marketplace Configuration (`geo_marketplace_config.py`)

**Purpose:** Centralized marketplace database

**Class:** `GeoMarketplaceConfig`

**Data Structure:**
```python
@dataclass
class Marketplace:
    name: str
    domain: str
    country_code: str
    country_name: str
    currency: str
    trust_score: float
    popular: bool
```

**Key Methods:**
```python
@classmethod
def get_marketplaces_for_country(country_code: str, popular_only: bool)
    """Get marketplaces for specific country"""
    
@classmethod
def get_all_supported_countries() -> List[Dict]
    """List all supported countries"""
    
@classmethod
def get_currency_symbol(currency_code: str) -> str
    """Get currency symbol for display"""
```

**Supported Countries:** 15+ (India, US, UK, Canada, Australia, Germany, France, Japan, China, UAE, Singapore, Brazil, Mexico, etc.)

**Total Marketplaces:** 100+

#### 2.1.4 Budget Advisor (`budget_advisor.py`)

**Purpose:** Intelligent budget analysis and recommendations

**Class:** `BudgetAdvisor`

**Data Structure:**
```python
@dataclass
class BudgetAnalysis:
    budget: float
    currency: str
    within_budget: List[ProductHit]
    best_in_budget: Optional[ProductHit]
    avg_score_in_budget: float
    budget_quality: str
    has_better_deals: bool
    recommended_products: List[ProductHit]
    recommended_budget: Optional[float]
    savings_message: Optional[str]
    upgrade_message: Optional[str]
```

**Key Methods:**
```python
def analyze_budget(products: List[ProductHit], budget: float, currency: str)
    """Comprehensive budget analysis"""
    
def get_budget_warning(analysis: BudgetAnalysis) -> Optional[Dict]
    """Generate warnings for low-quality options"""
    
def format_analysis_for_display(analysis: BudgetAnalysis) -> Dict
    """Format for web display"""
```


**Algorithm Parameters:**
- Budget flexibility: 40% above budget
- Minimum score improvement: 15 points
- Savings threshold: 25% below budget
- Quality thresholds:
  - Excellent: ≥85
  - Good: ≥75
  - Fair: ≥65
  - Poor: <65

#### 2.1.5 Web Application (`web_app.py`)

**Purpose:** Flask REST API server

**Key Routes:**
```python
GET  /                              # Serve main page
GET  /api/countries                 # List supported countries
GET  /api/marketplaces/<code>       # Get country marketplaces
POST /api/search                    # Search products
POST /api/filter                    # Filter results
POST /api/sort                      # Sort results
```

**Design Decisions:**
- RESTful API design
- CORS enabled for cross-origin requests
- Async event loop integration
- JSON response format
- Error handling with proper HTTP status codes

---

## 3. Database Design

### 3.1 PostgreSQL Schema (Future Implementation)

#### 3.1.1 Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    country_code CHAR(2),
    preferred_currency CHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_country ON users(country_code);
```

#### 3.1.2 Products Table
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    external_id VARCHAR(255),
    title TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    marketplace_id INTEGER REFERENCES marketplaces(marketplace_id),
    url TEXT NOT NULL,
    image_url TEXT,
    product_rating DECIMAL(3, 2),
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_products_marketplace ON products(marketplace_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_rating ON products(product_rating);
CREATE INDEX idx_products_external ON products(external_id);
```


#### 3.1.3 Marketplaces Table
```sql
CREATE TABLE marketplaces (
    marketplace_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    country_code CHAR(2) NOT NULL,
    currency CHAR(3) NOT NULL,
    trust_score DECIMAL(3, 2) NOT NULL,
    is_popular BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_marketplaces_country ON marketplaces(country_code);
CREATE INDEX idx_marketplaces_domain ON marketplaces(domain);
```

#### 3.1.4 Search History Table
```sql
CREATE TABLE search_history (
    search_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    query TEXT NOT NULL,
    country_code CHAR(2),
    results_count INTEGER,
    budget DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_date ON search_history(created_at);
```

#### 3.1.5 Saved Products Table
```sql
CREATE TABLE saved_products (
    saved_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    product_id INTEGER REFERENCES products(product_id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_saved_user ON saved_products(user_id);
CREATE INDEX idx_saved_product ON saved_products(product_id);
```

### 3.2 Redis Cache Design

**Purpose:** High-performance caching for frequently accessed data

**Cache Keys:**
```
search:{country_code}:{query_hash}        # Search results (TTL: 1 hour)
marketplaces:{country_code}               # Country marketplaces (TTL: 24 hours)
product:{product_id}                      # Product details (TTL: 6 hours)
user:session:{session_id}                 # User sessions (TTL: 24 hours)
rate_limit:{ip_address}                   # Rate limiting (TTL: 1 minute)
```

**Cache Strategy:**
- Cache-aside pattern
- TTL-based expiration
- LRU eviction policy
- Automatic cache warming for popular queries


### 3.3 MongoDB Collections (Analytics)

#### 3.3.1 Search Analytics
```javascript
{
  _id: ObjectId,
  timestamp: ISODate,
  query: String,
  country_code: String,
  user_id: Number,
  results_count: Number,
  avg_price: Number,
  currency: String,
  click_through_rate: Number,
  session_id: String
}
```

#### 3.3.2 User Behavior
```javascript
{
  _id: ObjectId,
  user_id: Number,
  session_id: String,
  events: [
    {
      type: String,  // 'search', 'click', 'filter', 'sort'
      timestamp: ISODate,
      data: Object
    }
  ],
  device_info: {
    browser: String,
    os: String,
    screen_size: String
  }
}
```

---

## 4. API Design

### 4.1 REST API Endpoints

#### 4.1.1 GET /api/countries

**Description:** Get list of all supported countries

**Request:** None

**Response:**
```json
{
  "success": true,
  "countries": [
    {
      "code": "IN",
      "name": "India",
      "currency": "INR",
      "marketplace_count": 12
    },
    {
      "code": "US",
      "name": "United States",
      "currency": "USD",
      "marketplace_count": 10
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 500: Server error

#### 4.1.2 GET /api/marketplaces/:country_code

**Description:** Get marketplaces for specific country

**Parameters:**
- `country_code` (path): ISO 3166-1 alpha-2 code

**Response:**
```json
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
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 404: Country not found
- 500: Server error


#### 4.1.3 POST /api/search

**Description:** Search for products

**Request Body:**
```json
{
  "query": "wireless headphones",
  "country_code": "IN",
  "max_results": 20,
  "budget": 5000
}
```

**Response:**
```json
{
  "success": true,
  "query": "wireless headphones",
  "country_code": "IN",
  "country_name": "India",
  "currency": "INR",
  "currency_symbol": "₹",
  "total_results": 45,
  "results": [
    {
      "title": "Sony WH-1000XM5",
      "price": 29990.00,
      "currency": "INR",
      "url": "https://amazon.in/...",
      "source": "Amazon India",
      "seller_name": "Sony Official",
      "seller_rating": 4.8,
      "product_rating": 4.7,
      "review_count": 2543,
      "image_url": "https://...",
      "trust_score": 92.5,
      "quality_score": 88.3,
      "value_score": 75.2,
      "overall_rank": 85.3
    }
  ],
  "budget_analysis": {
    "budget": 5000,
    "currency": "INR",
    "currency_symbol": "₹",
    "products_in_budget": 12,
    "avg_score": 68.5,
    "budget_quality": "fair",
    "quality_label": "😐 Fair Deals",
    "quality_color": "#f59e0b",
    "warning": {
      "type": "info",
      "title": "ℹ️ Fair Quality Products",
      "message": "Products within your budget...",
      "severity": "medium"
    },
    "has_recommendations": true,
    "recommended_products": [
      {
        "title": "Product Name",
        "price": 6500,
        "score": 85,
        "url": "https://...",
        "price_diff": 1500,
        "score_improvement": 18
      }
    ]
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request
- 500: Server error


#### 4.1.4 POST /api/filter

**Description:** Filter search results

**Request Body:**
```json
{
  "results": [...],
  "filter_type": "price",
  "filter_value": {
    "min": 1000,
    "max": 5000
  }
}
```

**Filter Types:**
- `price`: Filter by price range
- `source`: Filter by marketplace
- `rating`: Filter by minimum rating

**Response:**
```json
{
  "success": true,
  "filtered_results": [...],
  "count": 15
}
```

#### 4.1.5 POST /api/sort

**Description:** Sort search results

**Request Body:**
```json
{
  "results": [...],
  "sort_by": "price",
  "order": "asc"
}
```

**Sort Options:**
- `overall_rank`: Best match (default)
- `price`: Price
- `rating`: Product rating
- `trust`: Trust score
- `quality`: Quality score
- `value`: Value score

**Order:**
- `asc`: Ascending
- `desc`: Descending

**Response:**
```json
{
  "success": true,
  "sorted_results": [...]
}
```

### 4.2 API Error Handling

**Error Response Format:**
```json
{
  "success": false,
  "error": "Error message",
  "error_code": "ERROR_CODE",
  "details": {}
}
```

**Common Error Codes:**
- `INVALID_REQUEST`: Malformed request
- `MISSING_PARAMETER`: Required parameter missing
- `INVALID_COUNTRY`: Country not supported
- `SEARCH_FAILED`: Search operation failed
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## 5. Algorithm Design

### 5.1 Ranking Algorithm

**Purpose:** Calculate overall product ranking based on multiple factors


#### 5.1.1 Trust Score Algorithm

**Formula:**
```
Trust Score = (Seller Rating × 0.40) + (Review Count × 0.30) + (Marketplace Trust × 0.30)
```

**Components:**

1. **Seller Rating Component (40%)**
   ```
   Seller Component = (seller_rating / 5.0) × 40
   ```
   - Normalized to 0-40 scale
   - Based on seller's overall rating

2. **Review Count Component (30%)**
   ```
   Review Component = min(log10(review_count + 1) / 4, 1.0) × 30
   ```
   - Logarithmic scale to prevent bias toward high counts
   - Normalized to 0-30 scale
   - More reviews = higher reliability

3. **Marketplace Trust Component (30%)**
   ```
   Marketplace Component = marketplace_trust_score × 30
   ```
   - Predefined trust scores per marketplace
   - Amazon: 0.95, Walmart: 0.90, eBay: 0.75, etc.
   - Normalized to 0-30 scale

**Example Calculation:**
```
Product: Sony Headphones
- Seller Rating: 4.8/5.0
- Review Count: 2543
- Marketplace: Amazon (trust: 0.95)

Seller Component = (4.8 / 5.0) × 40 = 38.4
Review Component = min(log10(2544) / 4, 1.0) × 30 = 0.85 × 30 = 25.5
Marketplace Component = 0.95 × 30 = 28.5

Trust Score = 38.4 + 25.5 + 28.5 = 92.4/100
```

#### 5.1.2 Quality Score Algorithm

**Formula:**
```
Quality Score = (Product Rating × 0.60) + (Review Reliability × 0.40)
```

**Components:**

1. **Product Rating Component (60%)**
   ```
   Rating Component = (product_rating / 5.0) × 60
   ```
   - Direct product rating
   - Normalized to 0-60 scale

2. **Review Reliability Component (40%)**
   ```
   Reliability Component = min(log10(review_count + 1) / 4, 1.0) × 40
   ```
   - More reviews = more reliable rating
   - Logarithmic scale
   - Normalized to 0-40 scale

**Example Calculation:**
```
Product: Sony Headphones
- Product Rating: 4.7/5.0
- Review Count: 2543

Rating Component = (4.7 / 5.0) × 60 = 56.4
Reliability Component = min(log10(2544) / 4, 1.0) × 40 = 0.85 × 40 = 34.0

Quality Score = 56.4 + 34.0 = 90.4/100
```


#### 5.1.3 Value Score Algorithm

**Formula:**
```
Value Score = (1 - normalized_price) × 100
```

**Calculation:**
```
normalized_price = (product_price - min_price) / (max_price - min_price)
```

**Logic:**
- Lower price = higher value score
- Normalized across all results in same currency
- Inverted scale (0 = most expensive, 100 = cheapest)

**Example Calculation:**
```
Products in INR:
- Product A: ₹2000
- Product B: ₹5000 (target)
- Product C: ₹8000

min_price = 2000
max_price = 8000

For Product B:
normalized = (5000 - 2000) / (8000 - 2000) = 3000 / 6000 = 0.5
Value Score = (1 - 0.5) × 100 = 50/100
```

#### 5.1.4 Overall Rank Algorithm

**Formula:**
```
Overall Rank = (Trust × 0.30) + (Quality × 0.35) + (Value × 0.35)
```

**Weights Rationale:**
- **Trust (30%):** Important but not dominant
- **Quality (35%):** Slightly higher priority
- **Value (35%):** Price competitiveness matters

**Example Calculation:**
```
Product: Sony Headphones
- Trust Score: 92.4
- Quality Score: 90.4
- Value Score: 50.0

Overall Rank = (92.4 × 0.30) + (90.4 × 0.35) + (50.0 × 0.35)
             = 27.72 + 31.64 + 17.50
             = 76.86/100
```

### 5.2 Budget Advisor Algorithm

#### 5.2.1 Budget Quality Assessment

**Thresholds:**
```python
EXCELLENT_SCORE = 85
GOOD_SCORE = 75
FAIR_SCORE = 65
POOR_SCORE = 50
```

**Logic:**
```
if best_score >= 85:
    quality = "excellent"
elif best_score >= 75:
    quality = "good"
elif best_score >= 65:
    quality = "fair"
else:
    quality = "poor"
```

#### 5.2.2 Smart Recommendation Algorithm

**Parameters:**
```python
BUDGET_FLEXIBILITY = 0.40  # 40% above budget
MIN_SCORE_IMPROVEMENT = 15  # Minimum 15-point improvement
```

**Logic:**
```
max_recommended_price = budget × (1 + BUDGET_FLEXIBILITY)

for product in products:
    if budget < product.price <= max_recommended_price:
        if product.score >= best_in_budget.score + MIN_SCORE_IMPROVEMENT:
            recommendations.append(product)
```


**Example:**
```
Budget: ₹5000
Best in Budget: Score 68
Flexibility: 40%
Max Price: ₹7000

Product at ₹6500 with score 85:
- Within flexibility range: ✓
- Score improvement: 85 - 68 = 17 points ✓
- Recommend: YES
```

#### 5.2.3 Savings Opportunity Algorithm

**Parameters:**
```python
SAVINGS_THRESHOLD = 0.25  # 25% below budget
MIN_QUALITY_SCORE = 75    # Minimum acceptable quality
```

**Logic:**
```
savings_price_limit = budget × (1 - SAVINGS_THRESHOLD)

for product in products:
    if product.price <= savings_price_limit:
        if product.score >= MIN_QUALITY_SCORE:
            savings_opportunities.append(product)
```

**Example:**
```
Budget: ₹5000
Savings Threshold: 25%
Max Savings Price: ₹3750

Product at ₹3200 with score 82:
- Below threshold: ✓
- Quality acceptable: ✓
- Savings: ₹1800 (36%)
- Recommend: YES
```

---

## 6. UI/UX Design

### 6.1 Design Principles

1. **Minimalism:** Clean, uncluttered interface
2. **Clarity:** Clear information hierarchy
3. **Responsiveness:** Works on all devices
4. **Speed:** Fast interactions and feedback
5. **Accessibility:** WCAG 2.1 AA compliant

### 6.2 Color Palette

```css
/* Primary Colors */
--primary-blue: #3b82f6;
--primary-dark: #1e40af;
--primary-light: #93c5fd;

/* Semantic Colors */
--success-green: #10b981;
--warning-orange: #f59e0b;
--error-red: #ef4444;
--info-blue: #3b82f6;

/* Neutral Colors */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-600: #4b5563;
--gray-900: #111827;

/* Score Colors */
--score-excellent: #10b981;  /* Green */
--score-good: #3b82f6;       /* Blue */
--score-fair: #f59e0b;       /* Orange */
--score-poor: #ef4444;       /* Red */
```

### 6.3 Typography

```css
/* Font Family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```


### 6.4 Component Design

#### 6.4.1 Search Bar Component

**Structure:**
```html
<div class="search-container">
  <select class="country-selector">
    <option value="IN">🇮🇳 India (INR)</option>
    <option value="US">🇺🇸 United States (USD)</option>
  </select>
  <input type="text" class="search-input" placeholder="Search products...">
  <input type="number" class="budget-input" placeholder="Budget (optional)">
  <button class="search-button">Search</button>
</div>
```

**Styling:**
- Rounded corners (8px)
- Shadow for depth
- Hover states
- Focus indicators
- Responsive layout

#### 6.4.2 Product Card Component

**Structure:**
```html
<div class="product-card">
  <div class="product-rank">#1</div>
  <img class="product-image" src="...">
  <div class="product-info">
    <h3 class="product-title">Product Name</h3>
    <div class="product-price">₹29,990</div>
    <div class="product-source">Amazon India</div>
    <div class="product-rating">⭐⭐⭐⭐⭐ 4.7 (2,543)</div>
  </div>
  <div class="product-scores">
    <div class="score-bar trust">Trust: 92/100</div>
    <div class="score-bar quality">Quality: 88/100</div>
    <div class="score-bar value">Value: 75/100</div>
    <div class="score-overall">Overall: 85/100</div>
  </div>
  <a href="..." class="product-link">View Product →</a>
</div>
```

**Visual Features:**
- Card elevation
- Hover effects
- Color-coded scores
- Visual score bars
- Responsive grid layout

#### 6.4.3 Budget Analysis Component

**Structure:**
```html
<div class="budget-analysis">
  <div class="budget-header">
    <h3>Budget Analysis</h3>
    <div class="budget-amount">₹5,000</div>
  </div>
  <div class="budget-stats">
    <div class="stat">Products in Budget: 12</div>
    <div class="stat">Average Score: 68.5</div>
    <div class="stat quality-fair">Quality: Fair</div>
  </div>
  <div class="budget-warning">
    <div class="warning-icon">⚠️</div>
    <div class="warning-message">...</div>
  </div>
  <div class="budget-recommendations">
    <h4>Smart Recommendations</h4>
    <div class="recommendation-card">...</div>
  </div>
</div>
```

### 6.5 Responsive Breakpoints

```css
/* Mobile First Approach */
/* Mobile: < 768px (default) */
/* Tablet: 768px - 1023px */
@media (min-width: 768px) { ... }

/* Desktop: 1024px - 1279px */
@media (min-width: 1024px) { ... }

/* Large Desktop: ≥ 1280px */
@media (min-width: 1280px) { ... }
```

