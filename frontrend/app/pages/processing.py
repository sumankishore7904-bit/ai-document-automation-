import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api.backend_client import (
    get_status,
    BackendError
)


st.title("⚙️ Processing")


document_id = st.session_state.get(
    "document_id"
)


if not document_id:

    st.warning(
        "No document selected. Upload a document first."
    )

    st.page_link(
        "pages/1_Upload.py",
        label="⬅️ Go to Upload"
    )

    st.stop()


try:

    status = get_status(
        document_id
    )

    current = status.get(
        "status",
        "processing"
    ).upper()

    progress = int(
        status.get(
            "progress",
            100 if current == "COMPLETED"
            else 50
        )
    )

    st.metric(
        "Document ID",
        document_id
    )

    st.progress(
        min(
            max(progress, 0),
            100
        )
    )

    st.write(
        f"**Status:** `{current}`"
    )


    if current in (
        "COMPLETED",
        "SUCCESS",
        "PROCESSED"
    ):

        st.success(
            "AI processing completed."
        )

        st.page_link(
            "pages/3_Results.py",
            label="➡️ View AI Results"
        )


    elif current in (
        "FAILED",
        "ERROR"
    ):

        st.error(
            "Document processing failed."
        )


    else:

        st.info(
            "The AI pipeline is still processing "
            "this document. Refresh the page to check again."
        )


except BackendError as exc:

    st.error(str(exc))
