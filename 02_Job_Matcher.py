"""
CareerAI - Job Matcher & Skill Gap Analyzer Page (Phase 6)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.helpers import get_app_css, get_score_badge_class
from utils.constants import APP_NAME
from modules.job_matcher import JobMatcher

st.set_page_config(
    page_title=f"Job Matcher | {APP_NAME}",
    page_icon="🎯",
    layout="wide"
)

st.markdown(get_app_css(), unsafe_allow_html=True)

st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
  <h1 style="font-size:2rem; font-weight:800; margin-bottom:0.25rem;">🎯 Job Description Matcher</h1>
  <p style="color:#64748B; margin:0;">
    Compare your active resume against any target job description & get a prioritized skill gap breakdown.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sample Job Descriptions for Dataset Selection
SAMPLE_JOBS = {
    "Python / Django Developer": """
Job Title: Python Developer
Experience Required: 2+ years of experience
Qualifications: Bachelor in Computer Science or related field

Required Skills:
- Python
- Django or FastAPI
- SQL and PostgreSQL
- Git
- REST API

Preferred Skills:
- Docker
- AWS
- Redis
- React

Responsibilities:
Develop scalable backend services, build RESTful APIs, optimize SQL database queries, and collaborate with frontend developers.
""",
    "Data Scientist": """
Job Title: Data Scientist
Experience Required: 3+ years of experience
Qualifications: Master or Bachelor in Data Science, Statistics, Computer Science

Required Skills:
- Python
- Machine Learning
- Pandas
- NumPy
- SQL
- Scikit-Learn

Preferred Skills:
- Deep Learning
- PyTorch
- Tableau
- Docker

Responsibilities:
Build predictive models, clean and analyze large datasets, extract business insights, and deploy ML models into production.
""",
    "Full Stack Developer": """
Job Title: Full Stack Web Developer
Experience Required: 2+ years of experience
Qualifications: Bachelor degree in CS or equivalent experience

Required Skills:
- JavaScript
- HTML
- CSS
- React
- Python
- SQL

Preferred Skills:
- Node.js
- Docker
- MongoDB
- Git

