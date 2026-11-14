from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.backup_engine import backup_engine

router = APIRouter(prefix="/api/backups", tags=["Backup & Restore"])

@router.get("")
def list_backups(db: Session = Depends(get_db)):
    return backup_engine.list_backups(db)

@router.post("/create")
def create_backup_now(db: Session = Depends(get_db)):
    rec = backup_engine.create_database_backup(db, note="Manual snapshot from dashboard")
    return {"success": True, "backup_id": rec.id, "path": rec.backup_path, "size": rec.file_size_bytes}

@router.post("/{backup_id}/restore")
def restore_backup_now(backup_id: int, db: Session = Depends(get_db)):
    res = backup_engine.restore_backup(backup_id, db)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res
