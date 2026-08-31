from uuid import uuid4

from ai.document.loader import load_document
from ai.document.text_extractor import extract_text
from ai.document.classifier import classify_document

from ai.extraction.extractor import extract_information

from ai.validation.validator import validate_document

from ai.decision.confidence import calculate_confidence
from ai.decision.decision_engine import make_decision

from ai.agent.agent import run_agent


def process_document(
    file_path: str,
    document_id: str | None = None,
) -> dict:

    document_id = document_id or f"DOC-{uuid4().hex[:8].upper()}"

    try:

        # 1. Load
        document = load_document(file_path)

        # 2. Extract text
        text_data = extract_text(file_path)

        # 3. Classify
        classification = classify_document(text_data)

        # Stop safely if classification fails.
        if classification["document_type"] == "unknown":

            return {
                "document_id": document_id,
                "status": "review_required",
                "classification": classification,
                "extracted_data": {},
                "validation": {
                    "valid": False,
                    "issues": [
                        {
                            "type": "unknown_document",
                            "field": None,
                            "description": (
                                "Document type could not be determined."
                            ),
                        }
                    ],
                },
                "confidence": {
                    "score": classification.get(
                        "confidence",
                        0,
                    )
                },
                "decision": {
                    "action": "human_review",
                    "reason": (
                        "Document type could not be determined "
                        "with sufficient confidence."
                    ),
                    "next_action": "create_review_task",
                },
                "automation": {
                    "status": "not_executed"
                },
                "errors": [],
            }

        # 4. Extraction
        extracted_data = extract_information(
            text_data,
            classification,
        )

        # 5. Validation
        validation = validate_document(
            extracted_data,
            classification,
        )

        # 6. Confidence
        confidence = calculate_confidence(
            classification,
            extracted_data,
            validation,
        )

        # 7. Decision
        decision = make_decision(
            validation,
            confidence,
        )

        # 8. Agentic workflow
        agent_result = run_agent(
            document_id,
            extracted_data,
            validation,
            confidence,
            decision,
        )

        # 9. Final result
        return {
            "document_id": document_id,

            "status": "success",

            "document": {
                "file_name": document["file_name"],
                "file_type": document["extension"],
                "page_count": text_data["page_count"],
                "extraction_method": text_data[
                    "extraction_method"
                ],
            },

            "classification": classification,

            "extracted_data": extracted_data,

            "validation": validation,

            "confidence": confidence,

            "decision": decision,

            "automation": agent_result,

            "errors": [],
        }

    except Exception as exc:

        return {
            "document_id": document_id,
            "status": "error",
            "classification": None,
            "extracted_data": None,
            "validation": None,
            "confidence": None,
            "decision": {
                "action": "human_review",
                "reason": "Pipeline execution failed.",
                "next_action": "create_review_task",
            },
            "automation": {
                "status": "not_executed"
            },
            "errors": [
                {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            ],
        }
