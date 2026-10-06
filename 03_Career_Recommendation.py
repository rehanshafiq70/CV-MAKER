"""
CareerAI - Career Role Recommendation Page (Phase 8)
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import get_app_css, get_score_badge_class
from utils.constants import APP_NAME
from modules.career_engine import CareerEngine

st.set_page_config(
    page_title=f"Career Recommendations | {APP_NAME}",
    page_icon="🧭",
    layout="wide"
)

st.markdown(get_app_css(), unsafe_allow_html=True)

st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
  <h1 style="font-size:2rem; font-weight:800; margin-bottom:0.25rem;">🧭 Career Pathway Recommendations</h1>
  <p style="color:#64748B; margin:0;">
    Discover target industry roles best aligned with your verified technical skills & background.
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Get skills from active session or fallback
has_resume = "parsed_resume" in st.session_state

if has_resume:
    p_data = st.session_state["parsed_resume"]
    resume_skills = p_data.get("skills_flat", [])
    sections = p_data.get("sections", {})
    st.success(f"✅ **Active Resume Loaded:** Using **{len(resume_skills)} extracted skills** for career role matching.")
else:
    st.info("💡 **No active resume loaded in session.** Showing default recommendations. Upload your resume on the Resume Analyzer page for personalized recommendations.")
    resume_skills = ["Python", "SQL", "Git", "Data Analysis", "HTML", "CSS"]
    sections = {}

# Compute Recommendations
recs = CareerEngine.recommend_roles(resume_skills, sections, top_n=12)

# Top match hero banner
if recs:
    top_role = recs[0]
    badge_color = get_score_badge_class(top_role["match_pct"])

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0F172A, #1E3A5F);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        color: white;
    ">
        <div style="color:#94A3B8; font-size:0.85rem; font-weight:600; text-transform:uppercase;">
            Top Aligned Career Pathway
        </div>
        <div style="font-size:2.4rem; font-weight:800; margin:0.3rem 0; color:#F8FAFC;">
            {top_role['role']} <span style="color:{badge_color}; font-size:2rem;">({top_role['match_pct']:.0f}% Match)</span>
        </div>
        <div style="color:#CBD5E1; font-size:0.95rem;">
            <b>Category:</b> {top_role['category']} &nbsp;|&nbsp; 
            <b>Matching Skills:</b> {', '.join(top_role['matching_skills'][:5]) or 'Basic alignment'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Grid Layout of Role Recommendations
st.subheader("🎯 Role Compatibility Ranking")

cols = st.columns(3)

for idx, item in enumerate(recs):
    with cols[idx % 3]:
        score = item["match_pct"]
        badge_color = get_score_badge_class(score)

        st.markdown(f"""
        <div class="feature-card" style="margin-bottom: 1.2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <div class="card-title" style="margin:0;">{item['role']}</div>
                <span style="background:{badge_color}; color:white; font-weight:700; border-radius:999px; padding:0.2rem 0.6rem; font-size:0.85rem;">
                    {score:.0f}%
                </span>
            </div>
            <div class="card-desc" style="margin-bottom:0.5rem;">
                <b>Category:</b> {item['category']}<br>
                <b>Matched:</b> {item['req_matched']}/{item['req_total']} required skills
            </div>
            <div class="card-desc" style="font-size:0.85rem; color:#475569;">
                <b>Why it matches:</b> {item['why_matches'][0] if item['why_matches'] else 'Overlap'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🔍 View {item['role']} Details & Learning Path"):
            st.markdown("**Skills You Have:**")
            if item["matching_skills"]:
                st.write(", ".join(item["matching_skills"]))
            else:
                st.caption("None yet")

            st.markdown("**Missing Required Skills:**")
            if item["missing_required"]:
                st.write(", ".join(item["missing_required"]))
            else:
                st.success("All required skills met!")

            st.markdown("**Recommended Next Skills to Learn:**")
            if item["next_skills"]:
                for ns in item["next_skills"]:
                    st.markdown(f"- 🚀 **{ns}**")
            else:
                st.caption("Profile fully aligned.")

            if st.button(f"Prepare Interview Questions for {item['role']}", key=f"btn_{idx}"):
                st.session_state["target_role"] = item["role"]
                st.page_link("pages/04_Interview_Preparation.py", label=f"Go to Interview Prep for {item['role']} →")
