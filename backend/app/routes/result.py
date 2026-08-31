from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.document import AIResultInput
from app.services.database_service import save_ai_results, get_document
from app.services.workflow_service import execute_workflow
from app.models.document import DocumentStatus

router = APIRouter(prefix="/results", tags=["AI Results Interface"])

@router.post("/ai-output")
def receive_ai_results(data: AIResultInput, db: Session = Depends(get_db)):
    doc = get_document(db, data.document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        doc = save_ai_results(db, data)
        doc = execute_workflow(db, doc)
        return {
            "document_id": doc.document_id,
            "status": doc.status,
            "decision": doc.decision,
            "reason": doc.reason
        }
    except Exception as e:
        doc.status = DocumentStatus.ERROR
        doc.reason = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")
