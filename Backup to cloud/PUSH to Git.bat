@echo off
REM ========================================
REM Git Push - Deploy All Changes
REM Smart Global Marketplace Scanner
REM ========================================

echo.
echo ========================================
echo DEPLOYING CHANGES TO GITHUB
echo ========================================
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Refresh PATH to ensure git is available
set PATH=%PATH%;C:\Program Files\Git\cmd

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if we're in a git repository
git status >nul 2>&1
if errorlevel 1 (
    echo Initializing Git repository...
    git init
    git branch -M main
    git remote add origin https://github.com/Akshay6766/Smart-Global-Marketplace-scanner.git
    echo Repository initialized!
    echo.
)

echo Step 1: Checking for changes...
git status --short
echo.

REM Ask user for commit message
set /p COMMIT_MSG="Enter commit message (or press Enter for auto-message): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update: Changes on %date% at %time%

echo.
echo Step 2: Staging all changes...
git add .
echo All files staged!
echo.

echo Step 3: Creating commit...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo No changes to commit.
    echo.
    pause
    exit /b 0
)
echo.

echo Step 4: Pushing to GitHub...
echo Repository: https://github.com/Akshay6766/Smart-Global-Marketplace-scanner
echo.
git push origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo PUSH FAILED!
    echo ========================================
    echo.
    echo Trying force push...
    git push origin main --force
    
    if errorlevel 1 (
        echo.
        echo Force push also failed!
        echo.
        echo Possible reasons:
        echo 1. Authentication required (GitHub credentials)
        echo 2. No internet connection
        echo 3. Repository access denied
        echo.
        echo To fix authentication:
        echo 1. Go to: https://github.com/settings/tokens
        echo 2. Generate new token (classic)
        echo 3. Select 'repo' scope
        echo 4. Use token as password when prompted
        echo.
    ) else (
        echo.
        echo ========================================
        echo PUSH SUCCESSFUL (FORCED)!
        echo ========================================
        echo.
        echo Your changes are now on GitHub!
        echo View at: https://github.com/Akshay6766/Smart-Global-Marketplace-scanner
        echo.
    )
) else (
    echo.
    echo ========================================
    echo PUSH SUCCESSFUL!
    echo ========================================
    echo.
    echo Your changes are now on GitHub!
    echo View at: https://github.com/Akshay6766/Smart-Global-Marketplace-scanner
    echo.
)

pause
