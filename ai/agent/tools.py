def check_rules(validation_result: dict) -> dict:
    return {
        "valid": validation_result.get("valid", False),
        "issues": validation_result.get("issues", []),
    }


def create_review_task(
    document_id: str,
    reason: str,
) -> dict:

    # Prototype only.
    # Member 1 can later replace this with a backend API call.
    return {
        "status": "review_task_created",
        "document_id": document_id,
        "reason": reason,
    }


def generate_report(
    document_id: str,
    decision: dict,
) -> dict:

    return {
        "document_id": document_id,
        "decision": decision.get("action"),
        "reason": decision.get("reason"),
    }


def process_automatic_action(
    document_id: str,
) -> dict:

    # Prototype action.
    # Replace with backend automation later.
    return {
        "status": "automatic_processing_completed",
        "document_id": document_id,
    }
