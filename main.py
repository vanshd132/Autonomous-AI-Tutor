"""
Autonomous AI Tutor Orchestrator
A robust system for intelligent parameter extraction and educational tool orchestration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Tutor Orchestrator",
    description="Intelligent middleware for autonomous AI tutoring systems",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class UserInfo(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Student's full name")
    grade_level: str = Field(..., description="Student's current grade level")
    learning_style_summary: str = Field(..., description="Summary of student's preferred learning style")
    emotional_state_summary: str = Field(..., description="Current emotional state of the student")
    mastery_level_summary: str = Field(..., description="Current mastery level description")

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

class ConversationRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    current_message: str = Field(..., description="Current student message to process")

class ToolRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the educational tool to use")
    parameters: Dict[str, Any] = Field(..., description="Tool-specific parameters")

class ToolResponse(BaseModel):
    success: bool
    tool_name: str
    response_data: Dict[str, Any]
    error_message: Optional[str] = None

# Core orchestration logic
class TutorOrchestrator:
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
    
    def extract_parameters(self, conversation_request: ConversationRequest) -> Dict[str, Any]:
        """Extract parameters from conversation context using intelligent inference."""
        user_info = conversation_request.user_info
        chat_history = conversation_request.chat_history
        current_message = conversation_request.current_message
        
        # Simple but effective parameter extraction
        extracted = {
            "user_info": user_info.dict(),
            "chat_history": [msg.dict() for msg in chat_history]
        }
        
        # Extract topic and subject from conversation
        topic = self._extract_topic(current_message, chat_history)
        subject = self._extract_subject(current_message, chat_history)
        
        # Determine tool type based on conversation context
        tool_type = self._determine_tool_type(current_message)
        
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
        
        return extracted, tool_type
    
    def _extract_topic(self, message: str, chat_history: List[ChatMessage]) -> str:
        """Extract the main topic from conversation."""
        # Simple keyword extraction - in production, use NLP
        educational_keywords = [
            "math", "calculus", "algebra", "geometry", "statistics",
            "science", "biology", "chemistry", "physics", "environmental",
            "history", "literature", "english", "writing", "reading",
            "programming", "computer science", "coding"
        ]
        
        text = message.lower()
        for keyword in educational_keywords:
            if keyword in text:
                return keyword.title()
        
        # Fallback to first few words
        return message.split()[:3] if message.split() else "General Topic"
    
    def _extract_subject(self, message: str, chat_history: List[ChatMessage]) -> str:
        """Extract subject area from conversation."""
        subject_mapping = {
            "math": "Mathematics",
            "calculus": "Mathematics", 
            "algebra": "Mathematics",
            "science": "Science",
            "biology": "Biology",
            "chemistry": "Chemistry",
            "physics": "Physics",
            "history": "History",
            "english": "English",
            "literature": "English"
        }
        
        text = message.lower()
        for keyword, subject in subject_mapping.items():
            if keyword in text:
                return subject
        
        return "General Education"
    
    def _determine_tool_type(self, message: str) -> str:
        """Determine which educational tool to use based on conversation."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["note", "notes", "summary", "outline"]):
            return "note_maker"
        elif any(word in message_lower for word in ["flashcard", "quiz", "test", "practice", "review"]):
            return "flashcard_generator"
        elif any(word in message_lower for word in ["explain", "understand", "concept", "how", "what", "why"]):
            return "concept_explainer"
        else:
            return "concept_explainer"  # Default fallback
    
    def _infer_note_style(self, learning_style: str) -> str:
        """Infer note-taking style from learning style."""
        if "visual" in learning_style.lower():
            return "structured"
        elif "kinesthetic" in learning_style.lower():
            return "bullet_points"
        elif "auditory" in learning_style.lower():
            return "narrative"
        else:
            return "outline"
    
    def _infer_flashcard_count(self, message: str) -> int:
        """Infer number of flashcards needed."""
        if "few" in message.lower() or "some" in message.lower():
            return 5
        elif "many" in message.lower() or "lot" in message.lower():
            return 15
        else:
            return 10  # Default
    
    def _infer_difficulty(self, mastery_level: str, message: str) -> str:
        """Infer difficulty level from mastery and message context."""
        if "struggling" in message.lower() or "difficult" in message.lower():
            return "easy"
        elif "advanced" in message.lower() or "expert" in message.lower():
            return "hard"
        elif "level 7" in mastery_level.lower() or "level 8" in mastery_level.lower():
            return "hard"
        elif "level 4" in mastery_level.lower() or "level 5" in mastery_level.lower():
            return "medium"
        else:
            return "medium"
    
    def _infer_depth(self, mastery_level: str, message: str) -> str:
        """Infer explanation depth from mastery level and message."""
        if "basic" in message.lower() or "simple" in message.lower():
            return "basic"
        elif "advanced" in message.lower() or "comprehensive" in message.lower():
            return "comprehensive"
        elif "level 8" in mastery_level.lower() or "level 9" in mastery_level.lower():
            return "advanced"
        elif "level 2" in mastery_level.lower() or "level 3" in mastery_level.lower():
            return "basic"
        else:
            return "intermediate"

