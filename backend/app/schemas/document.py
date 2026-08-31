from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.document import DocumentStatus

class UploadResponse(BaseModel):
    document_id: str
    status: DocumentStatus

class StatusResponse(BaseModel):
    document_id: str
    status: DocumentStatus

class AIResultInput(BaseModel):
    document_id: str
    document_type: str
    extracted_data: Dict[str, Any] = {}
    validation: Dict[str, Any] = {}
    confidence: float

class HumanReviewInput(BaseModel):
    action: str  # APPROVE, REJECT, REQUEST_CORRECTION
    notes: Optional[str] = None

class DashboardStats(BaseModel):
    total_documents: int
    processed: int
    human_review: int
    rejected: int
    failed: int

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    document_type: Optional[str]
    upload_time: datetime
    status: DocumentStatus
    extracted_data: Optional[Dict[str, Any]]
    confidence_score: Optional[float]
    decision: Optional[str]
    reason: Optional[str]

    class Config:
        from_attributes = True
