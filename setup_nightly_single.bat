@echo off
REM Setup Nightly Schedule - Single Bot (Cost Optimized)
REM Creates a Windows Task Scheduler task to run ONE bot daily
REM Saves 50% on API costs!

echo ========================================
echo Polymarket Bot - Nightly Scheduler
echo COST-OPTIMIZED EDITION (Single Bot)
echo ========================================
echo.

REM Get the current directory
set BOT_DIR=%~dp0
set BOT_PATH=%BOT_DIR%LAUNCH_SINGLE.bat

echo Bot location: %BOT_PATH%
echo.

REM Check if LAUNCH_SINGLE.bat exists
if not exist "%BOT_PATH%" (
    echo ERROR: LAUNCH_SINGLE.bat not found!
    echo Make sure this script is in the same folder as LAUNCH_SINGLE.bat
    pause
    exit /b 1
)

echo What time should the bot run daily?
echo Examples: 06:00, 18:30, 23:00 (use 24-hour format)
echo.
set /p RUN_TIME="Enter time (HH:MM): "

if "%RUN_TIME%"=="" (
    echo No time entered. Using default: 06:00
    set RUN_TIME=06:00
)

echo.
echo Creating scheduled task...
echo.

REM Delete existing tasks if they exist (both old and new)
schtasks /delete /tn "Polymarket Alpha Bot - Nightly" /f >nul 2>&1
schtasks /delete /tn "Polymarket Alpha Bot - Single" /f >nul 2>&1

REM Create the scheduled task for SINGLE bot
schtasks /create ^
    /tn "Polymarket Alpha Bot - Single" ^
    /tr "cmd /c cd /d \"%BOT_DIR%\" && LAUNCH_SINGLE.bat" ^
    /sc daily ^
    /st %RUN_TIME% ^
    /rl limited ^
    /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Task created successfully
    echo ========================================
    echo.
    echo Task Details:
    echo   Name: Polymarket Alpha Bot - Single
    echo   Time: %RUN_TIME% (daily)
    echo   Location: %BOT_PATH%
    echo.
    echo COST SAVINGS:
    echo   - Runs ONLY original bot (all markets)
    echo   - Dashboard filters data into tabs automatically
    echo   - 50%% LESS API COST vs running both bots
    echo   - Same number of opportunities shown
    echo.
    echo The bot will run every day at %RUN_TIME%
    echo.
    echo IMPORTANT:
    echo   - Computer must be ON at the scheduled time
    echo   - PERPLEXITY_API_KEY must be set permanently
    echo   - Results saved to reports/ folder
    echo.
    echo Useful Commands:
    echo   - Test run now: schtasks /run /tn "Polymarket Alpha Bot - Single"
    echo   - View all tasks: taskschd.msc
    echo   - Delete task: schtasks /delete /tn "Polymarket Alpha Bot - Single" /f
    echo.
) else (
    echo.
    echo ERROR: Failed to create scheduled task
    echo Try running this script as Administrator
    echo.
)

pause
