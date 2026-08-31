import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """
    Validates file extension and size, saves it to disk,
    and returns a tuple of (unique_document_id, original_filename).
    """
    # 1. Validate file extension
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 2. Check file size against environment limits
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )

    # 3. Generate secure unique document ID
    doc_id = f"DOC-{uuid.uuid4().hex[:6].upper()}"

    # 4. Save to target directory
    destination_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}{ext}")
    with open(destination_path, "wb") as buffer:
        buffer.write(file.file.read())

    return doc_id, file.filename
