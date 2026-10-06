"""
Tests for ResumeParser, TextCleaner, SectionExtractor, SkillExtractor (Phases 2-4)
"""
import io
import pytest
from utils.validators import validate_file_extension, validate_file_size, validate_resume_text
from modules.document_validator import DocumentValidator
from modules.resume_parser import ResumeParser
from modules.text_cleaner import TextCleaner
from modules.section_extractor import SectionExtractor
from modules.skill_extractor import SkillExtractor


# ── Validator Tests ──────────────────────────────────────────────────

def test_file_extension_validation_valid():
    assert validate_file_extension("resume.pdf")[0] is True
    assert validate_file_extension("cv_sample.docx")[0] is True

def test_file_extension_validation_invalid():
    valid, msg = validate_file_extension("image.png")
    assert valid is False
    assert "Unsupported" in msg

def test_file_extension_empty():
    valid, msg = validate_file_extension("")
    assert valid is False

def test_file_size_within_limit():
    small_bytes = b"x" * 1024  # 1 KB
    assert validate_file_size(small_bytes, max_mb=5)[0] is True

def test_file_size_too_large():
    large_bytes = b"x" * (6 * 1024 * 1024)  # 6 MB
    valid, msg = validate_file_size(large_bytes, max_mb=5)
    assert valid is False
    assert "exceeds" in msg

def test_file_size_empty():
    valid, msg = validate_file_size(b"", max_mb=5)
    assert valid is False
    assert "empty" in msg

def test_resume_text_too_short():
    valid, msg = validate_resume_text("Hello world")
    assert valid is False

def test_resume_text_valid():
    text = (
        "Education: Bachelor of Science in Computer Science. "
        "Experience: Python Developer at Tech Corp for 3 years. "
        "Skills: Python, SQL, Git, Docker, Machine Learning. "
        "Projects: E-commerce platform using Django and PostgreSQL. "
        "Certifications: AWS Certified Developer."
    )
    valid, _ = validate_resume_text(text)
    assert valid is True


# ── TextCleaner Tests ────────────────────────────────────────────────

def test_text_cleaner_bullets():
    raw = "• Python developer\n• SQL expert\n▸ Docker user"
    cleaned = TextCleaner.clean(raw)
    assert "•" not in cleaned
    assert "▸" not in cleaned

def test_text_cleaner_ligatures():
    raw = "\uFB01le\uFB02ow"  # fi + fl
    cleaned = TextCleaner.clean(raw)
    assert "\uFB01" not in cleaned
    assert "\uFB02" not in cleaned
    assert "fi" in cleaned and "fl" in cleaned

def test_text_cleaner_nbsp():
    raw = "Python\u00a0Developer"
    cleaned = TextCleaner.clean(raw)
    assert "\u00a0" not in cleaned
    assert "Python Developer" in cleaned

def test_text_cleaner_multiple_newlines():
    raw = "Line1\n\n\n\n\nLine2"
    cleaned = TextCleaner.clean(raw)
    assert "\n\n\n" not in cleaned

def test_text_cleaner_empty():
    assert TextCleaner.clean("") == ""
    assert TextCleaner.clean("   ") == ""

def test_split_into_lines():
    text = "Line 1\n\nLine 2\nLine 3"
    lines = TextCleaner.split_into_lines(text)
    assert len(lines) == 3
    assert lines[0] == "Line 1"


# ── SectionExtractor Tests ───────────────────────────────────────────

SAMPLE_RESUME = """
John Doe
john.doe@email.com
+1-555-123-4567
linkedin.com/in/johndoe
github.com/johndoe

Professional Summary
Experienced Python developer with 4 years building scalable web services.

Education
Bachelor of Science in Computer Science
State University, 2019-2023

Work Experience
Senior Python Developer — TechCorp (Jan 2023 - Present)
- Developed REST APIs serving 50k daily users using Django and PostgreSQL
- Reduced API response time by 35% through query optimization
- Led a team of 4 engineers on microservices migration

Skills
Python, Django, PostgreSQL, Docker, Git, AWS, SQL, JavaScript, REST API

Projects
E-Commerce Platform (2022)
- Built full-stack web app with Django, React, and PostgreSQL
- Deployed on AWS EC2 with Docker containerization

Certifications
AWS Certified Developer – Associate (2023)
"""

def test_section_extractor_present_sections():
    from modules.text_cleaner import TextCleaner
    cleaned = TextCleaner.clean(SAMPLE_RESUME)
    sections = SectionExtractor.extract_sections(cleaned)
    present = SectionExtractor.detect_present_sections(sections)
    assert "education" in present
    assert "experience" in present
    assert "skills" in present
    assert "projects" in present
    assert "certifications" in present

def test_contact_info_extraction():
    info = SectionExtractor.extract_contact_info(SAMPLE_RESUME)
    assert info["email"] == "john.doe@email.com"
    assert info["phone"] is not None
    assert "johndoe" in info["linkedin"]
    assert "johndoe" in info["github"]

def test_name_detection():
    info = SectionExtractor.extract_contact_info(SAMPLE_RESUME)
    assert info["name"] == "John Doe"


# ── SkillExtractor Tests ─────────────────────────────────────────────

def test_skill_extraction_basic():
    text = "I work with Python, Django, PostgreSQL, Docker, and AWS."
    skills = SkillExtractor.extract_skills(text)
    flat = SkillExtractor.get_all_skills_flat(skills)
    assert "Python" in flat
    assert "Django" in flat
    assert "PostgreSQL" in flat

def test_skill_alias_normalization():
    text = "Experienced in ML and JS frameworks."
    skills = SkillExtractor.extract_skills(text)
    flat = SkillExtractor.get_all_skills_flat(skills)
    assert "Machine Learning" in flat
    assert "JavaScript" in flat

def test_skill_extraction_empty():
    skills = SkillExtractor.extract_skills("")
    flat = SkillExtractor.get_all_skills_flat(skills)
    assert flat == []

def test_skill_gap_analysis():
    resume_skills = ["Python", "Django", "Git"]
    required_skills = ["Python", "SQL", "Django", "REST API", "Docker"]
    gap = SkillExtractor.identify_missing_skills(resume_skills, required_skills)
    assert "Python" in gap["matching"]
    assert "Django" in gap["matching"]
    assert "SQL" in gap["missing"]
    assert "Docker" in gap["missing"]
    assert "REST API" in gap["missing"]

def test_skill_extraction_from_sections():
    sections = {
        "skills": "Python, Machine Learning, TensorFlow, SQL, Git",
        "experience": "Developed Django REST APIs. Worked with Docker and AWS.",
        "projects": "Built deep learning models using PyTorch.",
    }
    skills = SkillExtractor.extract_skills_from_sections(sections)
    flat = SkillExtractor.get_all_skills_flat(skills)
    assert "Python" in flat
    assert "TensorFlow" in flat
    assert "Django" in flat

def test_skill_category():
    assert SkillExtractor.get_skill_category("Python") == "Programming"
    assert SkillExtractor.get_skill_category("React") == "Web"
    assert SkillExtractor.get_skill_category("TensorFlow") == "AI/ML"
