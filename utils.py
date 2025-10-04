"""
Utility functions for AI Tutor Orchestrator
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def validate_parameters(parameters: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    Validate that all required parameters are present.
    
    Args:
        parameters: Dictionary of parameters to validate
        required_fields: List of required field names
        
    Returns:
        True if all required fields are present, False otherwise
    """
    missing_fields = [field for field in required_fields if field not in parameters]
    
    if missing_fields:
        logger.warning(f"Missing required fields: {missing_fields}")
        return False
    
    return True

def format_error_response(error_message: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
    """
    Format a standardized error response.
    
    Args:
        error_message: Human-readable error message
        error_code: Machine-readable error code
        
    Returns:
        Formatted error response dictionary
    """
    return {
        "error": error_message,
        "error_code": error_code,
        "timestamp": datetime.now().isoformat()
    }

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent issues.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    # Remove potentially harmful characters
    text = text.strip()
    
    return text

def extract_keywords(text: str, keyword_list: List[str]) -> List[str]:
    """
    Extract keywords from text based on a predefined list.
    
    Args:
        text: Text to analyze
        keyword_list: List of keywords to look for
        
    Returns:
        List of found keywords
    """
    text_lower = text.lower()
    found_keywords = [keyword for keyword in keyword_list if keyword in text_lower]
    
    return found_keywords

def calculate_difficulty_score(mastery_level: str, emotional_state: str, message_context: str) -> str:
    """
    Calculate appropriate difficulty level based on multiple factors.
    
    Args:
        mastery_level: Student's mastery level description
        emotional_state: Student's current emotional state
        message_context: Current message content
        
    Returns:
        Difficulty level: "easy", "medium", or "hard"
    """
    # Extract mastery level number if present
    mastery_score = 5  # Default medium
    if "level" in mastery_level.lower():
        try:
            level_num = int(mastery_level.lower().split("level")[1].split()[0])
            mastery_score = level_num
        except (IndexError, ValueError):
            pass
    
    # Emotional state adjustment
    emotional_adjustment = 0
    if any(word in emotional_state.lower() for word in ["confused", "struggling", "anxious"]):
        emotional_adjustment = -2
    elif any(word in emotional_state.lower() for word in ["focused", "motivated", "confident"]):
        emotional_adjustment = 1
    
    # Message context adjustment
    context_adjustment = 0
    if any(word in message_context.lower() for word in ["struggling", "difficult", "hard", "confused"]):
        context_adjustment = -2
    elif any(word in message_context.lower() for word in ["advanced", "expert", "challenging"]):
        context_adjustment = 2
    
    # Calculate final score
    final_score = mastery_score + emotional_adjustment + context_adjustment
    
    if final_score <= 3:
        return "easy"
    elif final_score >= 7:
        return "hard"
    else:
        return "medium"

def format_tool_response(tool_name: str, response_data: Dict[str, Any], success: bool = True) -> Dict[str, Any]:
    """
    Format a standardized tool response.
    
    Args:
        tool_name: Name of the tool that generated the response
        response_data: Tool-specific response data
        success: Whether the operation was successful
        
    Returns:
        Formatted response dictionary
    """
    return {
        "success": success,
        "tool_name": tool_name,
        "response_data": response_data,
        "timestamp": datetime.now().isoformat()
    }

def log_operation(operation: str, user_id: str, details: Dict[str, Any] = None) -> None:
    """
    Log an operation for debugging and monitoring.
    
    Args:
        operation: Name of the operation being performed
        user_id: ID of the user performing the operation
        details: Additional details to log
    """
    log_data = {
        "operation": operation,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    }
    
    if details:
        log_data.update(details)
    
    logger.info(f"Operation: {operation} for user {user_id}", extra=log_data)
