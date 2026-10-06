"""
Tests for Job Matching, Career Recommendations, Interview Engine & AI Engine
"""
import pytest
from modules.job_matcher import JobMatcher
from modules.career_engine import CareerEngine
from modules.interview_engine import InterviewEngine
from modules.ai_engine import AIEngine
from modules.report_generator import ReportGenerator
from utils.constants import DEFAULT_JOB_MATCH_WEIGHTS

def test_job_match_weights_sum_to_100():
    total_weight = sum(DEFAULT_JOB_MATCH_WEIGHTS.values())
    assert abs(total_weight - 100) < 0.01

def test_job_matcher_execution():
    matcher = JobMatcher()
    sample_resume = {
        "raw_text": "Python Developer with SQL, Git, and REST API experience.",
        "sections": {"skills": "Python, SQL, Git, REST API"},
        "skills_flat": ["Python", "SQL", "Git", "REST API"]
    }
    sample_job = matcher.parse_job_description("""
        Job Title: Python Engineer
        Requirements: Python, SQL, Django, REST API, Docker
    """)

    result = matcher.match(sample_resume, sample_job)

    assert "match_score" in result
    assert "matching_skills" in result
    assert "missing_skills" in result
    assert "Python" in result["matching_skills"]
    assert "Django" in result["missing_skills"]

def test_career_engine_recommendations():
    skills = ["Python", "Pandas", "NumPy", "SQL", "Data Analysis"]
    recs = CareerEngine.recommend_roles(skills)

    assert len(recs) > 0
    top_role = recs[0]
    assert "role" in top_role
    assert "match_pct" in top_role
    assert top_role["match_pct"] > 0

def test_interview_engine_questions():
    questions = InterviewEngine.get_questions_for_role("Python Developer", count=10)
    assert len(questions) == 10
    assert "q" in questions[0]
    assert "hint" in questions[0]

def test_ai_engine_local_bullet_improvement():
    ai = AIEngine()
    result = ai.improve_bullet_point("worked on machine learning project")
    assert result["success"] is True
    assert "Developed" in result["improved"]

def test_pdf_report_generation():
    ats_result = {
        "overall_score": 85.0,
        "label": "Excellent",
        "breakdown": {
            "skills": {"label": "Skills", "weighted": 18, "weight_budget": 20, "score": 18, "max": 20}
        },
        "strengths": ["Strong skills"],
        "weaknesses": []
    }
    skills = {"Programming": ["Python", "SQL"]}
    contact_info = {"name": "Test User"}

    pdf_bytes = ReportGenerator.generate_pdf_report(ats_result, {}, skills, contact_info)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
