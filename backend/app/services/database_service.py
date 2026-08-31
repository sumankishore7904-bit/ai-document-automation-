from typing import Optional
from sqlalchemy.orm import Session
from app.models.document import Document, DocumentStatus
from app.schemas.document import AIResultInput

def create_document(db: Session, doc_id: str, filename: str) -> Document:
    """Inserts a freshly uploaded document record into SQLite/PostgreSQL."""
    doc = Document(
        document_id=doc_id,
        filename=filename,
        status=DocumentStatus.UPLOADED
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: str) -> Optional[Document]:
    """Retrieves a single document by its primary ID key."""
    return db.query(Document).filter(Document.document_id == doc_id).first()

def save_ai_results(db: Session, data: AIResultInput) -> Document:
    """Updates database entity with AI payload prior to workflow execution."""
    doc = get_document(db, data.document_id)
    if not doc:
        raise ValueError(f"Document ID '{data.document_id}' not found.")

    doc.document_type = data.document_type
    doc.extracted_data = data.extracted_data
    doc.confidence_score = data.confidence
    doc.validation_status = data.validation.get("status", "UNKNOWN")
    doc.missing_fields = data.validation.get("missing_fields", [])
    doc.mismatches = data.validation.get("mismatches", [])
    doc.status = DocumentStatus.EXTRACTED

    db.commit()
    db.refresh(doc)
    return doc
