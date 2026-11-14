from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.reliability_engine import reliability_engine

router = APIRouter(prefix="/api/health", tags=["System Health"])

@router.get("")
def get_system_health(db: Session = Depends(get_db)):
    """Run full diagnostic health check on all subsystems."""
    return reliability_engine.check_all_subsystems(db)
