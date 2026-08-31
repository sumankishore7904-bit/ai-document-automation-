def check_consistency(documents: list[dict]) -> list[dict]:
    issues = []

    if len(documents) < 2:
        return issues

    income_values = []

    for document in documents:
        data = document.get("data", {})

        income = data.get("income", {})

        if income and income.get("value") is not None:
            try:
                income_values.append(
                    (
                        document.get("document_type"),
                        float(income["value"]),
                    )
                )
            except (ValueError, TypeError):
                pass

    if len(income_values) >= 2:
        first_value = income_values[0][1]

        for document_type, value in income_values[1:]:
            if value != first_value:
                issues.append(
                    {
                        "type": "mismatch",
                        "field": "income",
                        "description": (
                            "Income values do not match across documents."
                        ),
                        "values": income_values,
                    }
                )
                break

    return issues
