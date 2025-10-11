# AI Tutor Orchestrator

An intelligent middleware system that autonomously connects conversational AI tutors to multiple educational tools by extracting required parameters from chat context and managing complex tool interactions.

## 🚀 Past Projects

This project builds upon my previous work in AI and data processing:

- **[Pinecone PDF Uploader](https://github.com/vanshd132/Pinecone)** - A web application for uploading PDF documents, extracting text, chunking content, and storing in Pinecone vector database for RAG chatbots
- **[Balance Sheet AI Analyst](https://github.com/vanshd132/Balance-Sheet-AI-Analyst-)** - AI-powered balance sheet analysis platform with role-based access (Analyst/CEO/Top Management), Google Gemini integration, and real-time financial insights
- **[VisionForge](https://github.com/vanshd132/VisionForge)** - Advanced computer vision and image processing project

## 🚀 Quick Start (Minimal Setup)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python main.py
   ```

3. **Test the system:**
   ```bash
   python demo.py
   ```

That's it! The system will be running on `http://localhost:8000`

## 📋 What This System Does

This orchestrator acts as the "brain" between a student's conversation with an AI tutor and actual educational tools. It:

- **Understands conversation context** and determines what educational tools are needed
- **Extracts parameters** required by various tools from natural conversation
- **Validates and formats requests** to ensure proper tool execution
- **Handles diverse tool schemas** across multiple educational functionalities
- **Maintains conversation state** and student personalization context

## 🛠️ Available Educational Tools

1. **Note Maker** - Generates structured notes based on topics and learning styles
2. **Flashcard Generator** - Creates practice flashcards with adaptive difficulty
3. **Concept Explainer** - Provides detailed explanations with examples and visual aids

## 📊 API Endpoints

### Main Orchestration
- `POST /api/orchestrate` - Process conversation and call appropriate tools
- `GET /api/tools` - List available educational tools
- `POST /api/tools/{tool_name}` - Call specific tools directly

### Health Check
- `GET /` - API health status

## 🎯 Example Usage

### Conversation-Based Orchestration

```python
import requests

# Student conversation
conversation_data = {
    "user_info": {
        "user_id": "student123",
        "name": "Alice",
        "grade_level": "10",
        "learning_style_summary": "Visual learner, prefers structured notes",
        "emotional_state_summary": "Focused and motivated",
        "mastery_level_summary": "Level 6: Good understanding"
    },
    "chat_history": [
        {"role": "user", "content": "I'm studying for my biology exam"},
        {"role": "assistant", "content": "What topics are you covering?"}
    ],
    "current_message": "I need comprehensive notes on photosynthesis"
}

# Send to orchestrator
response = requests.post("http://localhost:8000/api/orchestrate", json=conversation_data)
result = response.json()

# System automatically:
# 1. Extracts topic: "photosynthesis"
# 2. Determines tool: "note_maker"
# 3. Infers parameters: note_taking_style="structured", include_examples=True
# 4. Calls Note Maker tool
# 5. Returns formatted notes
```

### Direct Tool Calling

```python
# Call flashcard generator directly
tool_request = {
    "tool_name": "flashcard_generator",
    "parameters": {
        "user_info": {...},
        "topic": "World War II",
        "count": 5,
        "difficulty": "medium",
        "subject": "History"
    }
}

response = requests.post("http://localhost:8000/api/tools/flashcard_generator", json=tool_request)
```

## 🧠 Intelligent Features

### Parameter Extraction
- **Topic Detection**: Automatically identifies educational topics from conversation
- **Subject Classification**: Maps topics to academic subjects
- **Tool Selection**: Determines appropriate educational tool based on context
- **Style Inference**: Adapts content format to student's learning style

### Personalization
- **Learning Style**: Visual, Auditory, Kinesthetic adaptation
- **Emotional State**: Adjusts difficulty and approach based on student mood
- **Mastery Level**: Scales content complexity (Levels 1-10)
- **Grade Level**: Age-appropriate content and examples

### Adaptive Intelligence
- **Difficulty Scaling**: Automatically adjusts based on mastery level
- **Content Format**: Chooses note styles, flashcard complexity, explanation depth
- **Example Inclusion**: Determines when to include examples and analogies
- **Context Awareness**: Uses conversation history for better parameter inference

## 🔧 System Architecture

```
Student Conversation → Orchestrator → Educational Tools
     ↓                    ↓              ↓
  Context Analysis   Parameter      Tool Execution
                    Extraction
     ↓                    ↓              ↓
  Intent Detection   Validation      Response
                    & Formatting     Processing
```

### Core Components

1. **Context Analysis Engine**: Parses conversation and identifies educational intent
2. **Parameter Extraction System**: Maps conversational elements to tool parameters
3. **Tool Orchestration Layer**: Manages API calls to educational tools
4. **State Management**: Maintains conversation context and student preferences
5. **Schema Validation**: Ensures requests meet tool specifications

## 📈 Demo Scenarios

The `demo.py` script showcases:

1. **Note Making**: Student requests notes on biology topics
2. **Flashcard Generation**: Student needs practice materials
3. **Concept Explanation**: Student asks for topic clarification
4. **Direct Tool Calling**: Testing individual tool functionality

## 🛡️ Error Handling

The system includes robust error handling for:
- Invalid input parameters
- Tool execution failures
- Network connectivity issues
- Schema validation errors
- Missing required parameters

## 🔍 Testing

Run the comprehensive demo:
```bash
python demo.py
```

This will test all major functionality and show realistic usage scenarios.

## 📚 API Documentation

Once the server is running, visit:
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/redoc` - Alternative API documentation

## 🚀 Production Considerations

For production deployment, consider:
- **Real Educational Tools**: Replace mock tools with actual API integrations
- **Database Integration**: Add persistent storage for conversation history
- **Authentication**: Implement user authentication and authorization
- **Rate Limiting**: Add request rate limiting and throttling
- **Monitoring**: Add logging and performance monitoring
- **Scaling**: Consider horizontal scaling for high traffic
