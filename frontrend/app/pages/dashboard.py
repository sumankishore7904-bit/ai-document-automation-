import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from api.backend_client import (
    get_dashboard_stats,
    BackendError
)


st.title("📊 Dashboard")

st.caption(
    "Overview of the intelligent document processing pipeline."
)


try:

    stats = get_dashboard_stats()


    cols = st.columns(6)


    labels = [

        ("Total Documents",
         "total_documents"),

        ("Processed",
         "processed"),

        ("Pending Review",
         "pending_review"),

        ("Approved",
         "approved"),

        ("Rejected",
         "rejected"),

        ("Avg. Confidence",
         "average_confidence")
    ]


    for col, (label, key) in zip(
        cols,
        labels
    ):

        value = stats.get(
            key,
            0
        )


        if key == "average_confidence":

            value = f"{value}%"


        col.metric(
            label,
            value
        )


    st.divider()


    total = stats.get(
        "total_documents",
        0
    )


    processed = stats.get(
        "processed",
        0
    )


    pending = stats.get(
        "pending_review",
        0
    )


    st.subheader(
        "Pipeline Health"
    )


    if total:

        percentage = (
            processed / total
        ) * 100


        st.write(
            f"Processed: **{percentage:.1f}%**"
        )


        st.progress(
            min(
                processed / total,
                1.0
            )
        )


        st.write(
            f"Pending human review: **{pending}**"
        )


    else:

        st.info(
            "No dashboard data available."
        )


except BackendError as exc:

    st.error(str(exc))
