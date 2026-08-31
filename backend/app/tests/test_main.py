from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_file_upload():
    response = client.post(
        "/documents/upload",
        files={"file": ("test.txt", b"invalid text content", "text/plain")}
    )
    assert response.status_code == 400

def test_full_pipeline_flow():
    # 1. Upload
    response = client.post(
        "/documents/upload",
        files={"file": ("test.pdf", b"%PDF-1.4 dummy pdf content", "application/pdf")}
    )
    assert response.status_code == 200
    doc_id = response.json()["document_id"]

    # 2. Status Check
    status_resp = client.get(f"/documents/{doc_id}/status")
    assert status_resp.json()["status"] == "UPLOADED"

    # 3. AI Result Ingestion
    ai_payload = {
        "document_id": doc_id,
        "document_type": "tax_form",
        "extracted_data": {"name": "Jane Doe", "income": 85000},
        "validation": {"status": "VALID", "missing_fields": [], "mismatches": []},
        "confidence": 0.95
    }
    ai_resp = client.post("/results/ai-output", json=ai_payload)
    assert ai_resp.status_code == 200
    assert ai_resp.json()["status"] == "COMPLETED"
