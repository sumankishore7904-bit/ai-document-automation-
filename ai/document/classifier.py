import json
import re

from ai.config import (
    AI_API_KEY,
    AI_MODEL,
    CLASSIFICATION_THRESHOLD,
    SUPPORTED_DOCUMENT_TYPES,
)


def _keyword_classification(text: str) -> dict:
    text_lower = text.lower()

    scores = {
        "application": 0.0,
        "certificate": 0.0,
        "identity_document": 0.0,
        "invoice": 0.0,
    }

    keywords = {
        "application": [
            "application",
            "applicant",
            "application id",
            "apply",
        ],
        "certificate": [
            "certificate",
            "certify",
            "certification",
        ],
        "identity_document": [
            "aadhaar",
            "passport",
            "identity",
            "date of birth",
            "id number",
        ],
        "invoice": [
            "invoice",
            "invoice number",
            "subtotal",
            "total amount",
            "tax",
        ],
    }

    for document_type, words in keywords.items():
        for word in words:
            if word in text_lower:
                scores[document_type] += 1

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    total_score = sum(scores.values())

    if total_score == 0:
        return {
            "document_type": "unknown",
            "confidence": 0.0,
            "method": "keyword",
        }

    confidence = min(best_score / max(total_score, 1), 1.0)

    if confidence < CLASSIFICATION_THRESHOLD:
        return {
            "document_type": "unknown",
            "confidence": round(confidence, 3),
            "method": "keyword",
        }

    return {
        "document_type": best_type,
        "confidence": round(confidence, 3),
        "method": "keyword",
    }


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in AI response.")

    return json.loads(match.group())


def _llm_classification(text: str) -> dict:
    if not AI_API_KEY:
        return _keyword_classification(text)

    try:
        from google import genai

        client = genai.Client(api_key=AI_API_KEY)

        prompt = f"""
Classify the following document.

Allowed document types:
{sorted(SUPPORTED_DOCUMENT_TYPES)}

Rules:
- Do not invent information.
- If uncertain, return "unknown".
- Return JSON only.
- Confidence must be between 0 and 1.

Required JSON:
{{
  "document_type": "application|certificate|identity_document|invoice|unknown",
  "confidence": 0.0
}}

DOCUMENT:
{text[:15000]}
"""

        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt,
        )

        result = _extract_json(response.text)

        document_type = result.get("document_type", "unknown")
        confidence = float(result.get("confidence", 0))

        if (
            document_type not in SUPPORTED_DOCUMENT_TYPES
            or confidence < CLASSIFICATION_THRESHOLD
        ):
            document_type = "unknown"

        return {
            "document_type": document_type,
            "confidence": round(confidence, 3),
            "method": "llm",
        }

    except Exception:
        # Safe fallback instead of allowing an LLM failure
        # to silently corrupt the pipeline.
        return _keyword_classification(text)


def classify_document(text_data: dict) -> dict:
    text = text_data.get("text", "").strip()

    if not text:
        return {
            "document_type": "unknown",
            "confidence": 0.0,
            "method": "no_text",
        }

    return _llm_classification(text)
