import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, JSON, Enum
from app.database import Base

class DocumentStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    EXTRACTED = "EXTRACTED"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    REJECTED = "REJECTED"
    ERROR = "ERROR"

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    
    # Extracted, Validation, Decision payload
    extracted_data = Column(JSON, nullable=True)
    validation_status = Column(String, nullable=True)
    missing_fields = Column(JSON, nullable=True)
    mismatches = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    decision = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    next_action = Column(String, nullable=True)
