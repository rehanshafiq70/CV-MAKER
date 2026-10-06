"""
CareerAI - About & Architecture Page
"""
import streamlit as st
from utils.helpers import get_app_css
from utils.constants import APP_NAME, TAGLINE, VERSION, DEFAULT_ATS_WEIGHTS, DEFAULT_JOB_MATCH_WEIGHTS

st.set_page_config(
    page_title=f"About & Privacy | {APP_NAME}",
    page_icon="ℹ️",
    layout="wide"
)

st.markdown(get_app_css(), unsafe_allow_html=True)

st.title("ℹ️ About CareerAI")
st.caption(f"{TAGLINE} • v{VERSION}")

tab1, tab2, tab3 = st.tabs(["Platform Architecture", "Scoring Methodology", "Privacy & Ethics"])

with tab1:
    st.subheader("System Architecture")
    st.markdown("""
    **CareerAI** is engineered as a modular, decoupled SaaS-style career platform:
    - **Frontend:** Streamlit 1.57+ responsive multi-page architecture
    - **Document Extraction:** PyMuPDF (fitz) for PDF text streams, python-docx for DOCX parsing
    - **NLP & Parsing:** Deterministic regex, section partitioners, normalized skill taxonomies
    - **Matching & Similarity:** Scikit-Learn TF-IDF, cosine similarity, sentence-transformers
    - **AI Abstraction Layer:** Configurable LLM adapter (supports Google Gemini, OpenAI, or 100% offline rule-based mode)
    - **Database Layer:** SQLite for local structured persistence
    - **Report Generation:** Automated PDF diagnostic export
    """)

with tab2:
    st.subheader("Explainable Scoring Methodology")
    st.warning("⚠️ **Important Disclaimer:** The CareerAI ATS Compatibility Score is an objective heuristic and does NOT represent any specific commercial vendor's proprietary algorithm.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ATS Score Components (Total = 100)")
        for key, weight in DEFAULT_ATS_WEIGHTS.items():
            st.write(f"- **{key.capitalize()}**: {weight}%")
            
    with col2:
        st.markdown("#### Job Match Score Components (Total = 100)")
        for key, weight in DEFAULT_JOB_MATCH_WEIGHTS.items():
            st.write(f"- **{key.capitalize()}**: {weight}%")

with tab3:
    st.subheader("Privacy, Data Security & Ethical AI")
    st.markdown("""
    - **Zero Permanent Storage by Default:** Resumes uploaded into CareerAI are processed in-memory or in temporary session storage. No resume documents are retained after your session concludes unless you explicitly choose to persist them.
    - **Zero PII Logging:** Personal identifying information such as phone numbers, street addresses, and full contact logs are never emitted to application logs.
    - **No Fake AI:** Scores are deterministic and explainable. When no AI API key is configured, CareerAI operates seamlessly in Rule-Based Local Mode without generating pseudo-random metrics.
    - **No Hallucinated Credentials:** When using AI resume enhancement, CareerAI is strictly constrained to optimize phrasing and action verbs without inventing employers, titles, degrees, or metrics.
    """)
