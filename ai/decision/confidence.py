def _average_extraction_confidence(data: dict) -> float:
    values = []

    for field in data.values():
        if isinstance(field, dict):
            confidence = field.get("confidence")

            if isinstance(confidence, (int, float)):
                values.append(float(confidence))

    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_confidence(
    classification: dict,
    extracted_data: dict,
    validation: dict,
) -> dict:

    classification_confidence = float(
        classification.get("confidence", 0)
    )

    data = extracted_data.get("data", {})

    extraction_confidence = _average_extraction_confidence(data)

    validation_score = 1.0 if validation.get("valid") else 0.5

    issue_penalty = min(
        len(validation.get("issues", [])) * 0.10,
        0.5,
    )

    final_score = (
        classification_confidence * 0.35
        + extraction_confidence * 0.40
        + validation_score * 0.25
        - issue_penalty
    )

    final_score = max(0.0, min(final_score, 1.0))

    return {
        "score": round(final_score, 3),
        "signals": {
            "classification": round(
                classification_confidence,
                3,
            ),
            "extraction": round(
                extraction_confidence,
                3,
            ),
            "validation": validation_score,
            "issue_penalty": issue_penalty,
        },
    }
