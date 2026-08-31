from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    document_id: str
    document_type: str
    extracted_data: dict[str, Any]
    validation_results: dict[str, Any]
    confidence: dict[str, Any]
    decision: dict[str, Any]
    actions_taken: list[str]
    errors: list[str]
