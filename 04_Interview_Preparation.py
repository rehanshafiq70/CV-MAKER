"""
CareerAI - Interview Preparation Studio Page (Phase 9)
"""
import streamlit as st
from utils.helpers import get_app_css
from utils.constants import APP_NAME, CAREER_ROLES
from modules.interview_engine import InterviewEngine

st.set_page_config(
    page_title=f"Interview Preparation | {APP_NAME}",
    page_icon="💼",
    layout="wide"
)

st.markdown(get_app_css(), unsafe_allow_html=True)

st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
  <h1 style="font-size:2rem; font-weight:800; margin-bottom:0.25rem;">💼 Interview Preparation Studio</h1>
  <p style="color:#64748B; margin:0;">
    Generate curated & tailored technical, HR, and resume-grounded interview questions with talking points.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Selected role from state or dropdown
default_role = st.session_state.get("target_role", list(CAREER_ROLES.keys())[0])

col_controls, col_content = st.columns([1, 2], gap="large")

with col_controls:
    st.subheader("1. Configure Interview Set")
    selected_role = st.selectbox("Target Role", options=list(CAREER_ROLES.keys()), index=list(CAREER_ROLES.keys()).index(default_role) if default_role in CAREER_ROLES else 0)

    q_count = st.radio("Number of Questions", options=[10, 20], horizontal=True)

    include_hr = st.checkbox("Include General HR Questions", value=True)

    gen_button = st.button("⚡ Generate Questions", type="primary", use_container_width=True)

    # Resume-based questions check
    has_resume = "parsed_resume" in st.session_state
    if has_resume:
        st.markdown("---")
        st.success("✅ **Active Resume Connected**")
        st.caption("Custom resume-based questions will be included.")

# Process Questions Generation
with col_content:
    if gen_button or selected_role:
        st.subheader(f"2. Questions for {selected_role}")

        # Fetch questions
        questions = InterviewEngine.get_questions_for_role(selected_role, count=q_count, include_hr=include_hr)

        # Include custom resume-based questions if resume loaded
        if has_resume:
            resume_skills = st.session_state["parsed_resume"].get("skills_flat", [])
            custom_resume_qs = InterviewEngine.get_resume_based_questions(resume_skills, selected_role, max_q=3)
            # Insert resume questions at top
            questions = custom_resume_qs + questions
            questions = questions[:q_count]

        st.caption(f"Showing **{len(questions)} curated questions** (Technical, HR & Resume-Specific).")

        for idx, q in enumerate(questions, 1):
            cat = q.get("category", "General")
            badge_color = "#3B82F6" if cat == "Technical" else ("#10B981" if cat == "HR" else "#8B5CF6")

            with st.expander(f"Q{idx}. [{cat}] {q['q']}"):
                st.markdown(f"**Category:** <span style='color:{badge_color}; font-weight:700;'>{cat}</span>", unsafe_allow_html=True)
                st.markdown("**Suggested Answer & Key Talking Points:**")
                st.info(q.get("hint", "Focus on technical accuracy and STAR method structured delivery."))
