# 🛍️ SMART PRODUCT FINDER

## AI-Powered Multi-Marketplace Shopping Assistant

**Never overpay again!** Smart Product Finder is an intelligent e-commerce search platform that aggregates products from multiple marketplaces and uses AI to recommend the best deals based on trust, quality, and value.

---

## 🎯 WHAT THIS APP DOES

Smart Product Finder searches **Amazon, Flipkart, eBay, Walmart, and Snapdeal** simultaneously, analyzes products using advanced algorithms, and provides intelligent recommendations tailored to your budget and preferences.

### Key Capabilities:
- 🔍 **Multi-Marketplace Search**: Search 5+ platforms in one query
- 🤖 **AI Chat Assistant**: Natural language queries powered by AWS Bedrock Claude 3.5
- 📱 **Mobile CPI System**: 978 phones pre-scored on 6 performance factors
- 💰 **Smart Budget Advisor**: Get upgrade suggestions and savings opportunities
- 🌍 **Geo-Aware**: Supports 10+ countries with local currency
- ⚡ **Real-Time Data**: Live prices, ratings, and reviews
- 🎯 **Intelligent Ranking**: Products ranked by trust, quality, and value

---

## 📊 PROJECT STATS

- ✅ **978** mobile phones pre-indexed with CPI scores
- ✅ **1,359** NDTV product reviews integrated
- ✅ **100+** marketplaces across 10+ countries
- ✅ **5+** major e-commerce platforms supported
- ✅ **Sub-second** local search response time
- ✅ **Production-ready** with comprehensive documentation

---

## 🚀 CURRENT STATUS

**Version**: 2.0  
**Status**: Production Ready  
**Last Updated**: March 2026

### ✅ Implemented Features:
- ✅ Multi-marketplace live search (Gemini AI + SerpAPI)
- ✅ AI Chat Assistant (AWS Bedrock Claude 3.5 Sonnet)
- ✅ Mobile CPI scoring system (978 phones indexed)
- ✅ Smart budget advisor with recommendations
- ✅ Geo-aware search (10+ countries)
- ✅ Intelligent ranking algorithm
- ✅ Responsive web interface
- ✅ RESTful API (12+ endpoints)
- ✅ Dual search modes (live + local)
- ✅ Advanced filtering and sorting

### 🚧 Planned Features:
- 🔜 User authentication and profiles
- 🔜 Price tracking and alerts
- 🔜 Wishlist and favorites
- 🔜 Mobile apps (iOS/Android)
- 🔜 Browser extensions

---

## 🚀 QUICK START

### Prerequisites
- Python 3.11+ installed
- Internet connection
- (Optional) API keys for enhanced features

### Option 1: Basic Setup (No API Keys Required)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python web_app.py

# 3. Open browser
# Navigate to: http://localhost:5000
```

**What you get:**
- ✅ Mobile CPI search (978 phones, instant results)
- ✅ Mock data for live marketplace search
- ✅ Full UI and features
- ✅ No API costs

---

### Option 2: Full Setup (With Free API Keys)

Get the complete experience with real-time data from all marketplaces!

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Get Free API Keys

**A. Gemini AI (Required for live search) - 100% FREE**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")

**B. SerpAPI (Optional, for real product URLs) - FREE TIER**
1. Go to: https://serpapi.com/users/sign_up
2. Sign up for free account
3. Get your API key from dashboard
4. Free tier: 100 searches/month

**C. AWS Bedrock (Optional, for AI chat) - FREE TIER**
1. Create AWS account: https://aws.amazon.com/
2. Enable Bedrock service
3. Request Claude 3.5 Sonnet access
4. Get AWS credentials (Access Key + Secret Key)
5. Free tier: 12 months limited usage

#### Step 3: Configure API Keys
```bash
# Open api_keys_config.py and add your keys:

# Required for live marketplace search
GEMINI_API_KEY = "AIza...YOUR_KEY_HERE"

# Optional for real product URLs
SERPAPI_KEY = "your_serpapi_key_here"

# Optional for AI chat assistant
AWS_ACCESS_KEY_ID = "your_aws_access_key"
AWS_SECRET_ACCESS_KEY = "your_aws_secret_key"
AWS_REGION = "us-east-1"
```

#### Step 4: Test Your Setup
```bash
# Test Gemini AI integration
python gemini_search.py

# Test SerpAPI integration (if configured)
python serpapi_search.py

