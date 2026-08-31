import json
import re
from typing import Type

from pydantic import BaseModel

from ai.config import AI_API_KEY, AI_MODEL
from .schemas import SCHEMA_MAP


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("AI did not return JSON.")

    return json.loads(match.group())


def _empty_schema(schema_class: Type[BaseModel]) -> dict:
    model = schema_class()
    return model.model_dump()


def _llm_extract(text: str, document_type: str) -> dict:
    schema_class = SCHEMA_MAP[document_type]

    if not AI_API_KEY:
        return _empty_schema(schema_class)

    from google import genai

    client = genai.Client(api_key=AI_API_KEY)

    schema = schema_class.model_json_schema()

    prompt = f"""
Extract structured information from this {document_type}.

STRICT RULES:
1. Never invent information.
2. If a value is missing, use null.
3. Preserve the original value where appropriate.
4. Include page/source information when possible.
5. Every confidence value must be between 0 and 1.
6. Return JSON only.
7. Follow this schema exactly.

SCHEMA:
{json.dumps(schema, indent=2)}

DOCUMENT:
{text[:20000]}
"""

    response = client.models.generate_content(
        model=AI_MODEL,
        contents=prompt,
    )

    raw = _extract_json(response.text)

    validated = schema_class.model_validate(raw)

    return validated.model_dump()


def extract_information(
    text_data: dict,
    classification: dict,
) -> dict:

    document_type = classification.get("document_type")

    if document_type not in SCHEMA_MAP:
        return {
            "document_type": document_type,
            "data": {},
            "error": "Unknown document type.",
        }

    text = text_data.get("text", "")

    try:
        data = _llm_extract(text, document_type)

        return {
            "document_type": document_type,
            "data": data,
            "error": None,
        }

    except Exception as exc:
        return {
            "document_type": document_type,
            "data": _empty_schema(SCHEMA_MAP[document_type]),
            "error": str(exc),
        }