Responsibilities:
Design user interfaces with React, develop backend APIs using Python/Node.js, write efficient SQL queries, and manage deployments.
"""
}

# ── Session State Resume Check ───────────────────────────────────────
has_resume = "parsed_resume" in st.session_state

if not has_resume:
    st.warning("⚠️ **No active resume loaded in session.** You can still paste a job description below, but for a full match comparison, please upload your resume on the **Resume Analyzer** page first.")
    st.page_link("pages/01_Resume_Analyzer.py", label="📄 Go to Resume Analyzer to upload resume", type="primary")
    st.markdown("<br>", unsafe_allow_html=True)

# ── Job Description Input Section ─────────────────────────────────────
col_input, col_results = st.columns([1, 1.4], gap="large")

with col_input:
    st.subheader("1. Target Job Description")
    tab_paste, tab_sample = st.tabs(["Paste Job Description", "Choose Benchmark Job"])

    job_text_input = ""

    with tab_paste:
        job_text_input = st.text_area(
            "Paste Job Description Here",
            height=250,
            placeholder="Paste complete job requirements, qualifications, and responsibilities..."
        )

    with tab_sample:
        selected_sample = st.selectbox("Select Benchmark Role", options=list(SAMPLE_JOBS.keys()))
        if selected_sample:
            job_text_input = SAMPLE_JOBS[selected_sample]
            st.text_area("Selected Job Posting Preview", value=job_text_input, height=180, disabled=True)

    match_button = st.button("🎯 Calculate Job Match Score", type="primary", use_container_width=True)

# ── Match Processing & Results ────────────────────────────────────────
if match_button or (has_resume and job_text_input.strip()):
    if not job_text_input.strip():
        with col_results:
            st.error("Please paste or select a job description first.")
            st.stop()

    with col_results:
        with st.spinner("⚡ Matching resume against job description..."):
            matcher = JobMatcher()

            # Parse Job Description
            job_data = matcher.parse_job_description(job_text_input)

            # Get resume data from session state or dummy if not loaded
            if has_resume:
                p_data = st.session_state["parsed_resume"]
                resume_data = {
                    "raw_text": p_data["raw_text"],
                    "sections": p_data["sections"],
                    "skills_flat": p_data["skills_flat"],
                    "skills_categorized": p_data["skills"],
                }
            else:
                resume_data = {
                    "raw_text": "",
                    "sections": {},
                    "skills_flat": [],
                    "skills_categorized": {},
                }

            match_result = matcher.match(resume_data, job_data)

        # ── Hero Match Score Card ────────────────────────────────────
        score = match_result["match_score"]
        badge_color = get_score_badge_class(score)
        label = match_result["match_label"]

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A, #1E3A5F);
            border-radius: 16px;
            padding: 1.8rem;
            text-align: center;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        ">
            <div style="color:#94A3B8; font-size:0.85rem; font-weight:600; text-transform:uppercase;">
                Overall Job Match Score
            </div>
            <div style="font-size:4rem; font-weight:900; color:{badge_color}; line-height:1.1; margin: 0.25rem 0;">
                {score:.0f}%
            </div>
            <div style="color:#CBD5E1; font-size:1rem; font-weight:600;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Component Breakdown Table ─────────────────────────────────
        st.markdown("#### 📊 Match Breakdown")
        breakdown = match_result["breakdown"]

        rows = []
        for key, comp in breakdown.items():
            rows.append({
                "Component": key.capitalize(),
                "Weight": f"{comp['weight']}%",
                "Raw Score": f"{comp['raw_score']:.1f}%",
                "Weighted Contribution": f"{comp['weighted']:.1f}%"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()

        # ── Skill Gap Analysis Tabs ──────────────────────────────────
        st.markdown("### 🔍 Skill Gap Analysis")

        tab_have, tab_req, tab_missing = st.tabs([
            "✅ Skills You Have",
            "📋 Skills Required",
            "⚠️ Missing Skills & Priorities"
        ])

        with tab_have:
            matching = match_result["matching_skills"]
            if matching:
                pills = " ".join(
                    f'<span style="display:inline-block; background:#D1FAE5; color:#065F46; border:1px solid #6EE7B7; border-radius:6px; padding:0.3rem 0.7rem; font-weight:600; margin:0.2rem;">{s}</span>'
                    for s in matching
                )
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("No matching skills found between resume and job posting.")

        with tab_req:
            all_req = match_result["all_job_skills"]
            if all_req:
                pills = " ".join(
                    f'<span style="display:inline-block; background:#EFF6FF; color:#1E40AF; border:1px solid #93C5FD; border-radius:6px; padding:0.3rem 0.7rem; font-weight:600; margin:0.2rem;">{s}</span>'
                    for s in all_req
                )
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("No explicit technical skills extracted from this job description.")

        with tab_missing:
            priority = match_result["priority"]
            high = priority.get("High", [])
            medium = priority.get("Medium", [])
            low = priority.get("Low", [])

            if high or medium or low:
                col_h, col_m, col_l = st.columns(3)
                with col_h:
                    st.markdown("##### 🔴 High Priority")
                    if high:
                        for s in high:
                            st.markdown(f"- **{s}**")
                    else:
                        st.caption("None")

                with col_m:
                    st.markdown("##### 🟡 Medium Priority")
                    if medium:
                        for s in medium:
                            st.markdown(f"- **{s}**")
                    else:
                        st.caption("None")

                with col_l:
                    st.markdown("##### 🟢 Low Priority")
                    if low:
                        for s in low:
                            st.markdown(f"- **{s}**")
                    else:
                        st.caption("None")
            else:
                st.success("🎉 You possess all required skills for this job description!")

elif not match_button and not job_text_input:
    with col_results:
        st.markdown("""
        <div style="border: 2px dashed #CBD5E1; border-radius: 16px; padding: 3rem 2rem; text-align: center; color: #94A3B8;">
            <div style="font-size:3rem; margin-bottom:1rem;">🎯</div>
            <div style="font-size:1.1rem; font-weight:600; margin-bottom:0.5rem;">Job Match Results Will Appear Here</div>
            <div style="font-size:0.9rem;">Paste a job description or choose a benchmark job on the left to calculate your match score.</div>
        </div>
        """, unsafe_allow_html=True)
