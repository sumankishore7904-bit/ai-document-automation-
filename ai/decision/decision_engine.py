from ai.config import (
    HIGH_CONFIDENCE_THRESHOLD,
    MEDIUM_CONFIDENCE_THRESHOLD,
)


def make_decision(
    validation: dict,
    confidence: dict,
) -> dict:

    score = confidence.get("score", 0)
    issues = validation.get("issues", [])

    if not validation.get("valid"):
        mismatch = any(
            issue.get("type") == "mismatch"
            for issue in issues
        )

        if mismatch:
            return {
                "action": "human_review",
                "reason": "Cross-document inconsistency detected.",
                "next_action": "create_review_task",
            }

        if score < MEDIUM_CONFIDENCE_THRESHOLD:
            return {
                "action": "flag",
                "reason": "Document has validation problems and low confidence.",
                "next_action": "flag_for_investigation",
            }

        return {
            "action": "human_review",
            "reason": "Validation issues require human verification.",
            "next_action": "create_review_task",
        }

    if score >= HIGH_CONFIDENCE_THRESHOLD:
        return {
            "action": "auto_process",
            "reason": "Document passed validation with high confidence.",
            "next_action": "process_automatically",
        }

    if score >= MEDIUM_CONFIDENCE_THRESHOLD:
        return {
            "action": "human_review",
            "reason": "Document is valid but confidence is not high enough for automatic processing.",
            "next_action": "create_review_task",
        }

    return {
        "action": "human_review",
        "reason": "Confidence is too low for automatic processing.",
        "next_action": "create_review_task",
    }
