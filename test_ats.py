"""
Tests for ATSEngine (Phase 5) — verifying scoring logic and component integrity
"""
import pytest
from modules.ats_engine import ATSEngine
from modules.skill_extractor import SkillExtractor
from utils.constants import DEFAULT_ATS_WEIGHTS


SAMPLE_SECTIONS = {
    "contact": "john.doe@email.com  +1-555-123-4567  linkedin.com/in/johndoe",
    "summary": (
        "Experienced Python developer with 4 years building scalable web applications. "
        "Developed and deployed microservices on AWS, reducing latency by 35%. "
        "Passionate about clean code and performance optimization."
    ),
    "education": (
        "Bachelor of Science in Computer Science\n"
        "State University, 2019–2023, GPA 3.8"
    ),
    "experience": (
        "Senior Python Developer – TechCorp (Jan 2023 – Present)\n"
        "- Developed REST APIs serving 50,000 daily users with Django and PostgreSQL\n"
        "- Reduced response time by 35% through query optimization\n"
        "- Led team of 4 engineers on microservices migration\n"
        "- Deployed containerized services on AWS using Docker and Kubernetes\n"
        "Junior Developer – StartupXYZ (Jun 2021 – Dec 2022)\n"
        "- Built e-commerce platform achieving $120k monthly revenue\n"
        "- Implemented CI/CD pipelines with GitHub Actions, reducing deployment time by 60%"
    ),
    "skills": (
        "Python, Django, FastAPI, PostgreSQL, MySQL, Docker, Kubernetes, "
        "AWS, Git, JavaScript, React, SQL, Linux, CI/CD, REST API"
    ),
    "projects": (
        "E-Commerce Platform (2022)\n"
        "- Built with Django, React, PostgreSQL; served 10k+ users\n"
        "- Deployed on AWS EC2 with Docker containerization\n\n"
        "ML Sentiment Analyzer (2021)\n"
        "- Python, TensorFlow, NLP pipeline; 88% accuracy on test set"
    ),
    "certifications": (
        "AWS Certified Developer – Associate (2023)\n"
        "Docker Certified Associate (2022)"
    ),
    "achievements": "",
    "publications": "",
    "languages": "",
    "interests": "",
    "objective": "",
}

SAMPLE_SKILLS = {
    "Programming":    ["Python", "JavaScript"],
    "Web":            ["Django", "FastAPI", "React", "REST API"],
    "Data":           ["SQL"],
    "AI/ML":          [],
    "Cloud/DevOps":   ["AWS", "Docker", "Kubernetes", "Git", "CI/CD", "Linux"],
    "Databases":      ["PostgreSQL", "MySQL"],
    "Bioinformatics": [],
    "Soft Skills":    [],
}

SAMPLE_TEXT = " ".join(SAMPLE_SECTIONS.values())


# ── Weight integrity ─────────────────────────────────────────────────

def test_ats_weights_sum_to_100():
    assert abs(sum(DEFAULT_ATS_WEIGHTS.values()) - 100) < 0.01

def test_ats_engine_initialization_with_defaults():
    engine = ATSEngine()
    assert engine.weights == DEFAULT_ATS_WEIGHTS

def test_ats_custom_weights():
    custom = {k: v for k, v in DEFAULT_ATS_WEIGHTS.items()}
    engine = ATSEngine(weights=custom)
    assert engine.weights == custom


# ── Result structure ─────────────────────────────────────────────────

def test_ats_result_keys():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    assert "overall_score" in result
    assert "label" in result
    assert "breakdown" in result
    assert "strengths" in result
    assert "weaknesses" in result

def test_ats_score_within_bounds():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    score = result["overall_score"]
    assert 0 <= score <= 100

def test_ats_breakdown_has_all_components():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    expected_keys = set(DEFAULT_ATS_WEIGHTS.keys())
    assert expected_keys == set(result["breakdown"].keys())

def test_ats_breakdown_weighted_scores():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    for key, comp in result["breakdown"].items():
        assert "weighted" in comp
        assert 0 <= comp["weighted"] <= comp["weight_budget"] + 0.01


# ── Scoring logic ────────────────────────────────────────────────────

def test_good_resume_scores_above_60():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    assert result["overall_score"] >= 60, (
        f"Expected ≥60 for well-formatted resume, got {result['overall_score']}"
    )

def test_empty_resume_scores_low():
    empty_sections = {k: "" for k in SAMPLE_SECTIONS}
    empty_skills = {k: [] for k in SAMPLE_SKILLS}
    engine = ATSEngine()
    result = engine.evaluate(empty_sections, empty_skills, "")
    assert result["overall_score"] < 20

def test_ats_label_is_string():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    assert isinstance(result["label"], str)
    assert result["label"] in ["Excellent", "Good", "Average", "Below Average", "Needs Improvement"]

def test_strengths_list():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    assert isinstance(result["strengths"], list)

def test_weaknesses_list():
    engine = ATSEngine()
    result = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    assert isinstance(result["weaknesses"], list)

def test_missing_experience_reduces_score():
    no_exp = dict(SAMPLE_SECTIONS)
    no_exp["experience"] = ""
    engine = ATSEngine()
    result_full = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    result_no_exp = engine.evaluate(no_exp, SAMPLE_SKILLS, "")
    assert result_full["overall_score"] > result_no_exp["overall_score"]

def test_missing_skills_reduces_score():
    no_skills = {k: [] for k in SAMPLE_SKILLS}
    engine = ATSEngine()
    result_full = engine.evaluate(SAMPLE_SECTIONS, SAMPLE_SKILLS, SAMPLE_TEXT)
    result_no_skills = engine.evaluate(SAMPLE_SECTIONS, no_skills, SAMPLE_TEXT)
    assert result_full["overall_score"] > result_no_skills["overall_score"]
