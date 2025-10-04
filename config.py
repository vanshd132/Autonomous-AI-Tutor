"""
Configuration management for AI Tutor Orchestrator
"""

import os
from typing import Dict, Any

# Try to load environment variables, but don't fail if dotenv is not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, continue without it
    pass

class Config:
    """Application configuration"""
    
    # API Configuration
    API_TITLE = "AI Tutor Orchestrator"
    API_DESCRIPTION = "Intelligent middleware for autonomous AI tutoring systems"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]  # In production, specify actual origins
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Educational Tools Configuration
    MAX_FLASHCARD_COUNT = 20
    MIN_FLASHCARD_COUNT = 1
    SUPPORTED_NOTE_STYLES = ["outline", "bullet_points", "narrative", "structured"]
    SUPPORTED_DIFFICULTIES = ["easy", "medium", "hard"]
    SUPPORTED_DEPTHS = ["basic", "intermediate", "advanced", "comprehensive"]
    
    # Parameter Extraction Configuration
    MAX_CHAT_HISTORY = 10
    TOPIC_EXTRACTION_KEYWORDS = [
        "math", "calculus", "algebra", "geometry", "statistics",
        "science", "biology", "chemistry", "physics", "environmental",
        "history", "literature", "english", "writing", "reading",
        "programming", "computer science", "coding", "photosynthesis",
        "derivatives", "equations", "world war"
    ]
    
    # Subject Mapping
    SUBJECT_MAPPING = {
        "math": "Mathematics",
        "calculus": "Mathematics", 
        "algebra": "Mathematics",
        "geometry": "Mathematics",
        "statistics": "Mathematics",
        "science": "Science",
        "biology": "Biology",
        "chemistry": "Chemistry",
        "physics": "Physics",
        "environmental": "Environmental Science",
        "history": "History",
        "english": "English",
        "literature": "English",
        "programming": "Computer Science",
        "coding": "Computer Science"
    }
    
    # Tool Selection Keywords
    NOTE_MAKER_KEYWORDS = ["note", "notes", "summary", "outline", "study guide"]
    FLASHCARD_KEYWORDS = ["flashcard", "quiz", "test", "practice", "review", "memorize"]
    EXPLAINER_KEYWORDS = ["explain", "understand", "concept", "how", "what", "why", "confused"]
    
    # Difficulty Inference
    EASY_KEYWORDS = ["struggling", "difficult", "hard", "confused", "beginner"]
    HARD_KEYWORDS = ["advanced", "expert", "challenging", "complex"]
    
    # Depth Inference
    BASIC_KEYWORDS = ["basic", "simple", "beginner", "confused", "fundamental"]
    ADVANCED_KEYWORDS = ["advanced", "comprehensive", "detailed", "expert"]
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get complete configuration as dictionary."""
        return {
            "api": {
                "title": cls.API_TITLE,
                "description": cls.API_DESCRIPTION,
                "version": cls.API_VERSION
            },
            "server": {
                "host": cls.HOST,
                "port": cls.PORT,
                "debug": cls.DEBUG
            },
            "logging": {
                "level": cls.LOG_LEVEL
            },
            "cors": {
                "origins": cls.CORS_ORIGINS,
                "credentials": cls.CORS_CREDENTIALS,
                "methods": cls.CORS_METHODS,
                "headers": cls.CORS_HEADERS
            },
            "tools": {
                "max_flashcard_count": cls.MAX_FLASHCARD_COUNT,
                "min_flashcard_count": cls.MIN_FLASHCARD_COUNT,
                "supported_note_styles": cls.SUPPORTED_NOTE_STYLES,
                "supported_difficulties": cls.SUPPORTED_DIFFICULTIES,
                "supported_depths": cls.SUPPORTED_DEPTHS
            }
        }
