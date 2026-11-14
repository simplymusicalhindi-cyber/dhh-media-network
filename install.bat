@echo off
title DHH Network Dependency Installer
color 0E

echo =====================================================================
echo       INSTALLING DHH AUTONOMOUS NETWORK DEPENDENCIES
echo =====================================================================
echo.

echo [1/3] Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\python.exe -m pip install --upgrade pip
call venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo [2/3] Setting up Frontend React dependencies...
cd frontend
call npm install
call npm run build
cd ..

echo.
echo [3/3] Initializing SQLite database and cultural seeds...
call venv\Scripts\python.exe -m backend.app.seed

echo.
echo =====================================================================
echo [SUCCESS] Installation Complete! Run START.bat to launch platform.
echo =====================================================================
pause
