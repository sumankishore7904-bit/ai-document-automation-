from .rules import (
    validate_required,
    validate_date,
    validate_positive_number,
    validate_application_id,
)


REQUIRED_FIELDS = {
    "application": [
        "name",
        "application_id",
    ],
    "certificate": [
        "name",
        "certificate_number",
    ],
    "identity_document": [
        "name",
        "id_number",
    ],
    "invoice": [
        "invoice_number",
        "vendor",
    ],
}


def validate_document(
    extracted_data: dict,
    classification: dict,
) -> dict:

    document_type = classification.get("document_type")
    data = extracted_data.get("data", {})

    if document_type == "unknown":
        return {
            "valid": False,
            "issues": [
                {
                    "type": "unknown_document",
                    "field": None,
                    "description": "Document type could not be determined.",
                }
            ],
        }

    issues = []

    required = REQUIRED_FIELDS.get(document_type, [])

    issues.extend(
        validate_required(
            data,
            required,
        )
    )

    if "date" in data:
        issues.extend(
            validate_date(
                "date",
                data["date"],
            )
        )

    if "issue_date" in data:
        issues.extend(
            validate_date(
                "issue_date",
                data["issue_date"],
            )
        )

    if "invoice_date" in data:
        issues.extend(
            validate_date(
                "invoice_date",
                data["invoice_date"],
            )
        )

    if "income" in data:
        issues.extend(
            validate_positive_number(
                "income",
                data["income"],
            )
        )

    if "total_amount" in data:
        issues.extend(
            validate_positive_number(
                "total_amount",
                data["total_amount"],
            )
        )

    if "application_id" in data:
        issues.extend(
            validate_application_id(
                data["application_id"]
            )
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
    }
