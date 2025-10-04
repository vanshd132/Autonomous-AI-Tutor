"""
Autonomous AI Tutor Orchestrator
A robust system for intelligent parameter extraction and educational tool orchestration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

# Import organized modules
from models import ConversationRequest, ToolRequest, ToolResponse, HealthResponse, ToolListResponse
from orchestrator import TutorOrchestrator
from educational_tools import EducationalTools
from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=Config.CORS_CREDENTIALS,
    allow_methods=Config.CORS_METHODS,
    allow_headers=Config.CORS_HEADERS,
)

# Initialize orchestrator
orchestrator = TutorOrchestrator()

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        message="AI Tutor Orchestrator is running!",
        status="healthy",
        timestamp=datetime.now().isoformat()
    )

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
        response_data = EducationalTools.call_tool(tool_type, parameters)
        
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

@app.post("/api/tools/{tool_name}", response_model=ToolResponse)
async def call_tool_directly(tool_name: str, tool_request: ToolRequest):
    """
    Direct tool calling endpoint for testing individual tools.
    """
    try:
        if tool_name not in EducationalTools.get_supported_tools():
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        response_data = EducationalTools.call_tool(tool_name, tool_request.parameters)
        
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

@app.get("/api/tools", response_model=ToolListResponse)
async def list_available_tools():
    """List all available educational tools."""
    tools_info = orchestrator.get_available_tools()
    return ToolListResponse(**tools_info)

@app.get("/api/config")
async def get_configuration():
    """Get system configuration."""
    return Config.get_config()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
