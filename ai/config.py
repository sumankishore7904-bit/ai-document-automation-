import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.5-flash")

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

MAX_FILE_SIZE_MB = 10

CLASSIFICATION_THRESHOLD = 0.70

HIGH_CONFIDENCE_THRESHOLD = 0.85
MEDIUM_CONFIDENCE_THRESHOLD = 0.60

SUPPORTED_DOCUMENT_TYPES = {
    "application",
    "certificate",
    "identity_document",
    "invoice",
}
