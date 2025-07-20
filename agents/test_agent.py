#!/usr/bin/env python3
"""
Test script for the Digital Twin Agent
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""
    print("🧪 Testing OpenAI connection...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say hello!"}]
        )
        
        print("✅ OpenAI connection successful")
        print(f"Test response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def test_resume_parsing():
    """Test resume parsing"""
    print("\n📄 Testing resume parsing...")
    
    try:
        from mcp_server import ResumeParserServer
        
        server = ResumeParserServer()
        resume_path = "./files/BryanWong_Resume_20250710.pdf"
        
        if not os.path.exists(resume_path):
            print(f"❌ Resume file not found: {resume_path}")
            return False
        
        text = server._extract_text_from_pdf(resume_path)
        resume_data = server._parse_resume_text(text)
        
        if resume_data and resume_data.get("personal_info", {}).get("name"):
            print(f"✅ Resume parsing successful")
            print(f"Parsed name: {resume_data['personal_info']['name']}")
            print(f"Experience entries: {len(resume_data.get('experience', []))}")
            print(f"Education entries: {len(resume_data.get('education', []))}")
            print(f"Skills: {len(resume_data.get('skills', []))}")
            return True
        else:
            print("❌ Resume parsing failed - no data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Resume parsing failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from digital_twin_agent_simple import DigitalTwinAgent
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found")
            return False
        
        agent = DigitalTwinAgent(api_key)
        print("✅ Agent initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Digital Twin Agent Tests...\n")
    
    tests = [
        test_openai_connection,
        test_resume_parsing,
        test_agent_initialization
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The agent should work correctly.")
        print("\nRun: python digital_twin_agent_simple.py")
    else:
        print("❌ Some tests failed. Please fix the issues before running the agent.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())