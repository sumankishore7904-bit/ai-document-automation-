from ai.pipeline import process_document


REQUIRED_AI_FIELDS = {
    "document_id",
    "classification",
    "extracted_data",
    "validation",
    "confidence",
    "decision",
    "automation",
}


def test_backend_ai_contract(tmp_path):

    import fitz

    pdf = tmp_path / "backend_test.pdf"

    document = fitz.open()
    page = document.new_page()

    page.insert_text(
        (50, 50),
        """
        Application
        Name: Rahul Kumar
        Application ID: APP1001
        Income: 120000
        Category: Student
        """
    )

    document.save(pdf)
    document.close()

    result = process_document(
        str(pdf),
        "DOC-BACKEND-001"
    )

    assert isinstance(result, dict)

    missing = REQUIRED_AI_FIELDS - result.keys()

    assert not missing, (
        f"AI/backend contract missing fields: {missing}"
    )


def test_backend_receives_document_id(tmp_path):

    import fitz

    pdf = tmp_path / "id_test.pdf"

    document = fitz.open()
    page = document.new_page()

    page.insert_text(
        (50, 50),
        "Application Name Rahul Kumar"
    )

    document.save(pdf)
    document.close()

    result = process_document(
        str(pdf),
        "DOC-123"
    )

    assert result["document_id"] == "DOC-123"
