#!/usr/bin/env python3
"""
Setup script for the Digital Twin Agent
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from .env.example")
            print("Please edit .env file and add your OpenAI API key")
            import shutil
            shutil.copy(env_example, env_file)
        else:
            print("❌ No .env file found. Please create one with OPENAI_API_KEY")
        return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_openai_api_key_here" in content:
            print("⚠️  Please update .env file with your actual OpenAI API key")
            return False
    
    print("✅ Environment file configured")
    return True


def check_resume_file():
    """Check if resume file exists"""
    resume_path = Path("./files/BryanWong_Resume_20250710.pdf")
    if resume_path.exists():
        print("✅ Resume file found")
        return True
    else:
        print(f"❌ Resume file not found at {resume_path}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Digital Twin Agent...")
    print()
    
    success = True
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Check environment
    if not check_env_file():
        success = False
    
    # Check resume file
    if not check_resume_file():
        success = False
    
    print()
    if success:
        print("🎉 Setup completed successfully!")
        print("Run 'python digital_twin_agent.py' to start the agent")
    else:
        print("❌ Setup incomplete. Please fix the issues above and try again.")
    
    return success


if __name__ == "__main__":
    main()