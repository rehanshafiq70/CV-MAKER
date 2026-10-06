"""
CareerAI - Resume Analyzer Page
Upload → Validate → Parse → Clean → Section Extract → Skill Extract → ATS Score → PDF Report & AI Tools
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.helpers import get_app_css, is_ai_configured, get_score_badge_class, get_env_var
from utils.constants import APP_NAME, SECTION_LABELS
from modules.document_validator import DocumentValidator
from modules.resume_parser import ResumeParser
from modules.text_cleaner import TextCleaner
from modules.section_extractor import SectionExtractor
from modules.skill_extractor import SkillExtractor
from modules.ats_engine import ATSEngine
from modules.ai_engine import AIEngine
from modules.report_generator import ReportGenerator

# ── Page Config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"Resume Analyzer | {APP_NAME}",
    page_icon="📄",
    layout="wide",
)
st.markdown(get_app_css(), unsafe_allow_html=True)

MAX_MB = int(get_env_var("MAX_UPLOAD_SIZE_MB", "5"))
ai_engine = AIEngine()

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
  <h1 style="font-size:2rem; font-weight:800; margin-bottom:0.25rem;">📄 Resume Analyzer</h1>
  <p style="color:#64748B; margin:0;">
    Upload your resume → Extract sections → Calculate your
    <strong>CareerAI ATS Compatibility Score</strong>
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Two-column layout ─────────────────────────────────────────────────
upload_col, result_col = st.columns([1, 1.6], gap="large")

with upload_col:
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        f"PDF or DOCX  ·  Max {MAX_MB} MB",
        type=["pdf", "docx"],
        help="Files are processed in-session only. Not retained on disk by default.",
        label_visibility="visible",
    )

    if uploaded_file:
        st.success(f"**{uploaded_file.name}**  ·  {uploaded_file.size / 1024:.1f} KB")
        analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown("**What will be analyzed:**")
        st.markdown("""
