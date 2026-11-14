@echo off
title Stop DHH Autonomous Media Network
color 0C

echo =====================================================================
echo       STOPPING DESI HIP-HOP AUTONOMOUS MEDIA PLATFORM
echo =====================================================================
echo.

echo [INFO] Terminating background processes on port 8787...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8787 ^| findstr LISTENING') do (
    echo Terminating PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo =====================================================================
echo [SUCCESS] DHH Media Network background services stopped cleanly.
echo =====================================================================
timeout /t 3
