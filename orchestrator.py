"""
AI Tutor Orchestrator Core Logic
Handles intelligent parameter extraction and tool selection
"""

import logging
from typing import Dict, Any, Tuple, List
from models import ConversationRequest, UserInfo, ChatMessage

logger = logging.getLogger(__name__)

class TutorOrchestrator:
    """Core orchestration logic for intelligent parameter extraction and tool selection"""
    
    def __init__(self):
        self.tool_schemas = {
            "note_maker": {
                "required": ["user_info", "chat_history", "topic", "subject", "note_taking_style"],
                "optional": ["include_examples", "include_analogies"]
            },
            "flashcard_generator": {
                "required": ["user_info", "topic", "count", "difficulty", "subject"],
                "optional": ["include_examples"]
            },
            "concept_explainer": {
                "required": ["user_info", "chat_history", "concept_to_explain", "current_topic", "desired_depth"],
                "optional": []
            }
        }
        
        # Educational keywords for topic detection
        self.educational_keywords = [
            "math", "calculus", "algebra", "geometry", "statistics",
            "science", "biology", "chemistry", "physics", "environmental",
            "history", "literature", "english", "writing", "reading",
            "programming", "computer science", "coding", "photosynthesis",
            "derivatives", "equations", "world war", "photosynthesis"
        ]
        
        # Subject mapping for classification
        self.subject_mapping = {
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
    
    def extract_parameters(self, conversation_request: ConversationRequest) -> Tuple[Dict[str, Any], str]:
        """
        Extract parameters from conversation context using intelligent inference.
        
        Args:
            conversation_request: The conversation data to process
            
        Returns:
            Tuple of (extracted_parameters, tool_type)
        """
        user_info = conversation_request.user_info
        chat_history = conversation_request.chat_history
        current_message = conversation_request.current_message
        
        logger.info(f"Extracting parameters for user: {user_info.name}")
        
        # Initialize base parameters
        extracted = {
            "user_info": user_info.dict(),
            "chat_history": [msg.dict() for msg in chat_history]
        }
        
        # Extract topic and subject from conversation
        topic = self._extract_topic(current_message, chat_history)
        subject = self._extract_subject(current_message, chat_history)
        
        # Determine tool type based on conversation context
        tool_type = self._determine_tool_type(current_message)
        
        # Add tool-specific parameters
        if tool_type == "note_maker":
            extracted.update({
                "topic": topic,
                "subject": subject,
                "note_taking_style": self._infer_note_style(user_info.learning_style_summary),
                "include_examples": True,
                "include_analogies": "visual" in user_info.learning_style_summary.lower()
            })
        elif tool_type == "flashcard_generator":
            extracted.update({
                "topic": topic,
                "subject": subject,
                "count": self._infer_flashcard_count(current_message),
                "difficulty": self._infer_difficulty(user_info.mastery_level_summary, current_message),
                "include_examples": True
            })
        elif tool_type == "concept_explainer":
            extracted.update({
                "concept_to_explain": topic,
                "current_topic": subject,
                "desired_depth": self._infer_depth(user_info.mastery_level_summary, current_message)
            })
        
        logger.info(f"Extracted parameters for tool: {tool_type}")
        return extracted, tool_type
    
    def _extract_topic(self, message: str, chat_history: List[ChatMessage]) -> str:
        """Extract the main topic from conversation."""
        # Combine current message with recent chat history
        full_text = message.lower()
        for msg in chat_history[-3:]:  # Look at last 3 messages
            full_text += " " + msg.content.lower()
        
        # Check for educational keywords
        for keyword in self.educational_keywords:
            if keyword in full_text:
                return keyword.title()
        
        # Fallback to first few words
        words = message.split()
        if len(words) >= 3:
            return " ".join(words[:3])
        return "General Topic"
    
    def _extract_subject(self, message: str, chat_history: List[ChatMessage]) -> str:
        """Extract subject area from conversation."""
        full_text = message.lower()
        for msg in chat_history[-2:]:  # Look at last 2 messages
            full_text += " " + msg.content.lower()
        
        for keyword, subject in self.subject_mapping.items():
            if keyword in full_text:
                return subject
        
        return "General Education"
    
    def _determine_tool_type(self, message: str) -> str:
        """Determine which educational tool to use based on conversation."""
        message_lower = message.lower()
        
        # Note-making keywords
        if any(word in message_lower for word in ["note", "notes", "summary", "outline", "study guide"]):
            return "note_maker"
        
        # Flashcard/practice keywords
        elif any(word in message_lower for word in ["flashcard", "quiz", "test", "practice", "review", "memorize"]):
            return "flashcard_generator"
        
        # Explanation keywords
        elif any(word in message_lower for word in ["explain", "understand", "concept", "how", "what", "why", "confused"]):
            return "concept_explainer"
        
        else:
            return "concept_explainer"  # Default fallback
    
    def _infer_note_style(self, learning_style: str) -> str:
        """Infer note-taking style from learning style."""
        style_lower = learning_style.lower()
        
        if "visual" in style_lower:
            return "structured"
        elif "kinesthetic" in style_lower:
            return "bullet_points"
        elif "auditory" in style_lower:
            return "narrative"
        else:
            return "outline"
    
    def _infer_flashcard_count(self, message: str) -> int:
        """Infer number of flashcards needed."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["few", "some", "little"]):
            return 5
        elif any(word in message_lower for word in ["many", "lot", "comprehensive", "extensive"]):
            return 15
        else:
            return 10  # Default
    
    def _infer_difficulty(self, mastery_level: str, message: str) -> str:
        """Infer difficulty level from mastery and message context."""
        message_lower = message.lower()
        mastery_lower = mastery_level.lower()
        
        # Message-based inference
        if any(word in message_lower for word in ["struggling", "difficult", "hard", "confused"]):
            return "easy"
        elif any(word in message_lower for word in ["advanced", "expert", "challenging"]):
            return "hard"
        
        # Mastery level-based inference
        elif "level 7" in mastery_lower or "level 8" in mastery_lower or "level 9" in mastery_lower:
            return "hard"
        elif "level 4" in mastery_lower or "level 5" in mastery_lower or "level 6" in mastery_lower:
            return "medium"
        elif "level 1" in mastery_lower or "level 2" in mastery_lower or "level 3" in mastery_lower:
            return "easy"
        else:
            return "medium"
    
    def _infer_depth(self, mastery_level: str, message: str) -> str:
        """Infer explanation depth from mastery level and message."""
        message_lower = message.lower()
        mastery_lower = mastery_level.lower()
        
        # Message-based inference
        if any(word in message_lower for word in ["basic", "simple", "beginner", "confused"]):
            return "basic"
        elif any(word in message_lower for word in ["advanced", "comprehensive", "detailed"]):
            return "comprehensive"
        
        # Mastery level-based inference
        elif "level 8" in mastery_lower or "level 9" in mastery_lower or "level 10" in mastery_lower:
            return "advanced"
        elif "level 2" in mastery_lower or "level 3" in mastery_lower:
            return "basic"
        elif "level 6" in mastery_lower or "level 7" in mastery_lower:
            return "intermediate"
        else:
            return "intermediate"
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get list of available tools and their schemas."""
        return {
            "available_tools": list(self.tool_schemas.keys()),
            "tool_schemas": self.tool_schemas
        }
