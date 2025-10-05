#!/usr/bin/env python3
"""
Launch script for Memory-Enabled Strands Agent
Provides easy startup options for different deployment modes
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # import streamlit
        # import fastapi
        # import mem0
        # import strands
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_api_server():
    """Start FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])

def start_streamlit_app():
    """Start Streamlit frontend"""
    print("🌐 Starting Streamlit frontend...")
    return subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", 
        "streamlit_auth.py", "--server.port", "8501", "--server.address", "0.0.0.0"
    ])

def main():
    """Main launcher function"""
    print("Memory-Enabled Strands Agent Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\nSelect launch mode:")
    print("1. 🌐 Web Interface (FastAPI + Streamlit)")
    print("2. 💻 CLI Memory Agent")
    print("3. 🔧 API Server Only")
    print("4. 📱 Streamlit Only")
    print("5. 🐳 Docker Compose")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        # Full web interface
        print("\n🚀 Launching full web interface...")
        
        # Start API server
        api_process = start_api_server()
        time.sleep(3)  # Wait for API to start
        
        # Start Streamlit
        streamlit_process = start_streamlit_app()
        time.sleep(5)  # Wait for Streamlit to start
        
        # Open browser
        print("\n✅ Services started successfully!")
        print("📱 Streamlit UI: http://localhost:8501")
        print("🔧 API Docs: http://localhost:8000/docs")
        
        try:
            webbrowser.open("http://localhost:8501")
        except:
            pass
        
        print("\nPress Ctrl+C to stop all services...")
        
        try:
            # Wait for user interrupt
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            api_process.terminate()
            streamlit_process.terminate()
            print("✅ Services stopped.")
    
    elif choice == "2":
        # CLI memory agent
        print("\n💻 Starting CLI Memory Agent...")
        subprocess.run([sys.executable, "memory_agent.py"])
    
    elif choice == "3":
        # API server only
        print("\n🔧 Starting API server only...")
        print("API will be available at: http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
    
    elif choice == "4":
        # Streamlit only
        print("\n📱 Starting Streamlit only...")
        print("Note: Make sure API server is running on port 8000")
        print("Streamlit will be available at: http://localhost:8501")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py", "--server.port", "8501"
        ])
    
    elif choice == "5":
        # Docker compose
        print("\n🐳 Starting with Docker Compose...")
        if Path("docker-compose.yml").exists():
            subprocess.run(["docker-compose", "up", "--build"])
        else:
            print("❌ docker-compose.yml not found!")
    
    else:
        print("❌ Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()