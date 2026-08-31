from ai.pipeline import process_document


FRONTEND_REQUIRED_FIELDS = [
    "classification",
    "extracted_data",
    "validation",
    "confidence",
    "decision",
    "automation",
]


def test_frontend_data_contract(tmp_path):

    import fitz

    pdf = tmp_path / "frontend_test.pdf"

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
        "DOC-FRONTEND-001"
    )

    for field in FRONTEND_REQUIRED_FIELDS:
        assert field in result


def test_frontend_can_display_decision(tmp_path):

    import fitz

    pdf = tmp_path / "decision_test.pdf"

    document = fitz.open()
    page = document.new_page()

    page.insert_text(
        (50, 50),
        """
        Application
        Name: Rahul Kumar
        Application ID: APP1001
        """
    )

    document.save(pdf)
    document.close()

    result = process_document(
        str(pdf),
        "DOC-FRONTEND-002"
    )

    decision = result["decision"]

    assert "action" in decision
    assert "reason" in decision
    assert "next_action" in decision
