import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import DiagramRequest, DiagramResponse, AssistantRequest, AssistantResponse
from app.services.llm_service import LLMService
from app.services.diagram_service import DiagramService
from app.services.diagram_tools import get_available_tools

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency injection
def get_llm_service() -> LLMService:
    return LLMService()

def get_diagram_service() -> DiagramService:
    return DiagramService()

@router.get("/")
async def root():
    return {"message": "Diagram API", "docs": "/docs"}

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.post("/generate-diagram", response_model=DiagramResponse)
async def generate_diagram(
    request: DiagramRequest,
    llm_service: LLMService = Depends(get_llm_service),
    diagram_service: DiagramService = Depends(get_diagram_service)
):
    """Generate a diagram from description using agent with tools"""
    logger.info(f"=== GENERATE DIAGRAM REQUEST ===")
    logger.info(f"Description: {request.description}")
    
    try:
        # Agent generates diagram specification using available tools
        logger.info("Step 1: Generating specification with LLM agent...")
        spec = llm_service.generate_diagram_spec(request.description)
        logger.info("Step 1: Specification generated successfully")
        
        # Create diagram from specification using parser
        logger.info("Step 2: Creating diagram from specification...")
        image_data = diagram_service.create_diagram_from_spec(spec)
        logger.info("Step 2: Diagram created successfully")
        
        logger.info("=== REQUEST COMPLETED SUCCESSFULLY ===")
        return DiagramResponse(
            image_data=image_data,
            message="Diagram generated successfully by agent"
        )
    except Exception as e:
        logger.error(f"Diagram generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Diagram generation failed: {str(e)}")

@router.post("/debug-spec")
async def debug_spec(
    request: DiagramRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """Debug endpoint to see what specification the agent generates"""
    try:
        spec = llm_service.generate_diagram_spec(request.description)
        return {"specification": spec.model_dump()}
    except Exception as e:
        logger.error(f"Debug spec failed: {e}")
        raise HTTPException(status_code=500, detail=f"Debug spec failed: {str(e)}")

@router.get("/tools")
async def get_tools():
    """Get available diagram tools"""
    tools = get_available_tools()
    return {
        "total_tools": len(tools),
        "tools": tools,
        "by_provider": {
            "aws": {k: v for k, v in tools.items() if k.startswith("aws.")},
            "gcp": {k: v for k, v in tools.items() if k.startswith("gcp.")},
            "azure": {k: v for k, v in tools.items() if k.startswith("azure.")}
        }
    }

@router.post("/assistant", response_model=AssistantResponse)
async def assistant(
    request: AssistantRequest,
    llm_service: LLMService = Depends(get_llm_service),
    diagram_service: DiagramService = Depends(get_diagram_service)
):
    """Assistant-style endpoint that understands user intent and responds helpfully"""
    logger.info(f"=== ASSISTANT REQUEST ===")
    logger.info(f"Message: {request.message}")
    logger.info(f"Context: {request.context}")
    
    try:
        # Use LLM to understand user intent
        response = llm_service.process_assistant_request(request.message, request.context)
        
        # If the response indicates diagram generation is needed
        if response.get("action") == "generate_diagram":
            logger.info("Assistant determined diagram generation is needed")
            spec = llm_service.generate_diagram_spec(response["description"])
            image_data = diagram_service.create_diagram_from_spec(spec)
            
            return AssistantResponse(
                response=response["response"],
                action="diagram_generated",
                image_data=image_data
            )
        else:
            # Just return the conversational response
            return AssistantResponse(
                response=response["response"],
                action=response.get("action")
            )
            
    except Exception as e:
        logger.error(f"Assistant error: {e}")
        raise HTTPException(status_code=500, detail=f"Assistant error: {str(e)}")