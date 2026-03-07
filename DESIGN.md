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


### 6.6 Interaction Design

#### 6.6.1 Loading States

**Search Loading:**
```html
<div class="loading-spinner">
  <div class="spinner"></div>
  <p>Searching marketplaces...</p>
</div>
```

**Skeleton Screens:**
- Show placeholder cards while loading
- Smooth transition to actual content
- Prevents layout shift

#### 6.6.2 Animations

```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Slide In */
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

/* Pulse (for loading) */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

**Usage:**
- Card entrance: fadeIn 0.3s ease-out
- Modal appearance: slideIn 0.2s ease-out
- Loading states: pulse 1.5s infinite

#### 6.6.3 Micro-interactions

- Button hover: Scale 1.02, shadow increase
- Card hover: Elevation increase, border highlight
- Input focus: Border color change, glow effect
- Score bars: Animated fill on load
- Success feedback: Checkmark animation

---

## 7. Security Design

### 7.1 Authentication & Authorization (Future)

#### 7.1.1 Password Security

**Hashing:**
```python
import bcrypt

# Hash password
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

# Verify password
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

**Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

#### 7.1.2 Session Management

**JWT Tokens:**
```python
import jwt
from datetime import datetime, timedelta

# Generate token
payload = {
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=24),
    'iat': datetime.utcnow()
}
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Verify token
decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
```

**Token Storage:**
- HttpOnly cookies (preferred)
- LocalStorage (alternative)
- Secure flag enabled
- SameSite=Strict


### 7.2 API Security

#### 7.2.1 Rate Limiting

**Implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)

@app.route('/api/search')
@limiter.limit("10 per minute")
def search():
    pass
```

**Limits:**
- Search: 10 requests/minute
- General API: 100 requests/hour
- Anonymous users: Stricter limits
- Authenticated users: Higher limits

#### 7.2.2 Input Validation

**Validation Rules:**
```python
from flask import request
import re

def validate_search_query(query):
    # Length check
    if len(query) < 2 or len(query) > 200:
        raise ValueError("Query must be 2-200 characters")
    
    # SQL injection prevention
    dangerous_patterns = [';', '--', '/*', '*/', 'xp_', 'sp_']
    if any(pattern in query.lower() for pattern in dangerous_patterns):
        raise ValueError("Invalid characters in query")
    
    return True

def validate_country_code(code):
    # Must be 2-letter ISO code
    if not re.match(r'^[A-Z]{2}$', code):
        raise ValueError("Invalid country code")
    
    return True
```

#### 7.2.3 CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
    }
})
```

### 7.3 Data Security

#### 7.3.1 HTTPS/TLS

**Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

#### 7.3.2 API Key Management

**Environment Variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv('SERPAPI_KEY')
AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
```

**Never commit:**
- API keys
- Database credentials
- Secret keys
- Private certificates


#### 7.3.3 XSS Prevention

**Output Escaping:**
```python
from markupsafe import escape

# Escape user input
safe_query = escape(user_query)

# Use Jinja2 auto-escaping
{{ user_input }}  # Automatically escaped
{{ user_input | safe }}  # Only when absolutely necessary
```

**Content Security Policy:**
```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
        "font-src 'self' fonts.gstatic.com; "
        "img-src 'self' data: https:;"
    )
    return response
```

#### 7.3.4 SQL Injection Prevention

**Parameterized Queries:**
```python
# BAD - Vulnerable to SQL injection
query = f"SELECT * FROM products WHERE title = '{user_input}'"