# Test AI chat (if AWS configured)
python bedrock_ai_assistant.py
```

#### Step 5: Run the App
```bash
python web_app.py
```

Open browser and navigate to: **http://localhost:5000**

---

## 🎮 HOW TO USE

### Main Search Page
1. **Select Country**: Choose your country from dropdown (auto-detected)
2. **Enter Query**: Type what you're looking for (e.g., "wireless headphones")
3. **Set Budget** (Optional): Enter your maximum budget
4. **Click Search**: Get results from all marketplaces

### Mobile CPI Search
1. Navigate to: http://localhost:5000/mobile
2. Use filters: Price range, brand, CPI score
3. Search by name or features
4. Sort by CPI score, price, or name
5. View detailed scores for each phone

### AI Chat Assistant
1. Click "Chat with AI" button
2. Ask natural language questions:
   - "Find best laptop under 50000"
   - "Compare iPhone 15 vs Samsung S24"
   - "Show me phones with good battery life"
3. Get personalized recommendations
4. Use quick action buttons for common queries

---

## 🔧 TECH STACK

### Backend
- **Python 3.14.3**: Core language
- **Flask 3.1.2**: Web framework
- **aiohttp 3.13.3**: Async HTTP client
- **BeautifulSoup4 4.14.3**: Web scraping
- **boto3 1.42.59**: AWS SDK

### AI & APIs
- **Google Gemini AI 2.0 Flash**: Product search
- **AWS Bedrock Claude 3.5 Sonnet**: Chat assistant
- **SerpAPI**: Google Shopping integration

### Frontend
- **HTML5, CSS3, JavaScript ES6+**
- **Responsive Design**: Mobile-first
- **AJAX**: Dynamic content loading

### Data
- **JSON**: Fast local search (mobile_cpi_index.json)
- **CSV**: Master data (mobiles_2025.csv, ndtv_data_final.csv)

---

## 📁 PROJECT STRUCTURE

```
Smart-product-finder/
├── web_app.py                    # Main Flask application
├── geo_product_finder.py         # Geo-aware search engine
├── mobile_cpi_integration.py     # Mobile CPI search
├── bedrock_ai_assistant.py       # AI chat assistant
├── gemini_search.py              # Gemini AI integration
├── serpapi_search.py             # SerpAPI integration
├── budget_advisor.py             # Budget analysis
├── geo_marketplace_config.py     # Marketplace database
├── mobile_cpi_generator.py       # CPI scoring system
├── api_keys_config.py            # API configuration
├── requirements.txt              # Python dependencies
├── mobile_cpi_index.json         # 978 phones indexed
├── mobiles_2025.csv              # Master phone database
├── ndtv_data_final.csv           # NDTV reviews
├── templates/
│   ├── index.html                # Main search page
│   └── mobile_cpi.html           # Mobile CPI page
├── static/
│   ├── style.css                 # Main styles
│   └── app.js                    # Frontend JavaScript
└── docs/
    ├── DESIGN.md                 # Architecture documentation
    ├── COMPREHENSIVE_DOCUMENTATION.md
    ├── API_KEYS_GUIDE.md
    └── AWS_DEPLOYMENT_GUIDE.md
```

---

## 🌍 SUPPORTED COUNTRIES

- 🇮🇳 **India** (INR) - Amazon, Flipkart, Snapdeal, eBay
- 🇺🇸 **United States** (USD) - Amazon, eBay, Walmart
- 🇬🇧 **United Kingdom** (GBP) - Amazon, eBay
- 🇨🇦 **Canada** (CAD) - Amazon, eBay, Walmart
- 🇦🇺 **Australia** (AUD) - Amazon, eBay
- 🇩🇪 **Germany** (EUR) - Amazon, eBay
- 🇫🇷 **France** (EUR) - Amazon, eBay
- 🇯🇵 **Japan** (JPY) - Amazon, eBay
- 🇸🇬 **Singapore** (SGD) - Amazon, eBay
- 🇦🇪 **UAE** (AED) - Amazon, eBay

---

## 💡 KEY FEATURES EXPLAINED

### 1. Mobile CPI Scoring System
**978 phones pre-scored** on 6 performance factors:
- **Processor** (25%): Chipset, cores, clock speed
- **Camera** (20%): Megapixels, features, video quality
- **Battery** (20%): Capacity, fast charging
- **Display** (15%): Resolution, refresh rate, type
- **Storage** (10%): RAM, internal storage
- **Connectivity** (10%): 5G, WiFi 6, Bluetooth, NFC

**Formula:**
```
Overall CPI = (Processor × 0.25) + (Camera × 0.20) + (Battery × 0.20) + 
              (Display × 0.15) + (Storage × 0.10) + (Connectivity × 0.10)

