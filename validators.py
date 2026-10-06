"""
CareerAI - Input & Document Validation Utilities
"""
import os
from typing import Tuple, Optional
from utils.constants import SUPPORTED_EXTENSIONS, DEFAULT_MAX_UPLOAD_SIZE_MB

def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """Validates if the uploaded file has a supported extension."""
    if not filename:
        return False, "No file provided."
    _, ext = os.path.splitext(filename.lower())
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file extension '{ext}'. Only PDF and DOCX files are supported."
    return True, ""

def validate_file_size(file_bytes: bytes, max_mb: int = DEFAULT_MAX_UPLOAD_SIZE_MB) -> Tuple[bool, str]:
    """Validates file size against configured ceiling."""
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_mb:
        return False, f"File size ({size_mb:.2f} MB) exceeds maximum permitted size of {max_mb} MB."
    if len(file_bytes) == 0:
        return False, "File is empty (0 bytes)."
    return True, ""

def validate_resume_text(text: str, min_words: int = 30) -> Tuple[bool, str]:
    """
    Validates whether extracted text is sufficient and contains resume-like characteristics.
    Detects scanned/image-only PDFs where text is empty or negligible.
    """
    if not text or not text.strip():
        return False, "No extractable text found. If this is a PDF, it may be a scanned image or corrupted."
    
    words = text.strip().split()
    if len(words) < min_words:
        return False, f"Document text is unusually brief ({len(words)} words). A typical resume contains at least {min_words} words."
        
    # Check for basic resume indicator terms
    resume_indicators = [
        "experience", "education", "skills", "projects", "objective", 
        "summary", "work", "university", "college", "employment", 
        "contact", "phone", "email", "certifications", "technologies"
    ]
    lower_text = text.lower()
    matches = [ind for ind in resume_indicators if ind in lower_text]
    
    if len(matches) < 2:
        return False, "Document does not appear to contain standard resume sections or terminology."
        
    return True, ""
