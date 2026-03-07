# AWS Deployment Guide for Smart Product Finder

## Prerequisites
1. AWS Account
2. AWS CLI installed and configured
3. EB CLI (Elastic Beanstalk CLI) installed

## Installation Steps

### 1. Install AWS CLI
```bash
# Windows (using pip)
pip install awscli

# Configure AWS credentials
aws configure
```

### 2. Install EB CLI
```bash
pip install awsebcli
```

## Deployment Options

### Option A: AWS Elastic Beanstalk (Recommended - Easiest)

#### Step 1: Initialize EB Application
```bash
cd Smart-prdouct-finder
eb init -p python-3.11 smart-product-finder --region us-east-1
```

#### Step 2: Create Environment
```bash
eb create smart-product-finder-env
```

#### Step 3: Deploy
```bash
eb deploy
```

#### Step 4: Open Application
```bash
eb open
```

#### Update Application
```bash
# After making changes
eb deploy
```

#### View Logs
```bash
eb logs
```

#### Terminate Environment (when done)
```bash
eb terminate smart-product-finder-env
```

---

### Option B: AWS EC2 (More Control)

#### Step 1: Launch EC2 Instance
1. Go to AWS Console  EC2
2. Launch Instance
3. Choose Ubuntu Server 22.04 LTS
4. Instance type: t2.medium or t3.medium (recommended)
5. Configure Security Group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
6. Create/Select Key Pair
7. Launch Instance

#### Step 2: Connect to Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

#### Step 3: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv nginx -y

# Install Git
sudo apt install git -y
```

#### Step 4: Clone/Upload Your Application
```bash
# Option 1: Upload files using SCP
scp -i your-key.pem -r Smart-prdouct-finder ubuntu@your-ec2-ip:~/

# Option 2: Clone from Git (if you have a repo)
git clone your-repo-url
cd Smart-prdouct-finder
```

#### Step 5: Setup Application
```bash
cd Smart-prdouct-finder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 6: Configure Gunicorn Service
```bash
sudo nano /etc/systemd/system/smart-product-finder.service
```

Add this content:
```ini
[Unit]
Description=Smart Product Finder
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Smart-prdouct-finder
Environment="PATH=/home/ubuntu/Smart-prdouct-finder/venv/bin"
ExecStart=/home/ubuntu/Smart-prdouct-finder/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 web_app:app

[Install]
WantedBy=multi-user.target
```

#### Step 7: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/smart-product-finder
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your EC2 public IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/ubuntu/Smart-prdouct-finder/static;
    }
}
```

#### Step 8: Enable and Start Services
```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/smart-product-finder /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start application service
sudo systemctl start smart-product-finder
sudo systemctl enable smart-product-finder

# Check status
sudo systemctl status smart-product-finder
```

#### Step 9: Access Your Application
Open browser: `http://your-ec2-public-ip`

---

### Option C: AWS Lambda + API Gateway (Serverless)

For serverless deployment, you'll need to use Zappa:

```bash
pip install zappa

# Initialize Zappa
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

---

## Environment Variables (if needed)

Create `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

---

## Cost Estimates

### Elastic Beanstalk
- t2.micro (Free Tier): $0/month for first year
- t2.small: ~$17/month
- t3.medium: ~$30/month

### EC2
- t2.micro (Free Tier): $0/month for first year
- t2.medium: ~$34/month
- t3.medium: ~$30/month

### Lambda (Serverless)
- First 1M requests free
- $0.20 per 1M requests after

---

## Monitoring

### Elastic Beanstalk
```bash
eb health
eb logs
```

### EC2
```bash
# View application logs
sudo journalctl -u smart-product-finder -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## Troubleshooting

### Application won't start
```bash
# Check logs
eb logs  # For EB
sudo journalctl -u smart-product-finder  # For EC2

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### Static files not loading
- Ensure static folder is included in deployment
- Check Nginx configuration
- Verify file permissions

---

## Security Best Practices

1. **Use HTTPS**: Set up SSL certificate (Let's Encrypt is free)
2. **Restrict SSH**: Only allow SSH from your IP
3. **Use Environment Variables**: Don't hardcode secrets
4. **Regular Updates**: Keep system and packages updated
5. **Backup Data**: Regular backups of mobile_cpi_index.json

---

## Quick Deploy Commands

### Elastic Beanstalk
```bash
eb init -p python-3.11 smart-product-finder
eb create smart-product-finder-env
eb deploy
eb open
```

### Update After Changes
```bash
eb deploy
```

---

## Support

For issues:
1. Check logs: `eb logs` or `sudo journalctl -u smart-product-finder`
2. Verify all files are uploaded
3. Check requirements.txt has all dependencies
4. Ensure mobile_cpi_index.json is included

---

## Files Created for Deployment

- `Procfile`: Tells AWS how to run the app
- `.ebextensions/01_flask.config`: EB configuration
- `runtime.txt`: Python version
- `.ebignore`: Files to exclude from deployment
- `requirements.txt`: Python dependencies (already exists)

All set! Choose your deployment method and follow the steps above.
