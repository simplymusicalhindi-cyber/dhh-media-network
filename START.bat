@echo off
setlocal enabledelayedexpansion
title DHH Autonomous Media Network - Startup
color 0B

echo =====================================================================
echo       DESI HIP-HOP (DHH) AUTONOMOUS INSTAGRAM MEDIA NETWORK
echo =====================================================================
echo.

:: 1. Check Python Availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.11+ is not found in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Check Virtual Environment
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    echo [INFO] Installing Python requirements...
    call venv\Scripts\python.exe -m pip install -r requirements.txt
)

:: 3. Check Database & Seeding
if not exist "backend\data\dhh_media.db" (
    echo [INFO] Initializing SQLite database and cultural seeds...
    call venv\Scripts\python.exe -m backend.app.seed
)

:: 4. Check Frontend Build
if not exist "frontend\dist\index.html" (
    echo [INFO] Building React production dashboard bundle...
    cd frontend
    call npm install
    call npm run build
    cd ..
)

:: 5. Launch Backend & Scheduler (Port 8787)
echo.
echo [INFO] Starting DHH Autonomous Media Server on http://127.0.0.1:8787...
start "DHH Network Backend" /min cmd /c "venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8787"

:: 6. Wait for Port 8787 to become active
echo [INFO] Waiting for service to become responsive...
timeout /t 3 /nobreak >nul

:: 7. Open Dashboard in Browser
echo [INFO] Opening Local Control Dashboard in default browser...
start http://127.0.0.1:8787/

echo.
echo =====================================================================
echo [SUCCESS] DHH Media Network is running autonomously in the background!
echo Dashboard: http://127.0.0.1:8787
echo To cleanly stop the server, run: STOP.bat
echo =====================================================================
timeout /t 5
