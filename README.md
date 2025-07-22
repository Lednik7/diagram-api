# Diagram API

Async, stateless Python API service for creating architecture diagrams using natural language with LLM agents.

## Features

- FastAPI async framework
- UV package management
- Stateless architecture (no database)
- LLM agent with tools for diagrams package
- Docker containerization
- OpenRouter API integration (Claude Sonnet-4)

## Quick Start

### Local Development

1. Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone and setup:
```bash
git clone <repo-url>
cd diagram-api
cp .env.example .env
# Add your OPENROUTER_API_KEY in .env
```

3. Install dependencies and run:
```bash
uv sync
uv run python main.py
```

API available at http://localhost:8000

### Docker

```bash
# Configure .env with your API key
docker-compose up --build
```

## API Endpoints

### POST /generate-diagram
Creates architecture diagram from natural language description.

**Example:**
```bash
curl -X POST http://localhost:8000/generate-diagram \
  -H "Content-Type: application/json" \
  -d '{"description": "Web application with load balancer, two EC2 instances, and RDS database"}'
```

**Response:**
```json
{
  "image_data": "base64_encoded_png_image",
  "message": "Diagram generated successfully"
}
```

### POST /assistant (Bonus)
Interactive assistant for architecture discussions and diagram generation.

**Example:**
```bash
curl -X POST http://localhost:8000/assistant \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help designing a microservices architecture"}'
```

### Other endpoints
- `GET /` - Service info
- `GET /health` - Health check
- `GET /docs` - API documentation

## Web Interface

Optional Gradio web interface for easier interaction:

```bash
# In separate terminal after starting API
uv run python gradio_app.py
```

Open http://localhost:7860 for chat interface with diagram generation.

## Example Inputs/Outputs

### Example 1: Basic Web Application
**Input:** 
```
"Create a diagram showing a basic web application with an Application Load Balancer, two EC2 instances for the web servers, and an RDS database for storage. The web servers should be in a cluster named 'Web Tier'."
```

**Output:** PNG diagram with ALB → EC2 cluster → RDS database

### Example 2: Microservices Architecture  
**Input:**
```
"Design a microservices architecture with three services: an authentication service, a payment service, and an order service. Include an API Gateway for routing, an SQS queue for message passing between services, and a shared RDS database. Group the services in a cluster called 'Microservices'. Add CloudWatch for monitoring."
```

**Output:** PNG diagram with API Gateway → Microservices cluster → SQS → RDS + CloudWatch

## Testing

Run tests:
```bash
uv run python run_tests.py
```

Test API manually:
```bash
# Health check
curl http://localhost:8000/health

# Generate diagram
curl -X POST http://localhost:8000/generate-diagram \
  -H "Content-Type: application/json" \
  -d '{"description": "Simple web app with database"}'
```

## Architecture

### Core Components
- **FastAPI**: Async web framework
- **OpenRouter**: LLM API integration  
- **Diagrams**: Python library for architecture diagrams
- **LLM Agent**: Claude Sonnet-4 with custom tools

### Supported Node Types
- **AWS Components**: EC2, ALB, RDS, S3, API Gateway, SQS, CloudWatch
- **Generic Components**: Web servers, databases, load balancers
- **Microservices**: API gateways, service clusters, message queues

### Agent Tools
Custom tools built around diagrams package:
1. **create_diagram**: Creates new diagram with title
2. **add_cluster**: Groups related components
3. **add_node**: Adds individual components
4. **connect_nodes**: Creates connections between components
5. **render_diagram**: Generates final PNG image

## Requirements

- Python 3.11+
- OpenRouter API key
- Graphviz (for diagram rendering)

## Considerations & Limitations

- **Stateless**: No session storage or database
- **LLM Dependency**: Requires OpenRouter API key
- **Diagram Package**: Uses Python diagrams library as "black box"
- **Supported Architectures**: Primarily AWS components
- **Image Format**: Returns base64 PNG only
- **Rate Limits**: Subject to OpenRouter API limits

## Error Handling

- Invalid inputs return 400 Bad Request
- LLM API errors return 500 with details  
- Temporary files are automatically cleaned up
- Comprehensive logging for debugging

## License

MIT License