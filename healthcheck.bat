@echo off
title DHH Network Subsystem Health Check
color 0E

echo =====================================================================
echo       DHH MEDIA NETWORK - SUBSYSTEM HEALTH & INTEGRITY CHECK
echo =====================================================================
echo.

venv\Scripts\python.exe -c "from backend.app.database import SessionLocal; from backend.app.services.reliability_engine import reliability_engine; db = SessionLocal(); res = reliability_engine.check_all_subsystems(db); print('\nOVERALL STATUS:', res['overall_status']); print('\nSUBSYSTEM DETAILS:'); [print(f' - {k.upper()}: [{v[\"status\"]}] {v[\"detail\"]}') for k, v in res['subsystems'].items()]; db.close()"

echo.
pause