Price-Value Ratio = Overall CPI / (Price / 1000)
```

### 2. Intelligent Ranking Algorithm
Products ranked by three factors:
- **Trust Score** (30%): Seller rating + reviews + marketplace trust
- **Quality Score** (35%): Product rating + review reliability
- **Value Score** (35%): Price competitiveness

### 3. Smart Budget Advisor
- Analyzes products within your budget
- Suggests better deals if available
- Recommends upgrades (up to 40% above budget)
- Identifies savings opportunities (25% below budget)
- Color-coded quality indicators

### 4. AI Chat Assistant
- Natural language understanding
- Context-aware conversations
- Product comparison analysis
- Personalized recommendations
- Budget-aware suggestions

---

## 🔍 SEARCH STRATEGY

The app uses a multi-tier fallback approach:

1. **SerpAPI** (if configured): Real Google Shopping results with actual product URLs
2. **Gemini AI** (if configured): AI-powered search across all marketplaces
3. **Mock Data**: Realistic product data for testing

**For Mobile CPI Search:**
- Instant local search from JSON index (978 phones)
- No API calls required
- Sub-second response time

---

## 🐛 TROUBLESHOOTING

### App won't start
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.11+

# Run with verbose output
python web_app.py --debug
```

### Gemini AI not working
- ✅ Check API key in `api_keys_config.py`
- ✅ Verify internet connection
- ✅ Check Gemini API quota (1,500 requests/day)
- ✅ App will fallback to mock data automatically

### SerpAPI errors
- ✅ Verify API key is correct
- ✅ Check free tier limits (100 searches/month)
- ✅ App will fallback to Gemini AI

### AWS Bedrock issues
- ✅ Verify AWS credentials
- ✅ Check Claude 3.5 Sonnet access is enabled
- ✅ Verify region is correct (us-east-1)
- ✅ Chat feature will be disabled if not configured

### Port already in use
```bash
# Change port in web_app.py
# Or kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

---

## 📚 DOCUMENTATION

- **[DESIGN.md](DESIGN.md)**: Architecture and design decisions
- **[COMPREHENSIVE_DOCUMENTATION.md](COMPREHENSIVE_DOCUMENTATION.md)**: Complete technical docs
- **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)**: API configuration guide
- **[AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)**: Deployment instructions
- **[SECURITY_README.md](SECURITY_README.md)**: Security best practices

---

## 💰 COST BREAKDOWN

### Free Tier (Recommended for MVP)
- ✅ Gemini AI: **FREE** (1,500 requests/day)
- ✅ SerpAPI: **FREE** (100 searches/month)
- ✅ AWS Free Tier: **FREE** (12 months, limited usage)
- ✅ Hosting: **FREE** (Render.com, Railway.app)

**Total Monthly Cost: $0**

### Paid Tier (Production)
- 💵 SerpAPI: $50/month (5,000 searches)
- 💵 AWS Bedrock: $10-30/month (pay-per-use)
- 💵 Hosting: $10-25/month (VPS)

**Total Monthly Cost: $70-105**

---

## 🚀 DEPLOYMENT

### Local Development
```bash
python web_app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Docker (Coming Soon)
```bash
docker build -t smart-product-finder .
docker run -p 5000:5000 smart-product-finder
```

### Cloud Platforms
- **AWS Elastic Beanstalk**: See [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)
- **Heroku**: `git push heroku main`
- **Render.com**: Connect GitHub repo
- **Railway.app**: One-click deploy

---

## 🤝 CONTRIBUTING

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---




## 🙏 ACKNOWLEDGMENTS

- **AI Tools**: Kiro IDE, GitHub Copilot, ChatGPT, Claude
- **APIs**: Google Gemini AI, AWS Bedrock, SerpAPI
- **Data Sources**: NDTV Gadgets, GSMArena
- **Community**: Stack Overflow, GitHub, Reddit

---

## 📞 Contact & Links

- **GitHub**: [https://github.com/Akshay6766/Smart-Global-Marketplace-scanner]
- **Live Demo**: [https://www.youtube.com/watch?v=diK1tSj6DIY]
- **Documentation**: [https://github.com/Akshay6766/Smart-Global-Marketplace-scanner/blob/main/COMPREHENSIVE_DOCUMENTATION.md]
- **Email**: [6766sankar@gmail.com]
- **LinkedIn**: [linkedin.com/akshay-sankar]
---

## ⭐ SHOW YOUR SUPPORT

If you find this project useful, please:
- ⭐ Star the repository
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🔀 Submit pull requests
- 📢 Share with others

---

**Built with ❤️ by a solo developer using AI tools**

**Proving that AI democratizes software development and empowers individual creators to build enterprise-grade applications at a fraction of traditional costs.**

---

**Last Updated**: March 2026  
**Version**: 2.0  
**Status**: Production Ready
