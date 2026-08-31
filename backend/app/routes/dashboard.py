from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.document import Document, DocumentStatus
from app.schemas.document import DashboardStats, DocumentResponse

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(Document).count()
    completed = db.query(Document).filter(Document.status == DocumentStatus.COMPLETED).count()
    human_review = db.query(Document).filter(Document.status == DocumentStatus.HUMAN_REVIEW).count()
    rejected = db.query(Document).filter(Document.status == DocumentStatus.REJECTED).count()
    failed = db.query(Document).filter(Document.status == DocumentStatus.ERROR).count()

    return DashboardStats(
        total_documents=total,
        processed=completed,
        human_review=human_review,
        rejected=rejected,
        failed=failed
    )

@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.upload_time.desc()).all()
