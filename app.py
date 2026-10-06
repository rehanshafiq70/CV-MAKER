"""
CareerAI — AI Resume Analyzer & Job Matcher
Modern, SaaS-style career intelligence platform for students, graduates, and professionals.
Phase 1: Project Architecture & Professional Home Page
"""
import streamlit as st
import os
from utils.helpers import get_app_css, is_ai_configured, get_env_var
from utils.constants import APP_NAME, TAGLINE, VERSION, CAREER_ROLES
from database.database import init_db

# Configure page settings
st.set_page_config(
    page_title=f"{APP_NAME} — {TAGLINE}",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom SaaS typography and UI styling
st.markdown(get_app_css(), unsafe_allow_html=True)

# Ensure database tables exist
init_db()

# Mode Detection
ai_active = is_ai_configured()
mode_label = "AI-Enhanced (API Connected)" if ai_active else "Local / Rule-Based Mode (Deterministic)"
mode_color = "#10B981" if ai_active else "#3B82F6"

# Sidebar Branding & Navigation Info
with st.sidebar:
    st.markdown(f"### 🚀 {APP_NAME}")
    st.caption(f"Version {VERSION}")
    st.markdown("---")
    
    st.markdown("#### System Status")
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.05); padding: 0.75rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.8rem; color: #94A3B8;">OPERATIONAL MODE</div>
            <div style="font-weight: 600; color: {mode_color}; font-size: 0.9rem; margin-top: 2px;">
                ● {mode_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("#### Quick Navigation")
    st.page_link("app.py", label="Home Overview", icon="🏠")
    st.page_link("pages/01_Resume_Analyzer.py", label="Resume Analyzer", icon="📄")
    st.page_link("pages/02_Job_Matcher.py", label="Job Matcher", icon="🎯")
    st.page_link("pages/03_Career_Recommendation.py", label="Career Roles", icon="🧭")
    st.page_link("pages/04_Interview_Preparation.py", label="Interview Prep", icon="💼")
    st.page_link("pages/05_About.py", label="About & Privacy", icon="ℹ️")
    
    st.markdown("---")
    st.caption("🔒 **Privacy Guarantee:** Uploads are processed in-memory by default. No PII is logged or permanently stored.")

# Hero Banner
st.markdown(f"""
<div class="hero-container">
    <span class="hero-badge">✦ ENTERPRISE CAREER INTELLIGENCE PLATFORM</span>
    <h1 class="hero-title">{APP_NAME}</h1>
    <p class="hero-subtitle">{TAGLINE}</p>
    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <span class="step-pill">1. Upload Resume</span>
        <span class="step-pill">2. Extract Text</span>
        <span class="step-pill">3. Analyze ATS Score</span>
        <span class="step-pill">4. Extract Skills</span>
        <span class="step-pill">5. Match Job Roles</span>
        <span class="step-pill">6. Prepare Interviews</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Key Platform Metrics / Highlights
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Supported Formats", value="PDF & DOCX", delta="PyMuPDF / docx")
with col_m2:
    st.metric(label="ATS Score Breakdown", value="10 Components", delta="100% Explainable")
with col_m3:
    st.metric(label="Tracked Tech Roles", value=f"{len(CAREER_ROLES)} Roles", delta="Skill Categorization")
with col_m4:
    st.metric(label="Privacy Standard", value="Zero PII Log", delta="Ephemeral Memory")

st.markdown("<br>", unsafe_allow_html=True)

# Main Actions Section
st.subheader("⚡ Core Modules & Actions")
st.write("Select a module below or use the sidebar to begin analyzing your career profile.")

card_col1, card_col2 = st.columns(2)

with card_col1:
    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">📄</span>
        <div class="card-title">Resume Analyzer & ATS Engine</div>
        <div class="card-desc">
            Parse your resume, detect key sections, extract technical skills, and calculate a transparent 
            <b>0–100 ATS Compatibility Score</b> with detailed weighted diagnostics.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/01_Resume_Analyzer.py", label="Open Resume Analyzer →", icon="📄")
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">🧭</span>
        <div class="card-title">Career Role Recommendations</div>
        <div class="card-desc">
            Discover optimal target roles tailored to your background, complete with match percentages, 
            skills you already have, and high-impact skills to learn next.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/03_Career_Recommendation.py", label="Explore Career Recommendations →", icon="🧭")

with card_col2:
    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">🎯</span>
        <div class="card-title">Job Description Matcher</div>
        <div class="card-desc">
            Paste any job posting or select from benchmark tech jobs. Get a transparent match percentage 
            and prioritized skill-gap breakdown (High, Medium, Low).
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/02_Job_Matcher.py", label="Launch Job Matcher →", icon="🎯")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">💼</span>
        <div class="card-title">Interview Preparation Studio</div>
        <div class="card-desc">
            Generate 10 or 20 curated technical, behavioral, and resume-grounded interview questions 
            with model responses and high-scoring talking points.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/04_Interview_Preparation.py", label="Start Interview Prep →", icon="💼")

st.markdown("<br>", unsafe_allow_html=True)

# Architecture & Privacy Banner
st.markdown("""
<div class="privacy-notice">
    <b>🛡️ Security & Privacy Assurance:</b> CareerAI adheres to strict data privacy principles. 
    Resumes uploaded into this platform are parsed securely in temporary session memory and are 
    never retained on disk or logged without explicit confirmation. No personal identifying information (PII) 
    is stored or passed to public indices.
</div>
""", unsafe_allow_html=True)
