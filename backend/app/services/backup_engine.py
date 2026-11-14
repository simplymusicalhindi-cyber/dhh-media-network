import os
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.models.system import BackupRecord

class BackupEngine:
    def __init__(self):
        self.backup_dir = settings.BACKUP_DIR
        self.db_file = Path(settings.DATABASE_URL.replace("sqlite:///", ""))

    def create_database_backup(self, db: Session, note: str = "Automated snapshot") -> BackupRecord:
        """Create a safe snapshot copy of the SQLite database."""
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"dhh_db_backup_{timestamp}.db"
        dest_path = self.backup_dir / backup_filename

        shutil.copy2(self.db_file, dest_path)
        file_size = dest_path.stat().st_size

        record = BackupRecord(
            backup_path=str(dest_path),
            file_size_bytes=file_size,
            backup_type="SQLITE_SNAPSHOT",
            status="SUCCESS",
            created_at=datetime.datetime.utcnow()
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        self._prune_old_backups(keep_count=10)
        return record

    def list_backups(self, db: Session) -> List[BackupRecord]:
        """List all recorded database backups."""
        return db.query(BackupRecord).order_by(BackupRecord.created_at.desc()).all()

    def restore_backup(self, backup_id: int, db: Session) -> Dict[str, Any]:
        """Restore database from an existing backup snapshot."""
        rec = db.query(BackupRecord).filter(BackupRecord.id == backup_id).first()
        if not rec or not Path(rec.backup_path).exists():
            return {"success": False, "error": "Backup snapshot file not found"}

        # Copy back to main DB path
        shutil.copy2(rec.backup_path, self.db_file)
        return {"success": True, "message": f"Successfully restored database from {Path(rec.backup_path).name}"}

    def _prune_old_backups(self, keep_count: int = 10):
        """Keep only the latest N backup files to preserve disk space."""
        files = sorted(self.backup_dir.glob("*.db"), key=lambda f: f.stat().st_mtime, reverse=True)
        if len(files) > keep_count:
            for extra in files[keep_count:]:
                try:
                    extra.unlink()
                except Exception:
                    pass

backup_engine = BackupEngine()
