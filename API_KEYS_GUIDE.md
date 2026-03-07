# API Keys Configuration Guide

## Overview
Your Smart Product Finder uses different search methods for different pages:

### 1. Mobile CPI Page (mobile_cpi.html) - ✅ WORKS WITHOUT API KEYS
- **Data Source**: Local JSON file (`mobile_cpi_index.json`)
- **Contains**: 978 pre-indexed mobile phones with CPI scores
- **Search Method**: Local search through JSON data
- **API Keys Required**: NONE
- **Why it works**: All data is stored locally, no external API calls needed

### 2. Main Page (index.html) - ❌ REQUIRES API KEYS
- **Data Source**: Live web search via external APIs
- **Search Method**: Real-time product search from e-commerce sites
- **API Keys Required**: YES (Gemini AI or SerpAPI)
- **Why it needs keys**: Searches live products from Amazon, Flipkart, etc.

---

## API Keys Storage Locations

### 1. Application API Keys (Gemini & SerpAPI)
**File**: `Smart-product-finder/api_keys_config.py`

Current status: Placeholder values (not configured)
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
SERPAPI_KEY = "YOUR_SERPAPI_KEY_HERE"
```

### 2. AWS Credentials (Bedrock AI)
**File**: `C:\Users\Arora\.aws\credentials`

Status: ✅ Configured and working
- Used for AWS Bedrock AI chat assistant
- Stored in standard AWS credentials file
- Requires valid payment method on AWS account

---

## How the Main Page Search Works

The main page tries two methods in order:

### Method 1: SerpAPI (Primary)
- Searches Google Shopping for real products
- Returns actual product URLs from Amazon, Flipkart, etc.
- **Status**: Not configured (needs API key)
- **Free Tier**: 100 searches/month
- **Get Key**: https://serpapi.com/users/sign_up

### Method 2: Gemini AI (Fallback)
- Uses Google's Gemini AI to search and find products
- Returns product recommendations with details
- **Status**: Not configured (needs API key)
- **Free Tier**: Available
- **Get Key**: https://makersuite.google.com/app/apikey

### Current Behavior
When you search on the main page:
1. Tries SerpAPI → Fails (no API key)
2. Falls back to Gemini AI → Fails (no API key)
3. Returns empty results with error message

---

## How to Fix Main Page Search

### Option 1: Add SerpAPI Key (Recommended)
1. Sign up at https://serpapi.com/users/sign_up
2. Get your free API key (100 searches/month)
3. Open `api_keys_config.py`
4. Replace `YOUR_SERPAPI_KEY_HERE` with your actual key
5. Save and restart web app

### Option 2: Add Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Open `api_keys_config.py`
5. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual key
6. Save and restart web app

### Option 3: Add Both (Best)
- SerpAPI provides real product URLs
- Gemini AI provides intelligent recommendations
- Having both gives best results

---

## Security Notes

✅ **Good**: API keys are in `api_keys_config.py` with placeholders
✅ **Good**: `.gitignore` prevents committing real keys to GitHub
✅ **Good**: AWS credentials stored in standard location (`~/.aws/credentials`)

⚠️ **Important**: Never commit real API keys to GitHub!

---

## Testing API Configuration

### Test SerpAPI:
```bash
cd Smart-product-finder
python serpapi_search.py
```

### Test Gemini AI:
```bash
cd Smart-product-finder
python gemini_search.py
```

### Test AWS Bedrock:
```bash
cd Smart-product-finder
python test_bedrock_simple.py
```

---

## Summary

| Feature | API Key Needed | Current Status | Location |
|---------|---------------|----------------|----------|
| Mobile CPI Search | ❌ None | ✅ Working | Local JSON file |
| Main Page Search | ✅ SerpAPI or Gemini | ❌ Not configured | `api_keys_config.py` |
| AI Chat Assistant | ✅ AWS Bedrock | ⚠️ Configured but needs payment | `~/.aws/credentials` |

**To make main page work**: Add at least one API key (SerpAPI or Gemini) to `api_keys_config.py`
