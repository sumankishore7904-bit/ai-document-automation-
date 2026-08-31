import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api.backend_client import (
    upload_document,
    BackendError
)


st.title("📤 Upload Document")

st.caption(
    "Upload a document and send it to the AI processing pipeline."
)


uploaded = st.file_uploader(
    "Choose a document",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "docx"
    ],
    help="Maximum file size: 10 MB."
)


if uploaded:

    size_mb = uploaded.size / (
        1024 * 1024
    )

    st.write(
        f"**File:** {uploaded.name}  |  "
        f"**Size:** {size_mb:.2f} MB"
    )

    if size_mb > 10:

        st.error(
            "File is larger than the 10 MB limit."
        )

    else:

        if st.button(
            "🚀 Start AI Processing",
            type="primary",
            use_container_width=True
        ):

            try:

                result = upload_document(
                    uploaded.name,
                    uploaded.getvalue(),
                    uploaded.type
                )

                st.session_state[
                    "document_id"
                ] = result.get("document_id")

                st.session_state[
                    "upload_result"
                ] = result

                st.success(
                    "Document uploaded successfully."
                )

                st.write(
                    "Document ID:",
                    st.session_state["document_id"]
                )

                st.page_link(
                    "pages/2_Processing.py",
                    label="➡️ Continue to Processing"
                )

            except BackendError as exc:

                st.error(str(exc))

else:

    st.info(
        "Upload a PDF, image, or DOCX file to begin."
    )
