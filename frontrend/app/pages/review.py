import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api.backend_client import (
    get_pending_reviews,
    submit_decision,
    BackendError
)


st.title("👤 Human Review")

st.caption(
    "Review low-confidence documents and make the final decision."
)


try:

    data = get_pending_reviews()

    reviews = data.get(
        "reviews",
        []
    )


    if not reviews:

        st.success(
            "🎉 No documents are waiting for human review."
        )

        st.stop()


    for item in reviews:

        with st.container(border=True):

            st.subheader(
                item.get(
                    "file_name",
                    "Document"
                )
            )


            c1, c2, c3 = st.columns(3)


            c1.write(
                f"**Type:** "
                f"{item.get('document_type', 'Unknown')}"
            )


            c2.write(
                f"**Confidence:** "
                f"{item.get('confidence', 0)}%"
            )


            c3.write(
                f"**Reason:** "
                f"{item.get('reason', 'Manual review required')}"
            )


            comment = st.text_area(
                "Reviewer comment",
                key=f"comment_{item.get('id')}",
                placeholder=(
                    "Add an optional reason or correction..."
                )
            )


            a, b, c = st.columns(3)


            try:

                if a.button(
                    "✅ Approve",
                    key=f"approve_{item.get('id')}",
                    use_container_width=True
                ):

                    result = submit_decision(
                        item["id"],
                        "APPROVED",
                        comment
                    )

                    st.success(
                        "Document approved."
                    )

                    st.json(result)


                if b.button(
                    "❌ Reject",
                    key=f"reject_{item.get('id')}",
                    use_container_width=True
                ):

                    result = submit_decision(
                        item["id"],
                        "REJECTED",
                        comment
                    )

                    st.error(
                        "Document rejected."
                    )

                    st.json(result)


                if c.button(
                    "✏️ Request Correction",
                    key=f"correct_{item.get('id')}",
                    use_container_width=True
                ):

                    result = submit_decision(
                        item["id"],
                        "CORRECTION_REQUIRED",
                        comment
                    )

                    st.warning(
                        "Correction requested."
                    )

                    st.json(result)


            except BackendError as exc:

                st.error(str(exc))


except BackendError as exc:

    st.error(str(exc))
