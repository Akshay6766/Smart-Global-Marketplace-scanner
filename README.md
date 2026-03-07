# SMART PRODUCT FINDER - QUICK START

## WHAT THIS APP DOES:
Searches ALL marketplaces (Amazon, Flipkart, eBay, Walmart, Snapdeal) and finds the best products with real prices, ratings, and reviews.

## CURRENT STATUS:
 Gemini AI integrated (searches ALL marketplaces including Flipkart)
 eBay API working (real data)
 Mock data with realistic products
 Web app ready to run

## HOW TO RUN:

### Option 1: Quick Start (uses eBay API + mock data)
```
python web_app.py
```
Then open: http://localhost:5000

### Option 2: With Gemini AI (get REAL data from ALL marketplaces)

1. Get FREE Gemini API key (takes 2 minutes):
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google
   - Click "Create API Key"
   - Copy the key (starts with "AIza...")

2. Add your API key:
   - Open: api_keys_config.py
   - Replace: YOUR_GEMINI_API_KEY_HERE
   - With: AIza...YOUR_ACTUAL_KEY...
   - Save the file

3. Test it:
   ```
   python test_gemini.py
   ```

4. Run the app:
   ```
   python web_app.py
   ```
   Or double-click: start_app.bat

5. Open browser: http://localhost:5000

## WHAT YOU GET:

### Without Gemini API key:
- eBay real product data
- Realistic mock data for other marketplaces
- Fully functional app

### With Gemini API key (FREE):
- REAL product data from ALL marketplaces
- Works for Flipkart (no Flipkart API needed!)
- Works for Amazon India, eBay, Walmart, Snapdeal
- Actual prices in local currency
- Real ratings and reviews
- Direct product URLs

## GEMINI API - 100% FREE:
- 60 requests per minute
- 1,500 requests per day
- No credit card required
- Perfect for testing and personal use

## FILES:
- web_app.py - Main Flask web server
- geo_product_finder.py - Search engine with Gemini integration
- gemini_search.py - Gemini AI search module
- api_integrations.py - eBay API integration
- api_keys_config.py - Your API keys (add Gemini key here)
- test_gemini.py - Test script
- start_app.bat - Easy startup script

## TROUBLESHOOTING:

### App won't start:
```
python -m pip install flask flask-cors google-genai requests beautifulsoup4
```

### Gemini not working:
- Check API key in api_keys_config.py
- Check internet connection
- App will automatically fallback to eBay API + mock data

### Need help:
- Read: QUICK_START_GUIDE.txt
- All features work without Gemini API key (uses eBay + mock data)

## SEARCH STRATEGY:
1. Try Gemini AI (if API key configured)  searches ALL marketplaces
2. Fallback to eBay API  real eBay products
3. Fallback to mock data  realistic product data

You get a working app either way!
