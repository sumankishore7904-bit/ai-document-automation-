from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse, HumanReviewInput

router = APIRouter(prefix="/review", tags=["Human Review"])

@router.get("/pending", response_model=List[DocumentResponse])
def get_pending_reviews(db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.status == DocumentStatus.HUMAN_REVIEW).all()

@router.post("/{document_id}")
def submit_review(document_id: str, payload: HumanReviewInput, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    action = payload.action.upper()
    if action == "APPROVE":
        doc.status = DocumentStatus.COMPLETED
        doc.decision = "MANUALLY_APPROVED"
    elif action == "REJECT":
        doc.status = DocumentStatus.REJECTED
        doc.decision = "MANUALLY_REJECTED"
    elif action == "REQUEST_CORRECTION":
        doc.status = DocumentStatus.PROCESSING
        doc.decision = "CORRECTION_REQUESTED"
    else:
        raise HTTPException(status_code=400, detail="Invalid review action")

    doc.reason = payload.notes or f"Action taken by admin: {action}"
    db.commit()
    return {"document_id": doc.document_id, "status": doc.status, "decision": doc.decision}
