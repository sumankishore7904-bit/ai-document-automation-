from pathlib import Path

import fitz


class TextExtractionError(Exception):
    """Raised when text extraction fails."""


def extract_text(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise TextExtractionError(f"File not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise TextExtractionError(
            "MVP currently supports text extraction from PDF files."
        )

    try:
        document = fitz.open(file_path)

        pages = []
        total_text = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

            if text:
                total_text.append(text)

        document.close()

        combined_text = "\n\n".join(total_text)

        extraction_method = (
            "pdf_text" if combined_text.strip() else "no_text"
        )

        return {
            "text": combined_text,
            "page_count": len(pages),
            "pages": pages,
            "extraction_method": extraction_method,
            "text_length": len(combined_text),
        }

    except Exception as exc:
        raise TextExtractionError(
            f"Failed to extract text: {exc}"
        ) from exc
