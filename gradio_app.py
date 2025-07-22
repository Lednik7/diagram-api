#!/usr/bin/env python3
"""
Gradio web interface for the Diagram API Assistant
"""
import base64
import io
import gradio as gr
import requests
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8000"

class DiagramAssistant:
    def __init__(self):
        self.conversation_history = []
    
    def chat_with_assistant(self, message, history):
        """Chat with the assistant and handle diagram generation"""
        try:
            # Call the assistant endpoint
            response = requests.post(
                f"{API_BASE_URL}/assistant",
                json={"message": message, "context": self._get_context()}
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_response = data["response"]
                
                # Add to conversation history
                self.conversation_history.append(("user", message))
                self.conversation_history.append(("assistant", assistant_response))
                
                # If a diagram was generated, return both text and image
                if data.get("action") == "diagram_generated" and data.get("image_data"):
                    image = self._decode_image(data["image_data"])
                    return assistant_response, image
                else:
                    return assistant_response, None
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return error_msg, None
                
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to the API server. Make sure it's running on http://localhost:8000", None
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"❌ Error: {str(e)}", None
    
    def generate_diagram_direct(self, description):
        """Direct diagram generation"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/generate-diagram",
                json={"description": description}
            )
            
            if response.status_code == 200:
                data = response.json()
                image = self._decode_image(data["image_data"])
                return image, data["message"]
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return None, error_msg
                
        except requests.exceptions.ConnectionError:
            return None, "❌ Cannot connect to the API server. Make sure it's running on http://localhost:8000"
        except Exception as e:
            logger.error(f"Error: {e}")
            return None, f"❌ Error: {str(e)}"
    
    def _decode_image(self, image_data):
        """Decode base64 image data to PIL Image"""
        image_bytes = base64.b64decode(image_data)
        return Image.open(io.BytesIO(image_bytes))
    
    def _get_context(self):
        """Get conversation context for the assistant"""
        if not self.conversation_history:
            return None
        
        # Return last 3 exchanges for context
        recent_history = self.conversation_history[-6:]  # 3 exchanges = 6 messages
        context_parts = []
        for role, msg in recent_history:
            context_parts.append(f"{role}: {msg}")
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return None, None

# Initialize assistant
assistant = DiagramAssistant()

def chat_interface(message, history):
    """Gradio chat interface wrapper"""
    response, image = assistant.chat_with_assistant(message, history)
    
    # Update chat history
    history.append([message, response])
    
    return history, "", image

def direct_diagram_interface(description):
    """Direct diagram generation interface"""
    image, message = assistant.generate_diagram_direct(description)
    return image, message

def clear_conversation():
    """Clear conversation and return empty state"""
    assistant.clear_history()
    return [], None

# Create Gradio interface
with gr.Blocks(title="Diagram API Assistant", theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 20px;">
        <h1>🏗️ Architecture Diagram Assistant</h1>
        <p>Ask me to create system architecture diagrams, or chat about diagram design!</p>
    </div>
    """)
    
    with gr.Tabs():
        # Assistant Chat Tab
        with gr.TabItem("💬 Assistant Chat"):
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        height=400,
                        placeholder="Start chatting with the assistant...",
                        show_label=False
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            placeholder="Ask me to create a diagram or ask questions about architecture...",
                            scale=4,
                            show_label=False
                        )
                        send_btn = gr.Button("Send", variant="primary")
                    
                    clear_btn = gr.Button("Clear Conversation", variant="secondary")
                
                with gr.Column(scale=1):
                    diagram_output = gr.Image(
                        label="Generated Diagram",
                        show_label=True,
                        height=400
                    )
            
            # Chat functionality
            def respond(message, history):
                response, image = assistant.chat_with_assistant(message, history)
                history.append([message, response])
                return history, "", image
            
            msg.submit(respond, [msg, chatbot], [chatbot, msg, diagram_output])
            send_btn.click(respond, [msg, chatbot], [chatbot, msg, diagram_output])
            clear_btn.click(clear_conversation, [], [chatbot, diagram_output])
        
        # Direct Diagram Tab  
        with gr.TabItem("🎨 Direct Diagram Generation"):
            with gr.Row():
                with gr.Column():
                    direct_input = gr.Textbox(
                        label="Diagram Description",
                        placeholder="Describe the architecture you want to create...",
                        lines=3
                    )
                    direct_btn = gr.Button("Generate Diagram", variant="primary")
                    direct_status = gr.Textbox(label="Status", interactive=False)
                
                with gr.Column():
                    direct_output = gr.Image(label="Generated Diagram", height=400)
            
            direct_btn.click(
                direct_diagram_interface,
                inputs=[direct_input],
                outputs=[direct_output, direct_status]
            )
        
        # Examples Tab
        with gr.TabItem("📋 Examples"):
            gr.HTML("""
            <div style="padding: 20px;">
                <h3>Example Requests:</h3>
                <ul>
                    <li><strong>Basic Web App:</strong> "Create a web application with load balancer, web servers, and database"</li>
                    <li><strong>Microservices:</strong> "Design a microservices architecture with API gateway, auth service, and message queue"</li>
                    <li><strong>Questions:</strong> "How should I design a scalable e-commerce architecture?"</li>
                    <li><strong>Explanations:</strong> "Explain the components needed for a high-availability web application"</li>
                </ul>
                
                <h3>Supported Components:</h3>
                <p>AWS: EC2, ALB, RDS, S3, Lambda, API Gateway, SQS, CloudWatch, and more...</p>
                <p>GCP: Compute Engine, GKE, Cloud SQL, Cloud Storage, Cloud Functions...</p>
                <p>Azure: Virtual Machines, AKS, SQL Database, Blob Storage...</p>
            </div>
            """)

def main():
    """Launch the Gradio interface"""
    print("🚀 Starting Diagram Assistant Web Interface...")
    print("🔗 Make sure the API server is running on http://localhost:8000")
    print("📱 Web interface will be available at: http://localhost:7860")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()