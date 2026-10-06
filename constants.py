"""
CareerAI - Core Constants and Configuration Definitions
"""

APP_NAME = "CareerAI"
TAGLINE = "Analyze Your Resume. Match Your Skills. Build Your Career."
VERSION = "1.0.0"

SUPPORTED_EXTENSIONS = [".pdf", ".docx"]
DEFAULT_MAX_UPLOAD_SIZE_MB = 5

# Supported Resume Sections
RESUME_SECTIONS = [
    "contact",
    "summary",
    "objective",
    "education",
    "experience",
    "skills",
    "projects",
    "certifications",
    "achievements",
    "publications",
    "languages",
    "interests",
]

# Section Display Labels
SECTION_LABELS = {
    "contact": "Contact Information",
    "summary": "Professional Summary",
    "objective": "Career Objective",
    "education": "Education",
    "experience": "Work Experience",
    "skills": "Technical & Soft Skills",
    "projects": "Projects & Portfolios",
    "certifications": "Certifications & Licenses",
    "achievements": "Key Achievements & Awards",
    "publications": "Publications & Research",
    "languages": "Languages",
    "interests": "Interests & Activities",
}

# Explainable ATS Score Weights (Must sum to 100)
DEFAULT_ATS_WEIGHTS = {
    "contact": 5,
    "summary": 10,
    "education": 10,
    "experience": 20,
    "skills": 20,
    "projects": 15,
    "certifications": 5,
    "keywords": 10,
    "formatting": 5,
}

# Explainable Job Match Weights (Must sum to 100)
DEFAULT_JOB_MATCH_WEIGHTS = {
    "skills": 40,
    "semantic": 25,
    "experience": 15,
    "education": 10,
    "keywords": 10,
}

# Skill Categorization Dictionary
SKILL_DICTIONARY = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "PHP", 
        "Ruby", "Go", "Rust", "Swift", "Kotlin", "R", "Scala", "MATLAB", "Perl"
    ],
    "Web": [
        "HTML", "CSS", "React", "Next.js", "Node.js", "Express", "Django", "Flask",
        "FastAPI", "Vue.js", "Angular", "Tailwind CSS", "Bootstrap", "REST API",
        "GraphQL", "WebSockets", "ASP.NET", "Spring Boot"
    ],
    "Data": [
        "SQL", "Excel", "Pandas", "NumPy", "Power BI", "Tableau", "Apache Spark",
        "Hadoop", "Airflow", "Kafka", "Data Analysis", "Data Mining", "ETL",
        "Matplotlib", "Seaborn", "Plotly", "BigQuery", "Snowflake"
    ],
    "AI/ML": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
        "NLP", "Natural Language Processing", "Computer Vision", "OpenCV",
        "Scikit-Learn", "Hugging Face", "LLMs", "Generative AI", "LangChain",
        "BERT", "Transformers", "Reinforcement Learning"
    ],
    "Cloud/DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Git",
        "GitHub", "GitLab", "CI/CD", "Terraform", "Linux", "Bash", "Jenkins",
        "Ansible", "Nginx", "Prometheus", "Grafana"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Elasticsearch",
        "Cassandra", "DynamoDB", "Oracle", "Firebase", "Neo4j"
    ],
    "Bioinformatics": [
        "BLAST", "Biopython", "NCBI", "Genomics", "Proteomics", "Bioinformatics",
        "RNA-Seq", "Next-Generation Sequencing", "Molecular Dynamics", "PyMOL",
        "Bioconductor", "Phylogenetics", "FASTA", "Sequence Alignment"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Problem Solving", "Teamwork", "Collaboration",
        "Critical Thinking", "Agile", "Scrum", "Time Management", "Adaptability"
    ]
}

# Common Skill Aliases for Normalization
SKILL_ALIASES = {
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "tf": "TensorFlow",
    "sk-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "k8s": "Kubernetes",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "ms excel": "Excel",
    "bi": "Power BI",
    "powerbi": "Power BI",
    "gcp": "Google Cloud",
    "amazon web services": "AWS",
    "restful api": "REST API",
    "rest apis": "REST API",
}

# Role Definitions for Career Recommendation Engine
CAREER_ROLES = {
    "Python Developer": {
        "required_skills": ["Python", "Git", "REST API", "SQL"],
        "preferred_skills": ["Django", "Flask", "FastAPI", "Docker", "PostgreSQL"],
        "category": "Software Engineering"
    },
    "Data Analyst": {
        "required_skills": ["SQL", "Excel", "Data Analysis", "Python"],
        "preferred_skills": ["Power BI", "Tableau", "Pandas", "NumPy", "Plotly"],
        "category": "Data & Analytics"
    },
    "Data Scientist": {
        "required_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL", "Scikit-Learn"],
        "preferred_skills": ["Deep Learning", "Statistics", "R", "Tableau", "PyTorch"],
        "category": "Data & Analytics"
    },
    "Machine Learning Engineer": {
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
        "preferred_skills": ["Docker", "Kubernetes", "MLOps", "Git", "AWS"],
        "category": "Artificial Intelligence"
    },
    "AI Engineer": {
        "required_skills": ["Python", "Deep Learning", "NLP", "LLMs", "PyTorch"],
        "preferred_skills": ["LangChain", "Hugging Face", "Generative AI", "FastAPI", "Docker"],
        "category": "Artificial Intelligence"
    },
    "Web Developer": {
        "required_skills": ["HTML", "CSS", "JavaScript", "Git"],
        "preferred_skills": ["React", "Node.js", "Responsive Design", "REST API"],
        "category": "Web Development"
    },
    "Full Stack Developer": {
        "required_skills": ["JavaScript", "HTML", "CSS", "Python", "SQL", "Git"],
        "preferred_skills": ["React", "Node.js", "Django", "Docker", "MongoDB", "REST API"],
        "category": "Software Engineering"
    },
    "Software Engineer": {
        "required_skills": ["Python", "Java", "Git", "SQL", "Problem Solving"],
        "preferred_skills": ["C++", "Docker", "Linux", "CI/CD", "Data Structures"],
        "category": "Software Engineering"
    },
    "QA Engineer": {
        "required_skills": ["Python", "Git", "Testing", "Problem Solving"],
        "preferred_skills": ["Selenium", "Automation", "CI/CD", "Agile", "Jira"],
        "category": "Quality Assurance"
    },
    "DevOps Engineer": {
        "required_skills": ["Linux", "Git", "Docker", "CI/CD", "Bash"],
        "preferred_skills": ["Kubernetes", "AWS", "Terraform", "Jenkins", "Ansible"],
        "category": "DevOps & Cloud"
    },
    "Business Analyst": {
        "required_skills": ["Excel", "SQL", "Data Analysis", "Communication", "Problem Solving"],
        "preferred_skills": ["Power BI", "Tableau", "Agile", "Documentation"],
        "category": "Business & Analytics"
    },
    "Bioinformatics Analyst": {
        "required_skills": ["Python", "Bioinformatics", "BLAST", "Genomics", "R"],
        "preferred_skills": ["Biopython", "NCBI", "RNA-Seq", "Linux", "Data Analysis"],
        "category": "Bioinformatics & Life Sciences"
    }
}
