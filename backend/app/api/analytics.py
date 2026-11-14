import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.analytics import CategoryPerformance, WeeklyLearningReport
from backend.app.services.growth_learning_engine import growth_learning_engine

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Self-Learning"])

@router.get("/categories")
def get_category_analytics(db: Session = Depends(get_db)):
    return growth_learning_engine.aggregate_category_performance(db)

@router.get("/weekly-report")
def get_latest_weekly_report(db: Session = Depends(get_db)):
    report = db.query(WeeklyLearningReport).order_by(WeeklyLearningReport.created_at.desc()).first()
    if not report:
        report = growth_learning_engine.generate_weekly_learning_report(db)
    return {
        "id": report.id,
        "week_start": report.week_start.isoformat(),
        "summary": report.summary,
        "top_performing_formats": json.loads(report.top_performing_formats),
        "top_topics": json.loads(report.top_topics),
        "recommended_strategy_shifts": json.loads(report.recommended_strategy_shifts),
        "created_at": report.created_at.isoformat()
    }

@router.post("/generate-report")
def generate_report_now(db: Session = Depends(get_db)):
    report = growth_learning_engine.generate_weekly_learning_report(db)
    return {
        "success": True,
        "report_id": report.id,
        "summary": report.summary
    }
