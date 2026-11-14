@echo off
title DHH Database Snapshot Backup
color 0A

echo =====================================================================
echo       CREATING DHH MEDIA NETWORK DATABASE SNAPSHOT
echo =====================================================================
echo.

venv\Scripts\python.exe -c "from backend.app.database import SessionLocal; from backend.app.services.backup_engine import backup_engine; db = SessionLocal(); rec = backup_engine.create_database_backup(db, 'Manual CLI backup'); print('\n[SUCCESS] Backup snapshot created at: ' + rec.backup_path); print('File size: ' + str(round(rec.file_size_bytes/1024, 2)) + ' KB'); db.close()"

echo.
pause
