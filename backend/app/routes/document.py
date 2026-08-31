from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.document_service import save_uploaded_file
from app.services.database_service import create_document, get_document
from app.schemas.document import UploadResponse, StatusResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    doc_id, filename = save_uploaded_file(file)
    doc = create_document(db, doc_id, filename)
    return UploadResponse(document_id=doc.document_id, status=doc.status)

@router.get("/{document_id}/status", response_model=StatusResponse)
def get_status(document_id: str, db: Session = Depends(get_db)):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return StatusResponse(document_id=doc.document_id, status=doc.status)
