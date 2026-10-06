"""
CareerAI - General Utility Helpers
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables on import
load_dotenv()

def get_env_var(key: str, default: Any = None) -> Any:
    """Safely retrieves an environment variable with a default fallback."""
    return os.environ.get(key, default)

def is_ai_configured() -> bool:
    """Checks whether an external AI API key is configured."""
    key = os.environ.get("AI_API_KEY", "").strip()
    return bool(key)

def get_score_badge_class(score: float) -> str:
    """Returns CSS class/color based on ATS or Job Match score."""
    if score >= 80:
        return "#10B981"  # Emerald green
    elif score >= 60:
        return "#3B82F6"  # Blue
    elif score >= 40:
        return "#F59E0B"  # Amber
    else:
        return "#EF4444"  # Red

def format_percentage(value: float) -> str:
    """Formats float value as rounded percentage string."""
    return f"{round(value, 1)}%"

def get_app_css() -> str:
    """Returns custom CSS for a polished, clean SaaS look in Streamlit."""
    return """
    <style>
    /* Global font and modern styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    /* Modern Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        color: #F8FAFC;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        line-height: 1.2;
        margin-bottom: 0.75rem;
        background: linear-gradient(90deg, #FFFFFF, #93C5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 400;
        color: #94A3B8;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }

    /* SaaS Metric Cards */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }

    /* Dark mode support for feature cards */
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background: #1E293B;
            border-color: #334155;
            color: #F8FAFC;
        }
        .feature-card:hover {
            border-color: #475569;
        }
    }

    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.75rem;
        display: inline-block;
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: inherit;
    }

    .card-desc {
        font-size: 0.9rem;
        color: #64748B;
        line-height: 1.5;
    }

    /* Privacy & Security banner */
    .privacy-notice {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #065F46;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-top: 2rem;
    }

    @media (prefers-color-scheme: dark) {
        .privacy-notice {
            color: #A7F3D0;
            background: rgba(16, 185, 129, 0.12);
        }
    }

    /* Workflow pipeline step pill */
    .step-pill {
        display: inline-flex;
        align-items: center;
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
        margin: 0.25rem;
    }
    @media (prefers-color-scheme: dark) {
        .step-pill {
            background: #0F172A;
            border-color: #334155;
            color: #CBD5E1;
        }
    }
    </style>
    """
