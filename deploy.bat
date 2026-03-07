@echo off
echo ============================================
echo Deploying to AWS Elastic Beanstalk
echo ============================================
echo.

echo Checking EB CLI...
eb --version
if errorlevel 1 (
    echo ERROR: EB CLI not found!
    echo Install it with: pip install awsebcli
    pause
    exit /b 1
)

echo.
echo Deploying application...
eb deploy

echo.
echo ============================================
echo Deployment complete!
echo ============================================
echo.
echo Opening application in browser...
eb open

pause
