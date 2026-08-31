import streamlit as st

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 1.5rem 1.8rem;
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 18px;
    margin-bottom: 1.2rem;
}

.step {
    text-align: center;
    padding: .7rem;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,.2);
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📄 DocuMind AI")
st.sidebar.caption("Intelligent Document Processing")
st.sidebar.divider()

st.sidebar.info(
    "Upload documents, monitor AI processing, "
    "review results and manage human-review decisions."
)

st.markdown("""
<div class="hero">
<h1>📄 DocuMind AI</h1>
<p style="font-size:1.1rem">
AI-powered document extraction, validation and human-review automation.
</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(7)

steps = [
    "Upload",
    "Processing",
    "AI Results",
    "Validation",
    "Decision",
    "Human Review",
    "Dashboard",
]

for col, step in zip(cols, steps):
    col.markdown(
        f'<div class="step"><b>{step}</b></div>',
        unsafe_allow_html=True
    )

st.write("")

st.subheader("Welcome")

st.write(
    "Start by uploading an invoice, receipt, application, "
    "contract, or other supported document."
)

st.page_link(
    "pages/1_Upload.py",
    label="🚀 Upload a Document"
)

st.page_link(
    "pages/2_Processing.py",
    label="⚙️ View Processing Status"
)

st.page_link(
    "pages/3_Results.py",
    label="🤖 View AI Results"
)

st.page_link(
    "pages/4_Review.py",
    label="👤 Human Review"
)

st.page_link(
    "pages/5_Dashboard.py",
    label="📊 Dashboard"
)
