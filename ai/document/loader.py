from pathlib import Path

from ai.config import (
    SUPPORTED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
)


class DocumentLoadError(Exception):
    """Raised when a document cannot be loaded."""


def load_document(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise DocumentLoadError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise DocumentLoadError(f"Path is not a file: {file_path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentLoadError(
            f"Unsupported file type: {extension}. "
            f"Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    size_mb = path.stat().st_size / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise DocumentLoadError(
            f"File is too large: {size_mb:.2f} MB. "
            f"Maximum allowed: {MAX_FILE_SIZE_MB} MB."
        )

    return {
        "file_path": str(path.resolve()),
        "file_name": path.name,
        "extension": extension,
        "size_mb": round(size_mb, 3),
    }
