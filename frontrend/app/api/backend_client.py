import os
import requests


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
).rstrip("/")

DEMO_MODE = os.getenv(
    "DEMO_MODE",
    "true"
).lower() == "true"

TIMEOUT = 30


class BackendError(Exception):
    pass


def _request(method, path, **kwargs):

    url = f"{BACKEND_URL}{path}"

    try:

        response = requests.request(
            method,
            url,
            timeout=TIMEOUT,
            **kwargs
        )

        response.raise_for_status()

        if not response.content:
            return {}

        return response.json()

    except requests.RequestException as exc:

        raise BackendError(
            f"Backend request failed: {exc}"
        ) from exc


def upload_document(
    file_name,
    file_bytes,
    content_type
):

    if DEMO_MODE:

        return {
            "document_id": "demo-001",
            "status": "processing",
            "file_name": file_name
        }

    return _request(
        "POST",
        "/documents/upload",
        files={
            "file": (
                file_name,
                file_bytes,
                content_type
            )
        }
    )


def get_status(document_id):

    if DEMO_MODE:

        return {
            "document_id": document_id,
            "status": "completed",
            "progress": 100
        }

    return _request(
        "GET",
        f"/documents/{document_id}/status"
    )


def get_result(document_id):

    if DEMO_MODE:

        return {
            "document_id": document_id,
            "status": "completed",
            "document_type": "Invoice",
            "confidence": 94,

            "fields": {
                "Invoice Number": "INV-2026-1042",
                "Vendor": "Acme Technologies",
                "Invoice Date": "31-08-2026",
                "Total Amount": "₹48,500",
                "Tax": "₹7,373",
                "Due Date": "30-09-2026"
            },

            "validation": {
                "status": "passed",
                "message": "All required fields passed validation."
            },

            "decision": "AUTO_APPROVED"
        }

    return _request(
        "GET",
        f"/documents/{document_id}/result"
    )


def get_pending_reviews():

    if DEMO_MODE:

        return {
            "reviews": [
                {
                    "id": "demo-001",
                    "file_name": "invoice_demo.pdf",
                    "document_type": "Invoice",
                    "confidence": 72,
                    "reason": "Low confidence in vendor field"
                }
            ]
        }

    return _request(
        "GET",
        "/reviews/pending"
    )


def submit_decision(
    review_id,
    decision,
    comment=""
):

    if DEMO_MODE:

        return {
            "review_id": review_id,
            "decision": decision,
            "comment": comment,
            "status": "success"
        }

    return _request(
        "POST",
        f"/reviews/{review_id}/decision",
        json={
            "decision": decision,
            "comment": comment
        }
    )


def get_dashboard_stats():

    if DEMO_MODE:

        return {
            "total_documents": 1284,
            "processed": 1241,
            "pending_review": 29,
            "approved": 1180,
            "rejected": 32,
            "average_confidence": 93.6
        }

    return _request(
        "GET",
        "/dashboard/stats"
    )
