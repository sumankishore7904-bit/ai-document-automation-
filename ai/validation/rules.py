import re
from datetime import datetime


def is_missing(field: dict) -> bool:
    if not field:
        return True

    value = field.get("value")

    return value is None or str(value).strip() == ""


def validate_required(data: dict, required_fields: list[str]) -> list[dict]:
    issues = []

    for field_name in required_fields:
        field = data.get(field_name, {})

        if is_missing(field):
            issues.append(
                {
                    "type": "missing",
                    "field": field_name,
                    "description": f"Required field '{field_name}' is missing.",
                }
            )

    return issues


def validate_date(field_name: str, field: dict) -> list[dict]:
    if is_missing(field):
        return []

    value = str(field["value"])

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            datetime.strptime(value, fmt)
            return []
        except ValueError:
            pass

    return [
        {
            "type": "invalid_format",
            "field": field_name,
            "description": f"Invalid date format: {value}",
        }
    ]


def validate_positive_number(
    field_name: str,
    field: dict,
) -> list[dict]:

    if is_missing(field):
        return []

    try:
        value = float(field["value"])

        if value < 0:
            raise ValueError

        return []

    except (ValueError, TypeError):
        return [
            {
                "type": "invalid_number",
                "field": field_name,
                "description": f"Invalid numeric value for {field_name}.",
            }
        ]


def validate_application_id(field: dict) -> list[dict]:
    if is_missing(field):
        return []

    value = str(field["value"])

    if not re.match(r"^[A-Za-z0-9_-]+$", value):
        return [
            {
                "type": "invalid_format",
                "field": "application_id",
                "description": "Application ID contains invalid characters.",
            }
        ]

    return []
