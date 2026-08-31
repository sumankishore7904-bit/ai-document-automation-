import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api.backend_client import (
    get_result,
    BackendError
)


st.title("🤖 AI Results")


document_id = st.session_state.get(
    "document_id"
)


if not document_id:

    st.warning(
        "No document selected. Upload a document first."
    )

    st.stop()


try:

    data = get_result(
        document_id
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Document Type",
        data.get(
            "document_type",
            "Unknown"
        )
    )


    c2.metric(
        "AI Confidence",
        f"{data.get('confidence', 0)}%"
    )


    c3.metric(
        "Decision",
        data.get(
            "decision",
            "PENDING"
        )
    )


    st.subheader(
        "Extracted Fields"
    )


    fields = data.get(
        "fields",
        {}
    )


    if fields:

        for key, value in fields.items():

            left, right = st.columns(
                [1, 2]
            )

            left.write(
                f"**{key}**"
            )

            right.write(
                str(value)
            )

    else:

        st.info(
            "No extracted fields returned by the backend."
        )


    st.subheader(
        "Validation"
    )


    validation = data.get(
        "validation",
        {}
    )


    if validation.get("status") in (
        "passed",
        "PASS",
        "PASSED"
    ):

        st.success(
            "✅ Validation passed"
        )

    else:

        st.warning(
            "Validation status: "
            + str(
                validation.get(
                    "status",
                    "unknown"
                )
            )
        )


    st.write(
        validation.get(
            "message",
            ""
        )
    )


    st.subheader(
        "Workflow Decision"
    )


    decision = data.get(
        "decision",
        "PENDING"
    )


    if decision == "AUTO_APPROVED":

        st.success(
            "🟢 Automatically approved by the AI workflow."
        )


    elif decision in (
        "REVIEW",
        "HUMAN_REVIEW"
    ):

        st.warning(
            "🟡 Sent to a human reviewer."
        )

        st.page_link(
            "pages/4_Review.py",
            label="➡️ Open Human Review"
        )


    elif decision == "REJECTED":

        st.error(
            "🔴 Document rejected."
        )


    else:

        st.info(
            f"Current decision: {decision}"
        )


except BackendError as exc:

    st.error(str(exc))
