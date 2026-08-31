from sqlalchemy.orm import Session
from app.models.document import Document, DocumentStatus

def execute_workflow(db: Session, doc: Document) -> Document:
    """
    Evaluates confidence score and validation issues to automatically decision state:
    
    - High Confidence (>= 0.85) & No Errors -> AUTO APPROVE (COMPLETED)
    - Medium Confidence (0.60 to 0.84) OR Missing Fields -> HUMAN REVIEW
    - Low Confidence (< 0.60) OR Data Mismatches -> REJECTED
    """
    confidence = doc.confidence_score or 0.0
    missing_fields = doc.missing_fields or []
    mismatches = doc.mismatches or []

    has_missing = len(missing_fields) > 0
    has_mismatches = len(mismatches) > 0

    if confidence >= 0.85 and not has_missing and not has_mismatches:
        doc.status = DocumentStatus.COMPLETED
        doc.decision = "AUTO_APPROVED"
        doc.reason = "High confidence score and zero validation anomalies."
        doc.next_action = "STORE_AND_FINALIZE"

    elif confidence >= 0.60 or has_missing:
        doc.status = DocumentStatus.HUMAN_REVIEW
        doc.decision = "FLAGGED_FOR_REVIEW"
        reason_parts = []
        if confidence < 0.85:
            reason_parts.append(f"Medium confidence ({confidence:.2f})")
        if has_missing:
            reason_parts.append(f"Missing fields: {', '.join(missing_fields)}")
        
        doc.reason = " | ".join(reason_parts)
        doc.next_action = "ASSIGN_TO_ADMIN"

    else:
        doc.status = DocumentStatus.REJECTED
        doc.decision = "AUTO_REJECTED"
        reason_parts = []
        if confidence < 0.60:
            reason_parts.append(f"Low confidence ({confidence:.2f})")
        if has_mismatches:
            reason_parts.append(f"Detected mismatches: {', '.join(mismatches)}")

        doc.reason = " | ".join(reason_parts)
        doc.next_action = "NOTIFY_ADMIN"

    db.commit()
    db.refresh(doc)
    return doc
