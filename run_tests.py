#!/usr/bin/env python3
"""
Quick test runner for the Diagram API
"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting Diagram API Tests")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run this from the diagram-api directory")
        sys.exit(1)
    
    # Install test dependencies
    print("📦 Installing test dependencies...")
    subprocess.run(["uv", "add", "--dev", "requests"], check=True)
    
    # Run the tests
    print("🧪 Running tests...")
    subprocess.run([sys.executable, "tests/test_examples.py"], check=True)

if __name__ == "__main__":
    main()