# GOOD - Parameterized query
query = "SELECT * FROM products WHERE title = %s"
cursor.execute(query, (user_input,))
```

**ORM Usage:**
```python
# Using SQLAlchemy ORM
products = Product.query.filter_by(title=user_input).all()
```

---

## 8. Performance Design

### 8.1 Caching Strategy

#### 8.1.1 Redis Caching

**Cache Layers:**
```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(cache_key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

@cache_result(ttl=3600)
def search_products(query, country_code):
    # Expensive operation
    pass
```

**Cache Invalidation:**
- Time-based expiration (TTL)
- Manual invalidation on data updates
- Cache warming for popular queries


#### 8.1.2 Browser Caching

**HTTP Headers:**
```python
@app.after_request
def add_cache_headers(response):
    # Static assets - long cache
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    
    # API responses - short cache
    elif request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'private, max-age=300'
    
    return response
```

### 8.2 Database Optimization

#### 8.2.1 Indexing Strategy

**Primary Indexes:**
```sql
-- Frequently queried columns
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_rating ON products(product_rating);
CREATE INDEX idx_products_marketplace ON products(marketplace_id);

-- Composite indexes for common queries
CREATE INDEX idx_products_marketplace_price 
ON products(marketplace_id, price);

CREATE INDEX idx_products_country_rating 
ON products(country_code, product_rating DESC);
```

#### 8.2.2 Query Optimization

**Use EXPLAIN:**
```sql
EXPLAIN ANALYZE
SELECT * FROM products 
WHERE marketplace_id = 1 
AND price BETWEEN 1000 AND 5000
ORDER BY product_rating DESC
LIMIT 20;
```

**Pagination:**
```sql
-- Efficient pagination with cursor
SELECT * FROM products
WHERE id > last_seen_id
ORDER BY id
LIMIT 20;

-- Instead of OFFSET (slow for large offsets)
SELECT * FROM products
ORDER BY id
LIMIT 20 OFFSET 10000;  -- Slow!
```

### 8.3 Frontend Optimization

#### 8.3.1 Asset Optimization

**Minification:**
```bash
# CSS minification
cssnano style.css -o style.min.css

# JavaScript minification
terser app.js -o app.min.js -c -m
```

**Image Optimization:**
- Use WebP format
- Lazy loading for images
- Responsive images with srcset
- CDN for static assets

#### 8.3.2 Code Splitting

**Lazy Loading:**
```javascript
// Load components on demand
const loadBudgetAnalyzer = () => {
    return import('./budget-analyzer.js');
};

// Load when needed
button.addEventListener('click', async () => {
    const module = await loadBudgetAnalyzer();
    module.analyze();
});
```

#### 8.3.3 Debouncing & Throttling

**Search Input Debouncing:**
```javascript
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Apply to search input
searchInput.addEventListener('input', debounce(performSearch, 500));
```


### 8.4 Async Operations

#### 8.4.1 Concurrent Marketplace Searches

**AsyncIO Implementation:**
```python
import asyncio
import aiohttp

async def search_marketplace(session, marketplace, query):
    async with session.get(marketplace.api_url, params={'q': query}) as response:
        return await response.json()

async def search_all_marketplaces(marketplaces, query):
    async with aiohttp.ClientSession() as session:
        tasks = [
            search_marketplace(session, marketplace, query)
            for marketplace in marketplaces
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
```

**Benefits:**
- Parallel API calls
- Reduced total search time
- Better resource utilization

---

## 9. Deployment Architecture

### 9.1 Production Environment

#### 9.1.1 Server Stack

```
┌─────────────────────────────────────────────────────────────┐
│                         INTERNET                             │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE CDN                          │
│                   (SSL, DDoS Protection)                     │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                           │
│                    (AWS ELB / Nginx)                         │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVERS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Server 1   │  │   Server 2   │  │   Server 3   │      │
│  │   Nginx +    │  │   Nginx +    │  │   Nginx +    │      │
│  │  Gunicorn    │  │  Gunicorn    │  │  Gunicorn    │      │
│  │   Flask      │  │   Flask      │  │   Flask      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │   MongoDB    │      │
│  │   Primary    │  │    Cache     │  │  Analytics   │      │
│  │  + Replica   │  │   Cluster    │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

#### 9.1.2 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "web_app:app"]
```


**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/products
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: always

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=products
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
```

#### 9.1.3 Nginx Configuration

**nginx.conf:**
```nginx
upstream flask_app {
    server web:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API requests
    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 9.2 CI/CD Pipeline

#### 9.2.1 GitHub Actions Workflow

**.github/workflows/deploy.yml:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            git pull
            docker-compose down
            docker-compose up -d --build
```


### 9.3 Monitoring & Logging

#### 9.3.1 Application Monitoring

**Sentry Integration:**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,
    environment="production"
)
```

**Custom Logging:**
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler(
    'app.log',
    maxBytes=10000000,
    backupCount=5
)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Usage
app.logger.info(f"Search performed: {query}")
app.logger.error(f"API error: {error}")
```

#### 9.3.2 Performance Monitoring

**New Relic / DataDog:**
```python
# New Relic
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

@newrelic.agent.background_task()
def search_products(query):
    pass

# Custom metrics
newrelic.agent.record_custom_metric('Search/Duration', duration)
newrelic.agent.record_custom_metric('Search/ResultCount', count)
```

#### 9.3.3 Health Checks

**Endpoint:**
```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'external_apis': check_apis()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code

def check_database():
    try:
        db.session.execute('SELECT 1')
        return True
    except:
        return False

def check_redis():
    try:
        redis_client.ping()
        return True
    except:
        return False
```

---

## 10. Data Flow

### 10.1 Search Flow

```
User Input
    ↓
[1] User enters query + country + budget
    ↓
[2] Frontend validates input
    ↓
[3] POST /api/search
    ↓
[4] Flask receives request
    ↓
[5] Check Redis cache
    ├─ Cache Hit → Return cached results
    └─ Cache Miss → Continue
    ↓
[6] Initialize GeoProductSearchEngine(country_code)
    ↓
[7] Get marketplaces for country
    ↓
[8] Async search all marketplaces (parallel)
    ├─ Search Marketplace 1
    ├─ Search Marketplace 2
    ├─ Search Marketplace 3
    └─ ...
    ↓
[9] Aggregate all results
    ↓
[10] Calculate scores for each product
    ├─ Trust Score
    ├─ Quality Score
    └─ Value Score
    ↓
[11] Calculate overall rank
    ↓
[12] Sort by overall rank
    ↓
[13] If budget provided:
    ├─ Run BudgetAdvisor.analyze_budget()
    ├─ Find products in budget
    ├─ Generate recommendations
    └─ Create warnings
    ↓
[14] Cache results in Redis
    ↓
[15] Return JSON response
    ↓
[16] Frontend receives data
    ↓
[17] Render product cards
    ↓
[18] Display budget analysis (if applicable)
    ↓
User sees results
```


### 10.2 Budget Analysis Flow

```
Search Results + Budget
    ↓
[1] BudgetAdvisor.analyze_budget(products, budget, currency)
    ↓
[2] Filter products within budget
    ↓
[3] Calculate average score in budget
    ↓
[4] Find best product in budget
    ↓
[5] Assess budget quality
    ├─ Excellent (≥85)
    ├─ Good (≥75)
    ├─ Fair (≥65)
    └─ Poor (<65)
    ↓
[6] Find products up to 40% above budget
    ↓
[7] Filter for significant improvements (≥15 points)
    ↓
[8] Sort by score and price
    ↓
[9] Select top 3 recommendations
    ↓
[10] Generate upgrade message
    ↓
[11] Find savings opportunities (25% below budget)
    ↓
[12] Filter for quality (≥75 score)
    ↓
[13] Generate savings message
    ↓
[14] Create warnings if needed
    ↓
[15] Format for display
    ↓
Return BudgetAnalysis object
```

### 10.3 Ranking Flow

```
Raw Product Data
    ↓
[1] For each product:
    ↓
[2] Calculate Trust Score
    ├─ Seller Rating × 0.40
    ├─ Review Count (log scale) × 0.30
    └─ Marketplace Trust × 0.30
    ↓
[3] Calculate Quality Score
    ├─ Product Rating × 0.60
    └─ Review Reliability × 0.40
    ↓
[4] Calculate Value Score
    ├─ Get all prices in same currency
    ├─ Find min and max
    ├─ Normalize product price
    └─ Invert (lower price = higher score)
    ↓
[5] Calculate Overall Rank
    ├─ Trust × 0.30
    ├─ Quality × 0.35
    └─ Value × 0.35
    ↓
[6] Sort all products by Overall Rank (descending)
    ↓
Ranked Product List
```

---

## 11. Scalability Considerations

### 11.1 Horizontal Scaling

**Load Balancing:**
- Multiple application server instances
- Round-robin or least-connections algorithm
- Session affinity if needed
- Health check-based routing

**Database Scaling:**
- Read replicas for query distribution
- Write to primary, read from replicas
- Connection pooling
- Query result caching

### 11.2 Vertical Scaling

**Resource Optimization:**
- Increase server CPU/RAM as needed
- Optimize database queries
- Reduce memory footprint
- Profile and optimize bottlenecks

### 11.3 Microservices (Future)

**Service Decomposition:**
```
┌─────────────────┐
│  API Gateway    │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ Search │ │Budget│ │ User │ │ Auth │ │ Data │
│Service │ │Service│ │Service│ │Service│ │Service│
└────────┘ └──────┘ └──────┘ └──────┘ └──────┘
```

**Benefits:**
- Independent scaling
- Technology flexibility
- Fault isolation
- Easier maintenance


---

## 12. Testing Strategy

### 12.1 Unit Testing

**Test Structure:**
```python
import pytest
from smart_product_finder import ProductSearchEngine, ProductHit

class TestProductSearchEngine:
    def setup_method(self):
        self.engine = ProductSearchEngine()
    
    def test_enhance_query(self):
        result = self.engine._enhance_query("laptop")
        assert "laptop computer notebook" in result
    
    def test_calculate_trust_score(self):
        hit = ProductHit(
            title="Test Product",
            price=100,
            currency="USD",
            url="https://test.com",
            source="Amazon",
            seller_rating=4.5,
            review_count=1000
        )
        score = self.engine._calculate_trust_score(hit)
        assert 0 <= score <= 100
        assert score > 80  # High trust expected
    
    def test_rank_products(self):
        hits = [
            ProductHit(...),  # Low score product
            ProductHit(...),  # High score product
        ]
        ranked = self.engine._rank_products(hits)
        assert ranked[0].overall_rank > ranked[1].overall_rank
```

**Coverage Target:** 80%+

### 12.2 Integration Testing

**API Testing:**
```python
import pytest
from web_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_endpoint(client):
    response = client.post('/api/search', json={
        'query': 'headphones',
        'country_code': 'US',
        'max_results': 10
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'results' in data
    assert len(data['results']) > 0

def test_invalid_country(client):
    response = client.post('/api/search', json={
        'query': 'headphones',
        'country_code': 'XX'
    })
    assert response.status_code == 400
```

### 12.3 Performance Testing

**Load Testing with Locust:**
```python
from locust import HttpUser, task, between

class ProductSearchUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def search_products(self):
        self.client.post("/api/search", json={
            "query": "wireless headphones",
            "country_code": "US",
            "max_results": 20
        })
    
    @task(1)
    def get_countries(self):
        self.client.get("/api/countries")
```

**Performance Targets:**
- 100 concurrent users
- < 3 second response time
- < 1% error rate

### 12.4 End-to-End Testing

**Selenium/Playwright:**
```python
from playwright.sync_api import sync_playwright

def test_complete_search_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to app
        page.goto("http://localhost:5000")
        
        # Select country
        page.select_option("#country-select", "IN")
        
        # Enter search query
        page.fill("#search-input", "wireless headphones")
        
        # Enter budget
        page.fill("#budget-input", "5000")
        
        # Click search
        page.click("#search-button")
        
        # Wait for results
        page.wait_for_selector(".product-card")
        
        # Verify results
        cards = page.query_selector_all(".product-card")
        assert len(cards) > 0
        
        # Verify budget analysis
        budget_analysis = page.query_selector(".budget-analysis")
        assert budget_analysis is not None
        
        browser.close()
```

---

## 13. Error Handling

### 13.1 Error Categories

**Client Errors (4xx):**
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 403 Forbidden: Access denied
- 404 Not Found: Resource not found
- 429 Too Many Requests: Rate limit exceeded

**Server Errors (5xx):**
- 500 Internal Server Error: Unexpected error
- 502 Bad Gateway: Upstream service error
- 503 Service Unavailable: Temporary outage
- 504 Gateway Timeout: Request timeout

### 13.2 Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INVALID_COUNTRY",
    "message": "Country code 'XX' is not supported",
    "details": {
      "supported_countries": ["IN", "US", "GB", ...]
    },
    "timestamp": "2026-02-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### 13.3 Graceful Degradation

**Fallback Strategies:**
```python
async def search_with_fallback(query, country_code):
    try:
        # Try primary search
        results = await primary_search(query, country_code)
        return results
    except PrimarySearchError:
        try:
            # Fallback to cached results
            cached = get_cached_results(query, country_code)
            if cached:
                return cached
        except CacheError:
            pass
        
        try:
            # Fallback to secondary search
            results = await secondary_search(query)
            return results
        except SecondarySearchError:
            # Return empty results with error message
            return {
                'success': False,
                'error': 'Search temporarily unavailable',
                'results': []
            }
```

---

## 14. Future Enhancements

### 14.1 Phase 2 Features

**User Accounts:**
- Registration and authentication
- Profile management
- Saved searches
- Favorite products
- Price alerts

**Advanced Search:**
- Filters (brand, category, features)
- Sort options
- Price history charts
- Comparison tables

### 14.2 Phase 3 Features

**AI/ML Enhancements:**
- Personalized recommendations
- Image-based search
- Natural language understanding
- Predictive pricing

**Mobile Apps:**
- iOS application
- Android application
- Push notifications
- Offline mode

### 14.3 Phase 4 Features

**Enterprise Features:**
- API for third-party developers
- White-label solution
- B2B marketplace integration
- Advanced analytics dashboard
- Custom reporting

---

## Document Control

**Author:** Development Team  
**Reviewers:** Tech Lead, Product Manager, Security Team  
**Approval:** Project Sponsor  
**Last Updated:** February 15, 2026  
**Next Review:** March 15, 2026  
**Version History:**
- v1.0 (Feb 15, 2026): Initial design document

---

**End of Design Document**
