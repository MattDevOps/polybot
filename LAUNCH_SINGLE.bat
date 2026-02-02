@echo off
REM Single Bot Launcher - Cost Optimized
REM Runs ONLY the original bot (all markets)
REM Dashboard tabs still work to filter Serious/Meme/All

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo Polymarket Alpha Bot - Single Run
echo Cost-Optimized Edition
echo ========================================
echo.
echo Working directory: %CD%
echo.

echo [1/4] Running bot (scanning all markets)...
echo.

python polymarket_alpha_bot.py

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Bot failed to run
    echo.
    echo Troubleshooting:
    echo   1. Make sure Python is installed: python --version
    echo   2. Check you're in the right folder: %CD%
    echo   3. Verify API key is set: echo %PERPLEXITY_API_KEY%
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Bot completed successfully
echo.

REM Rename the latest_report.json to original_latest.json
if exist "reports\latest_report.json" (
    copy /Y "reports\latest_report.json" "reports\original_latest.json" >nul 2>&1
    echo [2/4] Data saved for dashboard
)

REM Also copy to serious_latest.json so dashboard shows data in all tabs
if exist "reports\latest_report.json" (
    copy /Y "reports\latest_report.json" "reports\serious_latest.json" >nul 2>&1
    echo       (Populating all dashboard tabs)
)

echo.
echo [3/4] Copying dashboard to reports folder...
copy /Y dashboard_triple.html reports\dashboard.html >nul 2>&1

if not exist "reports\dashboard.html" (
    echo WARNING: Could not copy dashboard
    echo Make sure dashboard_triple.html exists in: %CD%
)

echo.
echo [4/4] Starting local server...
echo.
echo Server will run at: http://localhost:8000
echo Dashboard URL: http://localhost:8000/dashboard.html
echo.
echo The dashboard has THREE TABS:
echo   - All Markets (all opportunities)
echo   - Serious (filtered automatically by dashboard)
echo   - Meme (GTA, Jesus, etc. - filtered by dashboard)
echo.
echo All data comes from ONE bot run = 50% cost savings!
echo.
echo Press Ctrl+C in this window to stop the server
echo.

cd reports

REM Open dashboard in default browser after a short delay
timeout /t 2 /nobreak >nul
start "" http://localhost:8000/dashboard.html

echo Opening dashboard in your browser...
echo.

REM Start the server (this will keep running)
python -m http.server 8000
