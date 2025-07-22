import json
import logging
from openai import OpenAI
from app.core.config import get_settings
from app.services.diagram_tools import get_available_tools
from app.models.schemas import DiagramSpec

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.is_openrouter_configured:
            raise Exception("OPENROUTER_API_KEY not configured")
        
        self.client = OpenAI(
            api_key=self.settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        logger.info("OpenRouter client configured successfully")
    
    def generate_diagram_spec(self, description: str) -> DiagramSpec:
        """Use OpenRouter agent to generate diagram specification from description"""
        logger.info(f"Generating diagram spec for: {description[:50]}...")
        
        # Agent prompt with available tools
        tools_list = "\n".join([f"- {k}: {v}" for k, v in get_available_tools().items()])
        logger.info(f"Available tools: {len(get_available_tools())}")
        
        system_prompt = f"""You are a system architecture agent. You have access to these diagram tools:

{tools_list}

Your task is to analyze user descriptions and generate JSON specifications for system architecture diagrams.

You must respond with valid JSON that conforms to this JSON schema:

{{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["diagram", "nodes"],
  "properties": {{
    "diagram": {{
      "type": "object",
      "required": ["name", "filename", "show"],
      "properties": {{
        "name": {{"type": "string"}},
        "filename": {{"type": "string"}},
        "show": {{"type": "boolean"}}
      }}
    }},
    "nodes": {{
      "type": "array",
      "items": {{
        "type": "object",
        "required": ["id", "type", "label"],
        "properties": {{
          "id": {{"type": "string"}},
          "type": {{"type": "string"}},
          "label": {{"type": "string"}}
        }}
      }}
    }},
    "clusters": {{
      "type": "array",
      "items": {{
        "type": "object",
        "required": ["id", "name", "nodes"],
        "properties": {{
          "id": {{"type": "string"}},
          "name": {{"type": "string"}},
          "nodes": {{
            "type": "array",
            "items": {{"type": "string"}}
          }}
        }}
      }}
    }},
    "edges": {{
      "type": "array", 
      "items": {{
        "type": "object",
        "required": ["from", "to"],
        "properties": {{
          "from": {{"type": "string"}},
          "to": {{"type": "string"}}
        }}
      }}
    }}
  }}
}}

Example response format:
{{
  "diagram": {{
    "name": "Architecture Name",
    "filename": "diagram",  
    "show": false
  }},
  "nodes": [
    {{"id": "node_id", "type": "aws.network.ALB", "label": "Component Name"}}
  ],
  "clusters": [
    {{"id": "cluster_id", "name": "Cluster Name", "nodes": ["node1", "node2"]}}
  ],
  "edges": [
    {{"from": "source_id", "to": "target_id"}}
  ]
}}

Rules:
1. Use appropriate node types from the available tools
2. Create logical connections between components  
3. Group related nodes in clusters if mentioned
4. Use descriptive labels and IDs
5. Return ONLY valid JSON that matches the schema, no explanations"""

        user_prompt = f"Create a diagram specification for: {description}"
        
        logger.info("Sending request to OpenRouter...")
        logger.debug(f"System prompt length: {len(system_prompt)} characters")
        logger.debug(f"User prompt: {user_prompt}")
        
        response = self.client.chat.completions.create(
            model=self.settings.openrouter_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        logger.info("Received response from OpenRouter")
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"Raw response length: {len(response_text)} characters")
        logger.info(f"Raw response preview: {response_text[:200]}...")
        
        # Clean response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
            logger.info("Removed ```json prefix")
        if response_text.startswith('```'):
            response_text = response_text[3:]
            logger.info("Removed ``` prefix")
        if response_text.endswith('```'):
            response_text = response_text[:-3]
            logger.info("Removed ``` suffix")
        response_text = response_text.strip()
        
        logger.info(f"Cleaned response length: {len(response_text)} characters")
        logger.info(f"Cleaned response: {response_text[:500]}...")
        
        # Parse JSON
        try:
            spec_dict = json.loads(response_text)
            logger.info("Successfully parsed JSON response")
            logger.info(f"Parsed spec: {json.dumps(spec_dict, indent=2)[:300]}...")
            
            # Convert to Pydantic model
            spec = DiagramSpec(**spec_dict)
            return spec
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.error(f"Failed to parse: {response_text}")
            raise Exception(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            logger.error(f"Failed to create DiagramSpec: {e}")
            raise
    
    def process_assistant_request(self, message: str, context: str = None) -> dict:
        """Process assistant request to understand user intent"""
        logger.info(f"Processing assistant request: {message[:50]}...")
        
        system_prompt = """You are a helpful assistant that specializes in system architecture diagrams.

You can:
1. Answer questions about architecture, diagrams, and system design
2. Generate diagrams when users ask for them
3. Explain how to build specific architectures
4. Ask clarifying questions to better understand requirements

When a user wants a diagram generated, respond with JSON:
{
  "action": "generate_diagram",
  "response": "I'll create that diagram for you.",
  "description": "detailed description for diagram generation"
}

For other conversations, respond with JSON:
{
  "action": "conversation",
  "response": "your helpful response"
}

IMPORTANT: Always respond with ONLY valid JSON without additional text. No newline or control characters in JSON values."""

        context_text = f"\nPrevious context: {context}" if context else ""
        user_prompt = f"User message: {message}{context_text}"
        
        logger.info("Sending assistant request to OpenRouter...")
        
        response = self.client.chat.completions.create(
            model=self.settings.openrouter_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"Assistant response: {response_text[:200]}...")
        
        # Clean response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Remove control characters that break JSON parsing
        import re
        response_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response_text)
        
        try:
            result = json.loads(response_text)
            logger.info(f"Assistant action: {result.get('action')}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse assistant response: {e}")
            logger.error(f"Response text: {repr(response_text)}")
            # Fallback response
            return {
                "action": "conversation",
                "response": "I apologize, but I encountered an error processing your request. Please try again."
            }