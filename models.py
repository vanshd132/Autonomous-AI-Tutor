"""
Pydantic models for AI Tutor Orchestrator
Defines all data structures and validation schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# User Information Models
class UserInfo(BaseModel):
    """Student profile information"""
    user_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Student's full name")
    grade_level: str = Field(..., description="Student's current grade level")
    learning_style_summary: str = Field(..., description="Summary of student's preferred learning style")
    emotional_state_summary: str = Field(..., description="Current emotional state of the student")
    mastery_level_summary: str = Field(..., description="Current mastery level description")

class ChatMessage(BaseModel):
    """Individual chat message"""
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

# Request/Response Models
class ConversationRequest(BaseModel):
    """Main orchestration request"""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    current_message: str = Field(..., description="Current student message to process")

class ToolRequest(BaseModel):
    """Direct tool calling request"""
    tool_name: str = Field(..., description="Name of the educational tool to use")
    parameters: Dict[str, Any] = Field(..., description="Tool-specific parameters")

class ToolResponse(BaseModel):
    """Standard tool response"""
    success: bool
    tool_name: str
    response_data: Dict[str, Any]
    error_message: Optional[str] = None

class HealthResponse(BaseModel):
    """API health check response"""
    message: str
    status: str
    timestamp: str

class ToolListResponse(BaseModel):
    """Available tools response"""
    available_tools: List[str]
    tool_schemas: Dict[str, Dict[str, Any]]

# Educational Tool Models
class NoteMakerRequest(BaseModel):
    """Note Maker tool request"""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str
    subject: str
    note_taking_style: str = Field(..., pattern="^(outline|bullet_points|narrative|structured)$")
    include_examples: bool = True
    include_analogies: bool = False

class FlashcardGeneratorRequest(BaseModel):
    """Flashcard Generator tool request"""
    user_info: UserInfo
    topic: str
    count: int = Field(..., ge=1, le=20)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    subject: str
    include_examples: bool = True

class ConceptExplainerRequest(BaseModel):
    """Concept Explainer tool request"""
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str
    current_topic: str
    desired_depth: str = Field(..., pattern="^(basic|intermediate|advanced|comprehensive)$")

# Response Models for Educational Tools
class NoteSection(BaseModel):
    """Individual note section"""
    title: str
    content: str
    key_points: List[str]
    examples: List[str]
    analogies: List[str]

class NoteMakerResponse(BaseModel):
    """Note Maker tool response"""
    topic: str
    title: str
    summary: str
    note_sections: List[NoteSection]
    key_concepts: List[str]
    connections_to_prior_learning: List[str]
    visual_elements: List[Dict[str, Any]]
    practice_suggestions: List[str]
    source_references: List[str]
    note_taking_style: str

class Flashcard(BaseModel):
    """Individual flashcard"""
    title: str
    question: str
    answer: str
    example: Optional[str] = None

class FlashcardGeneratorResponse(BaseModel):
    """Flashcard Generator tool response"""
    flashcards: List[Flashcard]
    topic: str
    adaptation_details: str
    difficulty: str

class ConceptExplainerResponse(BaseModel):
    """Concept Explainer tool response"""
    explanation: str
    examples: List[str]
    related_concepts: List[str]
    visual_aids: List[str]
    practice_questions: List[str]
    source_references: List[str]
