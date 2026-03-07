# Smart Product Finder - AWS Deployment

## What This Application Does

A geo-aware product search engine with:
- Multi-country marketplace search
- AI-powered product ranking
- Budget-based recommendations
- Mobile phone CPI (Consumer Price Index) scoring system
- 978 mobile phones with comprehensive specs and scores
- Google Shopping integration

## Deployment Files Included

 `Procfile` - Tells AWS how to run the application
 `runtime.txt` - Specifies Python 3.11
 `.ebignore` - Excludes unnecessary files
 `.ebextensions/01_flask.config` - AWS EB configuration
 `requirements.txt` - All Python dependencies
 `mobile_cpi_index.json` - 978 phones with CPI scores
 `AWS_DEPLOYMENT_GUIDE.md` - Detailed deployment guide
 `QUICK_DEPLOY.md` - Quick start guide

## Quick Deploy (5 Minutes)

```bash
# Install AWS tools
pip install awscli awsebcli

# Configure AWS credentials
aws configure

# Navigate to project
cd Smart-prdouct-finder

# Initialize and deploy
eb init -p python-3.11 smart-product-finder --region us-east-1
eb create smart-product-finder-env
eb open
```

Your app is now live on AWS!

## Update Application

```bash
# After making changes
eb deploy
```

## View Logs

```bash
eb logs
```

## Terminate (When Done)

```bash
eb terminate smart-product-finder-env
```

## Cost

- **Free Tier**: t2.micro (free for first year)
- **Production**: t2.medium (~$30/month)
- **Serverless**: Lambda (first 1M requests free)

## Features

### Main Search
- Search products across global marketplaces
- Filter by country, price, rating
- AI-powered ranking by trust, quality, and value
- Budget analysis and recommendations

### Mobile CPI Search
- 978 mobile phones with comprehensive CPI scores
- 7 scoring metrics: Processor, Display, Camera, Battery, Storage, Connectivity, Value
- Auto-redirect from main search for mobile queries
- Budget filtering
- Google Shopping links for each phone

## Architecture

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript
- **Server**: Gunicorn (4 workers)
- **Deployment**: AWS Elastic Beanstalk or EC2
- **Database**: JSON index (mobile_cpi_index.json)

## Environment

- Python 3.11
- Flask 3.0+
- Gunicorn 21.0+
- No external database required

## Support

For detailed instructions, see:
- `QUICK_DEPLOY.md` - Quick start guide
- `AWS_DEPLOYMENT_GUIDE.md` - Comprehensive guide

For issues:
1. Check logs: `eb logs`
2. Verify all files uploaded
3. Ensure mobile_cpi_index.json is included

## Local Testing

```bash
python web_app.py
# Open http://localhost:5000
```

## Security

- CORS enabled for API access
- No hardcoded secrets
- Environment variables supported
- HTTPS recommended for production

Ready to deploy! 
