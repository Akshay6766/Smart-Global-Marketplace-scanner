@echo off
REM ========================================
REM AWS S3 Backup - Automated
REM Smart Global Marketplace Scanner
REM ========================================

echo.
echo ========================================
echo AWS S3 BACKUP STARTING
echo ========================================
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check if backup script exists
if not exist "C:\Users\Arora\.kiro\Smart-product-finder\Backup to cloud\backup_to_aws_s3_auto.py" (
    echo ERROR: Backup script not found!
    echo Expected location: C:\Users\Arora\.kiro\Smart-product-finder\Backup to cloud\backup_to_aws_s3_auto.py
    pause
    exit /b 1
)

echo Backup script found!
echo.

REM Check if boto3 is installed
python -c "import boto3" 2>nul
if errorlevel 1 (
    echo boto3 not found. Installing...
    pip install boto3
    echo.
)

REM Check AWS credentials
echo Checking AWS credentials...
python -c "import boto3; boto3.Session().get_credentials()" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: AWS credentials not configured!
    echo.
    echo To configure AWS credentials:
    echo 1. Install AWS CLI: pip install awscli
    echo 2. Run: aws configure
    echo 3. Enter your AWS Access Key ID
    echo 4. Enter your AWS Secret Access Key
    echo 5. Enter region: us-east-1
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" (
        echo Backup cancelled.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo RUNNING BACKUP
echo ========================================
echo.

REM Run the backup script
python "C:\Users\Arora\.kiro\Smart-product-finder\Backup to cloud\backup_to_aws_s3_auto.py"

if errorlevel 1 (
    echo.
    echo ========================================
    echo BACKUP FAILED!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
) else (
    echo.
    echo ========================================
    echo BACKUP COMPLETED SUCCESSFULLY!
    echo ========================================
    echo.
    echo Your project has been backed up to AWS S3.
    echo Bucket: smart-product-finder-backup
    echo Location: s3://smart-product-finder-backup/kiro-backups/
    echo.
)

pause
