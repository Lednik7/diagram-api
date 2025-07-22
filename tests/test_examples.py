"""
Test examples from the technical specification
"""
import requests
import base64
import os

BASE_URL = "http://localhost:8000"
OUTPUT_DIR = "test_outputs"

def setup_output_dir():
    """Create output directory for test images"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def save_image(image_data: str, filename: str):
    """Save base64 image data to file in output directory"""
    setup_output_dir()
    filepath = os.path.join(OUTPUT_DIR, filename)
    image_bytes = base64.b64decode(image_data)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    print(f"Saved image to {filepath}")

def test_example_1():
    """
    Example 1 from TZ:
    Create a diagram showing a basic web application with an Application Load Balancer,
    two EC2 instances for the web servers, and an RDS database for storage. 
    The web servers should be in a cluster named 'Web Tier'.
    """
    description = """Create a diagram showing a basic web application with an Application Load Balancer, 
    two EC2 instances for the web servers, and an RDS database for storage. 
    The web servers should be in a cluster named 'Web Tier'."""
    
    print("Testing Example 1...")
    print(f"Description: {description}")
    
    # Test debug endpoint first
    debug_response = requests.post(f"{BASE_URL}/debug-spec", json={"description": description})
    if debug_response.status_code == 200:
        spec = debug_response.json()["specification"]
        print("Generated specification:")
        import json
        print(json.dumps(spec, indent=2))
    
    # Generate diagram
    response = requests.post(f"{BASE_URL}/generate-diagram", json={"description": description})
    
    if response.status_code == 200:
        data = response.json()
        save_image(data["image_data"], "example1_web_app.png")
        print("✅ Example 1 passed")
        return True
    else:
        print(f"❌ Example 1 failed: {response.status_code} - {response.text}")
        return False

def test_example_2():
    """
    Example 2 from TZ:
    Design a microservices architecture with three services: an authentication service, 
    a payment service, and an order service. Include an API Gateway for routing, 
    an SQS queue for message passing between services, and a shared RDS database. 
    Group the services in a cluster called 'Microservices'. Add CloudWatch for monitoring.
    """
    description = """Design a microservices architecture with three services: an authentication service, 
    a payment service, and an order service. Include an API Gateway for routing, 
    an SQS queue for message passing between services, and a shared RDS database. 
    Group the services in a cluster called 'Microservices'. Add CloudWatch for monitoring."""
    
    print("\nTesting Example 2...")
    print(f"Description: {description}")
    
    # Test debug endpoint first
    debug_response = requests.post(f"{BASE_URL}/debug-spec", json={"description": description})
    if debug_response.status_code == 200:
        spec = debug_response.json()["specification"]
        print("Generated specification:")
        import json
        print(json.dumps(spec, indent=2))
    
    # Generate diagram
    response = requests.post(f"{BASE_URL}/generate-diagram", json={"description": description})
    
    if response.status_code == 200:
        data = response.json()
        save_image(data["image_data"], "example2_microservices.png")
        print("✅ Example 2 passed")
        return True
    else:
        print(f"❌ Example 2 failed: {response.status_code} - {response.text}")
        return False

def test_simple_case():
    """Test simple case"""
    description = "Simple web server with database"
    
    print("\nTesting Simple Case...")
    print(f"Description: {description}")
    
    response = requests.post(f"{BASE_URL}/generate-diagram", json={"description": description})
    
    if response.status_code == 200:
        data = response.json()
        save_image(data["image_data"], "simple_case.png")
        print("✅ Simple case passed")
        return True
    else:
        print(f"❌ Simple case failed: {response.status_code} - {response.text}")
        return False

def test_available_tools():
    """Test that tools endpoint works"""
    print("\nTesting Available Tools...")
    
    response = requests.get(f"{BASE_URL}/tools")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total tools available: {data['total_tools']}")
        print(f"AWS tools: {len(data['by_provider']['aws'])}")
        print(f"GCP tools: {len(data['by_provider']['gcp'])}")  
        print(f"Azure tools: {len(data['by_provider']['azure'])}")
        print("✅ Tools endpoint passed")
        return True
    else:
        print(f"❌ Tools endpoint failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("Running Diagram API Tests")
    print("=" * 50)
    
    # Skip health check - run tests directly
    
    # Run tests
    results = []
    results.append(test_available_tools())
    results.append(test_simple_case())
    results.append(test_example_1())
    results.append(test_example_2())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")
        
    print(f"\nGenerated images in {OUTPUT_DIR}/:")
    if os.path.exists(OUTPUT_DIR):
        images = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
        for img in images:
            print(f"- {img}")
    else:
        print("- No images generated")