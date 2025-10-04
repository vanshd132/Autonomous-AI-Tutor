git # AI Tutor Orchestrator - Project Structure

## 📁 Organized Project Layout

```
Autonomous-AI-Tutor/
├── main.py                    # FastAPI application entry point
├── models.py                  # Pydantic models and data structures
├── orchestrator.py           # Core orchestration logic
├── educational_tools.py      # Educational tools implementation
├── config.py                 # Configuration management
├── utils.py                  # Utility functions
├── demo.py                   # Demo script
├── __init__.py               # Package initialization
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows launcher
├── test.bat                  # Demo runner
├── README.md                 # Project documentation
└── PROJECT_STRUCTURE.md      # This file
```

## 🧩 Module Breakdown

### **main.py** - FastAPI Application
- **Purpose**: Application entry point and API endpoints
- **Responsibilities**:
  - FastAPI app initialization
  - CORS middleware configuration
  - API endpoint definitions
  - Request/response handling
  - Error handling and logging

### **models.py** - Data Models
- **Purpose**: Pydantic models for request/response validation
- **Contains**:
  - `UserInfo` - Student profile information
  - `ChatMessage` - Individual chat messages
  - `ConversationRequest` - Main orchestration request
  - `ToolRequest` - Direct tool calling request
  - `ToolResponse` - Standard tool response
  - Educational tool request/response models
  - Health check and configuration models

### **orchestrator.py** - Core Logic
- **Purpose**: Intelligent parameter extraction and tool selection
- **Key Features**:
  - `TutorOrchestrator` class with intelligent parameter extraction
  - Topic and subject detection from conversation
  - Tool type determination based on context
  - Parameter inference for different tools
  - Learning style and mastery level adaptation

### **educational_tools.py** - Tool Implementation
- **Purpose**: Mock implementations of educational tools
- **Tools**:
  - `note_maker` - Generate structured notes
  - `flashcard_generator` - Create practice flashcards
  - `concept_explainer` - Provide detailed explanations
- **Features**:
  - Adaptive content generation
  - Difficulty scaling
  - Learning style adaptation

### **config.py** - Configuration Management
- **Purpose**: Centralized configuration and settings
- **Features**:
  - Environment variable support
  - API configuration
  - CORS settings
  - Educational tool parameters
  - Logging configuration

### **utils.py** - Utility Functions
- **Purpose**: Helper functions and utilities
- **Features**:
  - Logging setup
  - Parameter validation
  - Error response formatting
  - Input sanitization
  - Keyword extraction
  - Difficulty calculation

## 🔄 Data Flow

```
Student Conversation
        ↓
   main.py (API)
        ↓
orchestrator.py (Parameter Extraction)
        ↓
educational_tools.py (Tool Execution)
        ↓
models.py (Response Validation)
        ↓
Student Response
```

## 🛠️ Key Benefits of Organization

### **1. Separation of Concerns**
- **API Layer** (`main.py`) - Handles HTTP requests/responses
- **Business Logic** (`orchestrator.py`) - Core intelligence
- **Tool Implementation** (`educational_tools.py`) - Educational tools
- **Data Models** (`models.py`) - Type safety and validation

### **2. Maintainability**
- **Clear module boundaries** - Easy to locate and modify code
- **Single responsibility** - Each module has one clear purpose
- **Reduced coupling** - Modules can be modified independently

### **3. Scalability**
- **Easy to add new tools** - Just extend `educational_tools.py`
- **Configuration management** - Centralized in `config.py`
- **Modular testing** - Each component can be tested independently

### **4. Code Quality**
- **Type safety** - Pydantic models ensure data integrity
- **Error handling** - Centralized error handling and logging
- **Documentation** - Clear docstrings and type hints

## 🚀 Usage Examples

### **Importing Modules**
```python
from models import ConversationRequest, ToolResponse
from orchestrator import TutorOrchestrator
from educational_tools import EducationalTools
from config import Config
from utils import setup_logging, validate_parameters
```

### **Adding New Educational Tool**
1. Add tool implementation to `educational_tools.py`
2. Add tool schema to `orchestrator.py`
3. Add request/response models to `models.py`
4. Update configuration in `config.py` if needed

### **Extending Orchestration Logic**
1. Modify parameter extraction in `orchestrator.py`
2. Add new inference methods
3. Update tool selection logic
4. Test with demo scenarios

## 📊 Performance Benefits

- **Faster imports** - Only load what you need
- **Memory efficiency** - Modular loading
- **Better debugging** - Clear error locations
- **Easier testing** - Isolated components
- **Cleaner code** - Organized and readable

## 🔧 Development Workflow

1. **Modify business logic** → `orchestrator.py`
2. **Add new tools** → `educational_tools.py`
3. **Update data models** → `models.py`
4. **Change configuration** → `config.py`
5. **Add utilities** → `utils.py`
6. **Test changes** → `demo.py`

This organized structure makes the codebase professional, maintainable, and ready for production deployment! 🎯
