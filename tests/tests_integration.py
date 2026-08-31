import fitz

from ai.pipeline import process_document


def create_pdf(path, text):

    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (50, 50),
        text
    )

    document.save(path)
    document.close()


def test_valid_document_workflow(tmp_path):

    pdf = tmp_path / "valid.pdf"

    create_pdf(
        pdf,
        """
        APPLICATION

        Name: Rahul Kumar
        Application ID: APP1001
        Income: 120000
        Category: Student
        Date: 2026-08-30
        """
    )

    result = process_document(
        str(pdf),
        "DOC-VALID"
    )

    assert result["status"] in {
        "success",
        "review_required"
    }

    assert result["classification"] is not None
    assert result["extracted_data"] is not None
    assert result["validation"] is not None
    assert result["confidence"] is not None
    assert result["decision"] is not None
    assert result["automation"] is not None


def test_unknown_document_workflow(tmp_path):

    pdf = tmp_path / "unknown.pdf"

    create_pdf(
        pdf,
        """
        The weather today is pleasant.
        Trees are green.
        The sky is blue.
        This document contains no application information.
        """
    )

    result = process_document(
        str(pdf),
        "DOC-UNKNOWN"
    )

    assert result["classification"]["document_type"] == "unknown"

    assert result["decision"]["action"] == "human_review"


def test_bad_file_workflow(tmp_path):

    bad_file = tmp_path / "bad.exe"

    bad_file.write_text(
        "This is not a supported document."
    )

    result = process_document(
        str(bad_file),
        "DOC-BAD"
    )

    assert result["status"] == "error"

    assert len(result["errors"]) > 0
