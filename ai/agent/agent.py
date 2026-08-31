from .state import AgentState
from .tools import (
    create_review_task,
    generate_report,
    process_automatic_action,
)


def run_agent(
    document_id: str,
    extracted_data: dict,
    validation: dict,
    confidence: dict,
    decision: dict,
) -> dict:

    state: AgentState = {
        "document_id": document_id or "UNKNOWN",
        "document_type": extracted_data.get(
            "document_type",
            "unknown",
        ),
        "extracted_data": extracted_data,
        "validation_results": validation,
        "confidence": confidence,
        "decision": decision,
        "actions_taken": [],
        "errors": [],
    }

    action = decision.get("next_action")

    if action == "process_automatically":

        result = process_automatic_action(
            state["document_id"]
        )

        state["actions_taken"].append(
            "process_automatic_action"
        )

    elif action == "create_review_task":

        result = create_review_task(
            state["document_id"],
            decision.get("reason", "Manual review required."),
        )

        state["actions_taken"].append(
            "create_review_task"
        )

    elif action == "flag_for_investigation":

        result = {
            "status": "flagged",
            "document_id": state["document_id"],
        }

        state["actions_taken"].append(
            "flag_for_investigation"
        )

    else:

        result = {
            "status": "no_action",
            "document_id": state["document_id"],
        }

        state["actions_taken"].append(
            "no_action"
        )

    report = generate_report(
        state["document_id"],
        decision,
    )

    state["actions_taken"].append(
        "generate_report"
    )

    return {
        "status": result.get("status"),
        "actions_taken": state["actions_taken"],
        "action_result": result,
        "report": report,
    }