- ✅ Document structure & sections
- 🏷️ Technical skill extraction
- 🎯 ATS compatibility score (0–100)
- ⚡ Strengths & improvement areas
- 📄 Professional PDF report export
        """)
    else:
        st.info("👆 Upload a PDF or DOCX resume to begin analysis.")
        analyze_btn = False

    # Show active session info if previously parsed
    if "parsed_resume" in st.session_state and not analyze_btn:
        st.markdown("---")
        st.success("✅ **Active Resume Loaded in Session**")
        st.caption("You can navigate to Job Matcher or Career Recommendations using the sidebar.")

# ── Analysis Logic ────────────────────────────────────────────────────
if uploaded_file and analyze_btn:
    file_bytes = uploaded_file.read()
    filename   = uploaded_file.name

    with result_col:
        with st.spinner("🔍 Analyzing your resume..."):
            # Step 1: Validate
            valid, msg = DocumentValidator.validate_upload(filename, file_bytes, MAX_MB)
            if not valid:
                st.error(f"❌ Upload validation failed: {msg}")
                st.stop()

            # Step 2: Parse
            success, raw_text, error, parse_meta = ResumeParser.parse(filename, file_bytes)
            if not success:
                st.error(f"❌ Could not extract text: {error}")
                st.stop()

            # Step 3: Clean
            cleaned_text = TextCleaner.clean(raw_text)

            # Step 4: Sections & Contact
            sections = SectionExtractor.extract_sections(cleaned_text)
            contact_info = SectionExtractor.extract_contact_info(cleaned_text)
            present_sections = SectionExtractor.detect_present_sections(sections)

            # Step 5: Skills
            skills = SkillExtractor.extract_skills_from_sections(sections)
            all_skills_flat = SkillExtractor.get_all_skills_flat(skills)

            # Step 6: ATS Evaluation
            engine = ATSEngine()
            ats_result = engine.evaluate(sections, skills, cleaned_text)

            # Save in session state for cross-page persistence
            st.session_state["parsed_resume"] = {
                "filename": filename,
                "raw_text": raw_text,
                "cleaned_text": cleaned_text,
                "sections": sections,
                "contact_info": contact_info,
                "present_sections": present_sections,
                "skills": skills,
                "skills_flat": all_skills_flat,
                "ats_result": ats_result,
                "parse_meta": parse_meta,
            }

# Render results if available in session_state
if "parsed_resume" in st.session_state:
    p_data = st.session_state["parsed_resume"]
    ats_result = p_data["ats_result"]
    sections = p_data["sections"]
    skills = p_data["skills"]
    all_skills_flat = p_data["skills_flat"]
    present_sections = p_data["present_sections"]
    contact_info = p_data["contact_info"]
    parse_meta = p_data["parse_meta"]

    with result_col:
        overall = ats_result["overall_score"]
        badge_color = get_score_badge_class(overall)
        label = ats_result["label"]

        # ── Overall ATS Score Hero ───────────────────────────────────
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A, #1E3A5F);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.08);
        ">
            <div style="color:#94A3B8; font-size:0.85rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">
                CareerAI ATS Compatibility Score
            </div>
            <div style="font-size:4.5rem; font-weight:900; color:{badge_color}; line-height:1.1; margin: 0.5rem 0;">
                {overall:.0f}
            </div>
            <div style="color:#CBD5E1; font-size:1rem; font-weight:600;">/100 — {label}</div>
            <div style="margin-top:1rem;">
                <div style="
                    background: rgba(255,255,255,0.1);
                    border-radius: 999px;
                    height: 10px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {overall}%;
                        background: {badge_color};
                        height: 100%;
                        border-radius: 999px;
                        transition: width 0.5s ease;
                    "></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Action Buttons (PDF Export & Navigation) ────────────────
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            pdf_bytes = ReportGenerator.generate_pdf_report(
                ats_result=ats_result,
                sections=sections,
                skills=skills,
                contact_info=contact_info
            )
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name="CareerAI_Resume_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

        with col_btn2:
            st.page_link("pages/02_Job_Matcher.py", label="🎯 Match with Job Posting →", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Quick Stats Row ──────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Sections Found", len(present_sections))
        m2.metric("Skills Detected", len(all_skills_flat))
        m3.metric("Strengths", len(ats_result["strengths"]))
        m4.metric("Improvement Areas", len(ats_result["weaknesses"]))

        st.divider()

        # ── Tabs for detail views ────────────────────────────────────
        tab_score, tab_skills, tab_sections, tab_swot, tab_ai = st.tabs([
            "📊 Score Breakdown",
            "🏷️ Skills",
            "📋 Sections",
            "⚡ Strengths & Weaknesses",
            "🤖 AI Resume Tools",
        ])

        # ── TAB 1: Score Breakdown ───────────────────────────────────
        with tab_score:
            breakdown = ats_result["breakdown"]
            components = [comp.get("label", key) for key, comp in breakdown.items()]
            scored = [comp.get("weighted", 0) for key, comp in breakdown.items()]
            budgets = [comp.get("weight_budget", 0) for key, comp in breakdown.items()]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Your Score",
                x=components, y=scored,
                marker_color=badge_color,
                text=[f"{s:.1f}" for s in scored],
                textposition="outside",
            ))
            fig.add_trace(go.Bar(
                name="Maximum",
                x=components, y=budgets,
                marker_color="rgba(148,163,184,0.25)",
                text=[f"{b}" for b in budgets],
                textposition="outside",
            ))
            fig.update_layout(
                barmode="overlay", height=360,
                margin=dict(l=10, r=10, t=30, b=60),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_tickangle=-25,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

            rows = []
            for key, comp in breakdown.items():
                pct = comp.get("score", 0) / comp.get("max", 1) * 100 if comp.get("max", 1) else 0
                rows.append({
                    "Component": comp.get("label", key),
                    "Score": f"{comp.get('weighted', 0):.1f} / {comp.get('weight_budget', 0)}",
                    "Rating (%)": f"{pct:.0f}%",
                    "Status": "✅ Good" if pct >= 70 else ("⚠️ Average" if pct >= 40 else "❌ Needs Work"),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ── TAB 2: Skills ────────────────────────────────────────────
        with tab_skills:
            if all_skills_flat:
                st.success(f"**{len(all_skills_flat)} skills** detected across categories")
                for category, skill_list in skills.items():
                    if skill_list:
                        st.markdown(f"**{category}**")
                        pills = " ".join(
                            f'<span style="display:inline-block; background:#EFF6FF; color:#1D4ED8; '
                            f'border:1px solid #BFDBFE; border-radius:6px; padding:0.2rem 0.6rem; '
                            f'font-size:0.82rem; font-weight:600; margin:0.2rem;">{s}</span>'
                            for s in skill_list
                        )
                        st.markdown(pills, unsafe_allow_html=True)
                        st.markdown("")
            else:
                st.warning("No skills detected. Add a Skills section with clear technology names.")

        # ── TAB 3: Sections ──────────────────────────────────────────
        with tab_sections:
            all_section_keys = list(SECTION_LABELS.keys())
            found_set = set(present_sections)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### ✅ Detected Sections")
                for sec in all_section_keys:
                    if sec in found_set:
                        st.markdown(f"✅ **{SECTION_LABELS.get(sec, sec)}**")
            with col_b:
                st.markdown("#### ⚠️ Missing Sections")
                missing_secs = [sec for sec in all_section_keys if sec not in found_set]
                if missing_secs:
                    for sec in missing_secs:
                        st.markdown(f"⚠️ {SECTION_LABELS.get(sec, sec)}")
                else:
                    st.success("All standard sections detected!")

        # ── TAB 4: Strengths & Weaknesses ────────────────────────────
        with tab_swot:
            s_col, w_col = st.columns(2)
            with s_col:
                st.markdown("### 💪 Strengths")
                for s in ats_result.get("strengths", []):
                    st.markdown(f"- {s}")
            with w_col:
                st.markdown("### 🔧 Areas to Improve")
                for w in ats_result.get("weaknesses", []):
                    st.markdown(f"- {w}")

        # ── TAB 5: AI Resume Tools ────────────────────────────────────
        with tab_ai:
            st.markdown("### 🤖 Improve My Resume")
            st.caption("Enhance wording using action verbs strictly without inventing facts.")

            st.markdown("#### 1. Improve Bullet Point Wording")
            sample_bullet = st.text_input("Paste a bullet point to improve:", value="Worked on machine learning project using python.")
            if st.button("Enhance Bullet Point"):
                res = ai_engine.improve_bullet_point(sample_bullet)
                st.markdown(f"**Original:** {res['original']}")
                st.markdown(f"**Improved:** {res['improved']}")
                st.caption(f"Mode: `{res['mode']}`")

            st.markdown("---")
            st.markdown("#### 2. AI Professional Summary Generator")
            if st.button("Generate Professional Summary"):
                res_sum = ai_engine.generate_professional_summary(
                    name=contact_info.get("name"),
                    skills=all_skills_flat,
                    experience_text=sections.get("experience", ""),
                    education_text=sections.get("education", "")
                )
                st.text_area("Generated Summary (Truthful)", value=res_sum["summary"], height=120)
                st.caption("Copy this summary directly into your resume.")

elif not uploaded_file and "parsed_resume" not in st.session_state:
    with result_col:
        st.markdown("""
        <div style="border: 2px dashed #CBD5E1; border-radius: 16px; padding: 3rem 2rem; text-align: center; color: #94A3B8;">
            <div style="font-size:3rem; margin-bottom:1rem;">📄</div>
            <div style="font-size:1.1rem; font-weight:600; margin-bottom:0.5rem;">Analysis Results Will Appear Here</div>
            <div style="font-size:0.9rem;">Upload your PDF or DOCX resume to see your ATS score and diagnostic feedback.</div>
        </div>
        """, unsafe_allow_html=True)
