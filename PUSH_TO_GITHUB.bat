@echo off
echo ========================================
echo PUSHING TO GITHUB
echo ========================================
echo.

REM Navigate to Smart-product-finder directory
cd /d "%~dp0Smart-product-finder"

echo Step 1: Initializing Git repository...
git init
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Creating initial commit...
git commit -m "Initial commit: Smart Global Marketplace Scanner - AI-powered e-commerce search platform"
echo.

echo Step 4: Setting main branch...
git branch -M main
echo.

echo Step 5: Adding remote repository...
git remote add origin https://github.com/Akshay6766/Smart-Global-Marketplace-scanner.git
echo.

echo Step 6: Pushing to GitHub...
git push -u origin main --force
echo.

echo ========================================
echo PUSH COMPLETE!
echo ========================================
echo.
echo Your code is now on GitHub at:
echo https://github.com/Akshay6766/Smart-Global-Marketplace-scanner
echo.
pause
