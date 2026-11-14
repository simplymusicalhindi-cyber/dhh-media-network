from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.app.database import get_db
from backend.app.models.system import ErrorLog
from backend.app.services.reliability_engine import reliability_engine

router = APIRouter(prefix="/api/errors", tags=["Error Diagnostics & Recovery"])

class CodeRepairRequest(BaseModel):
    file_rel_path: str
    proposed_code: str

@router.get("")
def list_errors(limit: int = 50, db: Session = Depends(get_db)):
    errors = db.query(ErrorLog).order_by(ErrorLog.created_at.desc()).limit(limit).all()
    return errors

@router.post("/recover-now")
def trigger_recovery_cycle(db: Session = Depends(get_db)):
    reliability_engine._clean_temp_media()
    reliability_engine._recover_stuck_queue_jobs(db)
    return {"success": True, "message": "Automated recovery executed. Stale temp files cleared and stuck jobs recovered."}

@router.post("/repair-code")
def repair_code_sandbox(req: CodeRepairRequest):
    res = reliability_engine.run_isolated_code_repair(req.file_rel_path, req.proposed_code)
    return res
