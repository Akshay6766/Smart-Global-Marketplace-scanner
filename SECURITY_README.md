# Smart Product Finder - Security Guide

##  CRITICAL: API Keys Security

**NEVER commit `api_keys_config.py` to GitHub!**

This file contains your actual API keys and is protected by `.gitignore`.

## Setup Instructions

1. **The file `api_keys_config.py` already exists** with placeholder values
2. **Edit it and add your real API keys**:
   ```python
   GEMINI_API_KEY = "your_actual_gemini_key_here"
   SERPAPI_KEY = "your_actual_serpapi_key_here"
   ```
3. **Keep it local** - it's already in `.gitignore`

## Get Your API Keys

- **Gemini API**: https://makersuite.google.com/app/apikey (Free)
- **SerpAPI**: https://serpapi.com/users/sign_up (100 free searches/month)
- **AWS Bedrock**: Configure via AWS CLI

## Before Pushing to GitHub

Run this command to verify your API keys won't be exposed:
```bash
cd Smart-product-finder
git status
```

**Make sure `api_keys_config.py` is NOT in the list!**

If you see it, the `.gitignore` is working correctly and it will be ignored.

## Project Structure

```
Smart-product-finder/
 api_keys_config.py          # Your actual keys (NEVER commit!)
 .gitignore                  # Protects api_keys_config.py
 web_app.py                  # Main application
 templates/                  # HTML templates
 static/                     # CSS, JS files
 README.md                   # Project documentation
```

## Features

- Mobile phone search with CPI scores
- AI-powered natural language search
- Interactive chat assistant
- Sorting and pagination
- Statistics dashboard

## Running the Application

```bash
python web_app.py
```

Visit: http://localhost:5000
