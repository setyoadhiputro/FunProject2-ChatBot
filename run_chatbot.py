#!/usr/bin/env python3
"""
Simple launcher for the AI Chatbot application.
This script starts the Streamlit app with optimal settings.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit chatbot application."""
    print("🤖 Starting AI Chatbot with OpenRouter...")
    print("📱 The app will open in your default browser")
    print("🔑 Don't forget to add your OpenRouter API key in the sidebar!")
    print("-" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            "streamlit", "run", "chatbot_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running the application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using AI Chatbot! Goodbye!")
        sys.exit(0)
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install requirements first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()