# Initialize orchestrator
orchestrator = TutorOrchestrator()

# Mock educational tools (in production, these would call real APIs)
class MockEducationalTools:
    @staticmethod
    def note_maker(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Mock Note Maker tool."""
        return {
            "topic": parameters.get("topic", "General Topic"),
            "title": f"Notes on {parameters.get('topic', 'General Topic')}",
            "summary": f"Comprehensive notes covering {parameters.get('topic', 'the topic')} with examples and key concepts.",
            "note_sections": [
                {
                    "title": "Introduction",
                    "content": f"Introduction to {parameters.get('topic', 'the topic')}",
                    "key_points": ["Key concept 1", "Key concept 2"],
                    "examples": ["Example 1", "Example 2"],
                    "analogies": ["Analogy 1"] if parameters.get("include_analogies") else []
                }
            ],
            "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
            "practice_suggestions": ["Practice exercise 1", "Practice exercise 2"],
            "note_taking_style": parameters.get("note_taking_style", "outline")
        }
    
    @staticmethod
    def flashcard_generator(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Mock Flashcard Generator tool."""
        topic = parameters.get("topic", "General Topic")
        count = parameters.get("count", 5)
        
        flashcards = []
        for i in range(count):
            flashcards.append({
                "title": f"Question {i+1}",
                "question": f"What is the main concept of {topic}?",
                "answer": f"The main concept of {topic} is...",
                "example": f"Example: {topic} in practice..."
            })
        
        return {
            "flashcards": flashcards,
            "topic": topic,
            "adaptation_details": f"Adapted for {parameters.get('difficulty', 'medium')} difficulty",
            "difficulty": parameters.get("difficulty", "medium")
        }
    
    @staticmethod
    def concept_explainer(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Mock Concept Explainer tool."""
        concept = parameters.get("concept_to_explain", "General Concept")
        depth = parameters.get("desired_depth", "intermediate")
        
        return {
            "explanation": f"This is a {depth} explanation of {concept}. It covers the fundamental principles and applications.",
            "examples": [
                f"Example 1: {concept} in real-world scenario",
                f"Example 2: {concept} in academic context"
            ],
            "related_concepts": ["Related concept 1", "Related concept 2"],
            "visual_aids": ["Diagram suggestion", "Chart recommendation"],
            "practice_questions": [
                f"How does {concept} work?",
                f"What are the applications of {concept}?"
            ],
            "source_references": ["Reference 1", "Reference 2"]
        }

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "AI Tutor Orchestrator is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/orchestrate", response_model=ToolResponse)
async def orchestrate_conversation(conversation_request: ConversationRequest):
    """
    Main orchestration endpoint that processes conversation and calls appropriate educational tools.
    """
    try:
        logger.info(f"Processing conversation for user: {conversation_request.user_info.name}")
        
        # Extract parameters and determine tool
        parameters, tool_type = orchestrator.extract_parameters(conversation_request)
        
        # Call the appropriate educational tool
        if tool_type == "note_maker":
            response_data = MockEducationalTools.note_maker(parameters)
        elif tool_type == "flashcard_generator":
            response_data = MockEducationalTools.flashcard_generator(parameters)
        elif tool_type == "concept_explainer":
            response_data = MockEducationalTools.concept_explainer(parameters)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool type: {tool_type}")
        
        return ToolResponse(
            success=True,
            tool_name=tool_type,
            response_data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error in orchestration: {str(e)}")
        return ToolResponse(
            success=False,
            tool_name="unknown",
            response_data={},
            error_message=str(e)
        )

@app.post("/api/tools/{tool_name}")
async def call_tool_directly(tool_name: str, tool_request: ToolRequest):
    """
    Direct tool calling endpoint for testing individual tools.
    """
    try:
        if tool_name == "note_maker":
            response_data = MockEducationalTools.note_maker(tool_request.parameters)
        elif tool_name == "flashcard_generator":
            response_data = MockEducationalTools.flashcard_generator(tool_request.parameters)
        elif tool_name == "concept_explainer":
            response_data = MockEducationalTools.concept_explainer(tool_request.parameters)
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        return ToolResponse(
            success=True,
            tool_name=tool_name,
            response_data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error calling tool {tool_name}: {str(e)}")
        return ToolResponse(
            success=False,
            tool_name=tool_name,
            response_data={},
            error_message=str(e)
        )

@app.get("/api/tools")
async def list_available_tools():
    """List all available educational tools."""
    return {
        "available_tools": list(orchestrator.tool_schemas.keys()),
        "tool_schemas": orchestrator.tool_schemas
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
