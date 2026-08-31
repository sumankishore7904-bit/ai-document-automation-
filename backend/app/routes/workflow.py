from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.database_service import get_document
from app.services.workflow_service import execute_workflow

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/trigger/{document_id}")
def trigger_workflow(document_id: str, db: Session = Depends(get_db)):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc = execute_workflow(db, doc)
    return {"document_id": doc.document_id, "status": doc.status, "decision": doc.decision}
