import logging
from app.core.config import get_settings

def setup_logging():
    """Configure application logging"""
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at {settings.log_level} level")
    logger.info(f"OpenRouter API configured: {'Yes' if settings.is_openrouter_configured else 'No'}")
    
    if settings.is_openrouter_configured:
        logger.info(f"API Key: {settings.openrouter_api_key[:10]}...")
    
    return logger