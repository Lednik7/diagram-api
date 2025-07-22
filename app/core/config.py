import os
import logging
from functools import lru_cache

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.getLogger(__name__).info("Loaded .env file")
except ImportError:
    logging.getLogger(__name__).warning("python-dotenv not installed, using system environment")

class Settings:
    # OpenRouter Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Application Configuration
    app_name: str = "Diagram API"
    app_version: str = "1.0.0"
    
    @property
    def is_openrouter_configured(self) -> bool:
        return bool(self.openrouter_api_key)

@lru_cache()
def get_settings() -> Settings:
    return Settings()