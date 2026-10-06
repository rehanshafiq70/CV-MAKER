"""
CareerAI - Benchmark & Evaluation Script
Evaluates job matching accuracy and skill gap precision across sample profiles.
"""
import sys
from pathlib import Path
_root_dir = Path(__file__).resolve().parent.parent
if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))

from modules.job_matcher import JobMatcher
from modules.skill_extractor import SkillExtractor

def run_matching_benchmark():
    """Runs a benchmark test comparing sample resumes against sample job postings."""
    print("==================================================")
    print("CareerAI - Job Matching Benchmark")
    print("==================================================")

    sample_resume = {
        "raw_text": "Experienced Python Developer with 3 years building web apps with Django, PostgreSQL, Docker, Git, REST API.",
        "sections": {
            "experience": "Python Developer at TechCorp. Built Django REST APIs, PostgreSQL DB, Docker containers.",
            "education": "Bachelor of Science in Computer Science",
            "skills": "Python, Django, PostgreSQL, Docker, Git, REST API, SQL"
        },
        "skills_flat": ["Python", "Django", "PostgreSQL", "Docker", "Git", "REST API", "SQL"]
    }

    matcher = JobMatcher()

    job_posting = """
    Job Title: Senior Python Engineer
    Experience: 3+ years
    Requirements: Python, Django, PostgreSQL, Docker, AWS, Kubernetes, Redis
    """

    job_data = matcher.parse_job_description(job_posting)
    result = matcher.match(sample_resume, job_data)

    print(f"Match Score: {result['match_score']:.1f}% ({result['match_label']})")
    print("Matching Skills:", result['matching_skills'])
    print("Missing Skills:", result['missing_skills'])
    print("High Priority Missing:", result['priority']['High'])
    print("==================================================")

if __name__ == "__main__":
    run_matching_benchmark()
