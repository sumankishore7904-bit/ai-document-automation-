import pytest

from ai.pipeline import process_document
from ai.validation.validator import validate_document
from ai.validation.consistency import check_consistency
from ai.decision.confidence import calculate_confidence
from ai.decision.decision_engine import make_decision


def test_validation_valid_document():
    classification = {
        "document_type": "application",
        "confidence": 0.95
    }

    extracted = {
        "document_type": "application",
        "data": {
            "name": {
                "value": "Rahul Kumar",
                "confidence": 0.95
            },
            "application_id": {
                "value": "APP1001",
                "confidence": 0.95
            },
            "income": {
                "value": 120000,
                "confidence": 0.95
            },
            "category": {
                "value": "Student",
                "confidence": 0.95
            }
        }
    }

    result = validate_document(
        extracted,
        classification
    )

    assert result["valid"] is True
    assert result["issues"] == []


def test_validation_missing_field():
    classification = {
        "document_type": "application",
        "confidence": 0.95
    }

    extracted = {
        "document_type": "application",
        "data": {
            "name": {
                "value": "Rahul Kumar",
                "confidence": 0.95
            },
            "application_id": {
                "value": "APP1002",
                "confidence": 0.95
            }
        }
    }

    result = validate_document(
        extracted,
        classification
    )

    assert result["valid"] is False

    assert any(
        issue["type"] == "missing"
        for issue in result["issues"]
    )


def test_consistency_matching_documents():

    documents = [
        {
            "document_type": "application",
            "data": {
                "income": {
                    "value": 120000
                }
            }
        },
        {
            "document_type": "certificate",
            "data": {
                "income": {
                    "value": 120000
                }
            }
        }
    ]

    result = check_consistency(documents)

    assert result == []


def test_consistency_mismatch():

    documents = [
        {
            "document_type": "application",
            "data": {
                "income": {
                    "value": 120000
                }
            }
        },
        {
            "document_type": "certificate",
            "data": {
                "income": {
                    "value": 250000
                }
            }
        }
    ]

    result = check_consistency(documents)

    assert len(result) > 0
    assert result[0]["type"] == "mismatch"


def test_confidence_range():

    classification = {
        "confidence": 0.95
    }

    extracted = {
        "data": {
            "name": {
                "confidence": 0.95
            },
            "income": {
                "confidence": 0.90
            }
        }
    }

    validation = {
        "valid": True,
        "issues": []
    }

    result = calculate_confidence(
        classification,
        extracted,
        validation
    )

    assert 0 <= result["score"] <= 1


def test_high_confidence_auto_process():

    validation = {
        "valid": True,
        "issues": []
    }

    confidence = {
        "score": 0.95
    }

    result = make_decision(
        validation,
        confidence
    )

    assert result["action"] == "auto_process"
    assert result["reason"]
    assert result["next_action"]


def test_low_confidence_human_review():

    validation = {
        "valid": True,
        "issues": []
    }

    confidence = {
        "score": 0.65
    }

    result = make_decision(
        validation,
        confidence
    )

    assert result["action"] == "human_review"


def test_invalid_document_requires_review():

    validation = {
        "valid": False,
        "issues": [
            {
                "type": "missing",
                "field": "name",
                "description": "Name missing"
            }
        ]
    }

    confidence = {
        "score": 0.80
    }

    result = make_decision(
        validation,
        confidence
    )

    assert result["action"] == "human_review"


def test_pipeline_returns_structured_result(tmp_path):

    pdf = tmp_path / "sample.pdf"

    import fitz

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
        "DOC-TEST-001"
    )

    assert isinstance(result, dict)

    assert "classification" in result
    assert "extracted_data" in result
    assert "validation" in result
    assert "confidence" in result
    assert "decision" in result
    assert "automation" in result
