@echo off
title DHH Database Snapshot Restore
color 0C

echo =====================================================================
echo       RESTORE DHH MEDIA NETWORK DATABASE SNAPSHOT
echo =====================================================================
echo.

venv\Scripts\python.exe -c "from backend.app.database import SessionLocal; from backend.app.services.backup_engine import backup_engine; db = SessionLocal(); backups = backup_engine.list_backups(db); print('Available Backups:'); [print(f'[{b.id}] {b.backup_path} ({round(b.file_size_bytes/1024, 1)} KB)') for b in backups]; db.close()"

echo.
set /p BID="Enter Backup ID to restore: "

venv\Scripts\python.exe -c "from backend.app.database import SessionLocal; from backend.app.services.backup_engine import backup_engine; db = SessionLocal(); res = backup_engine.restore_backup(int('%BID%'), db); print(res['message'] if res.get('success') else 'Error: ' + res.get('error', '')); db.close()"

echo.
pause
