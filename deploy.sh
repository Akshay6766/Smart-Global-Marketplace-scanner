#!/bin/bash
echo "============================================"
echo "Deploying to AWS Elastic Beanstalk"
echo "============================================"
echo

echo "Checking EB CLI..."
if ! command -v eb &> /dev/null; then
    echo "ERROR: EB CLI not found!"
    echo "Install it with: pip install awsebcli"
    exit 1
fi

echo
echo "Deploying application..."
eb deploy

echo
echo "============================================"
echo "Deployment complete!"
echo "============================================"
echo
echo "Opening application in browser..."
eb open
