#!/usr/bin/env python3
"""
Digital Twin AI Agent using LangGraph and MCP - Simplified Version
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass

try:
    import openai
    import httpx
except ImportError:
    print("Error: openai library not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

load_dotenv()


class ConversationState(TypedDict):
    """State for the conversation graph"""
    messages: List[Dict[str, str]]
    resume_data: Dict[str, Any]
    context: Dict[str, Any]
    last_response: str
    last_question: str


@dataclass
class MCPClient:
    """Simple MCP client for communicating with the resume parser server"""
    
    def __init__(self):
        self.resume_data = {}
    
    async def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume using the MCP server functionality"""
        try:
            # Import and use the resume parser directly
            from mcp_server import ResumeParserServer
            
            server = ResumeParserServer()
            
            # Extract text and parse
            text = server._extract_text_from_pdf(file_path)
            self.resume_data = server._parse_resume_text(text)
            
            return self.resume_data
        except Exception as e:
            print(f"Error parsing resume: {e}")
            return {}
    
    def get_resume_section(self, section: str) -> Any:
        """Get a specific section from the parsed resume"""
        return self.resume_data.get(section, [])


class DigitalTwinAgent:
    """Digital Twin AI Agent that emulates a person based on their resume"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self._initialize_openai_client()
        self.mcp_client = MCPClient()
        self.resume_data = {}
        self.conversation_history = []
        self.graph = self._create_conversation_graph()
    
    def _initialize_openai_client(self):
        """Initialize OpenAI client using modern format"""
        try:
            # Use modern OpenAI client format (v1.0+) with custom http client to avoid proxies issue
            http_client = httpx.Client()
            self.client = openai.OpenAI(api_key=self.api_key, http_client=http_client)
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            raise Exception("Could not initialize OpenAI client. Please check your API key.")
    
    def _create_conversation_graph(self) -> StateGraph:
        """Create the LangGraph conversation flow"""
        
        def load_resume_node(state: ConversationState) -> ConversationState:
            """Load and parse resume data"""
            state["resume_data"] = self.resume_data
            state["context"] = {"conversation_started": True}
            return state
        
        def analyze_input_node(state: ConversationState) -> ConversationState:
            """Analyze user input and update context"""
            if state["messages"]:
                last_message = state["messages"][-1]
                # Simple intent detection
                user_input = last_message.get("content", "").lower()
                
                if any(word in user_input for word in ["experience", "work", "job", "career"]):
                    state["context"]["topic"] = "experience"
                elif any(word in user_input for word in ["education", "school", "university", "degree"]):
                    state["context"]["topic"] = "education"
                elif any(word in user_input for word in ["skills", "technical", "programming", "technology"]):
                    state["context"]["topic"] = "skills"
                elif any(word in user_input for word in ["project", "portfolio", "github"]):
                    state["context"]["topic"] = "projects"
                else:
                    state["context"]["topic"] = "general"
            
            return state
        
        def generate_response_node(state: ConversationState) -> ConversationState:
            """Generate response as the digital twin"""
            response = self._generate_response(state)
            state["last_response"] = response
            return state
        
        def generate_question_node(state: ConversationState) -> ConversationState:
            """Generate a follow-up question"""
            question = self._generate_question(state)
            state["last_question"] = question
            return state
        
        # Create the graph
        workflow = StateGraph(ConversationState)
        
        # Add nodes
        workflow.add_node("load_resume", load_resume_node)
        workflow.add_node("analyze_input", analyze_input_node)
        workflow.add_node("generate_response", generate_response_node)
        workflow.add_node("generate_question", generate_question_node)
        
        # Add edges
        workflow.set_entry_point("load_resume")
        workflow.add_edge("load_resume", "analyze_input")
        workflow.add_edge("analyze_input", "generate_response")
        workflow.add_edge("generate_response", "generate_question")
        workflow.add_edge("generate_question", END)
        
        return workflow.compile()
    
    async def load_resume(self, file_path: str) -> bool:
        """Load and parse the resume"""
        try:
            self.resume_data = await self.mcp_client.parse_resume(file_path)
            return bool(self.resume_data)
        except Exception as e:
            print(f"Error loading resume: {e}")
            return False
    
    def _generate_response(self, state: ConversationState) -> str:
        """Generate a response as the digital twin using OpenAI"""
        resume_data = state.get("resume_data", {})
        context = state.get("context", {})
        messages = state.get("messages", [])
        
        # Build persona from resume
        persona = self._build_persona(resume_data)
        
        # Get conversation context
        conversation_context = ""
        if messages:
            conversation_context = "\n".join([
                f"{msg['role']}: {msg['content']}" for msg in messages[-5:]  # Last 5 messages
            ])
        
        # Create the prompt
        prompt = f"""You are {persona['name']}, acting as a digital twin based on your resume. You have a networking-oriented personality and are genuinely interested in learning about the person you're talking to.

Your background:
{persona['background']}

Current conversation context:
{conversation_context}

Topic focus: {context.get('topic', 'general')}

Respond as {persona['name']} would, drawing from your professional experience and maintaining an engaging, curious personality. Keep responses concise but personal.

User's latest message: {messages[-1]['content'] if messages else 'Starting conversation'}"""

        try:
            # Use modern OpenAI client format (v1.0+)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {e}")
            return f"I'm having trouble processing that right now. Could you tell me a bit about yourself?"
    
    def _generate_question(self, state: ConversationState) -> str:
        """Generate a follow-up question to learn about the conversation partner"""
        context = state.get("context", {})
        topic = context.get("topic", "general")
        
        # Topic-specific questions
        questions = {
            "experience": [
                "What kind of work do you do?",
                "What's been the most interesting project you've worked on recently?",
                "How did you get started in your career?",
                "What industry are you in?"
            ],
            "education": [
                "Where did you study?",
                "What was your favorite subject in school?",
                "Did you enjoy your university experience?",
                "What drew you to your field of study?"
            ],
            "skills": [
                "What technologies do you enjoy working with?",
                "Are you learning any new skills lately?",
                "What's your preferred programming language?",
                "How do you like to stay current with technology?"
            ],
            "projects": [
                "Are you working on any interesting projects?",
                "Do you have any side projects you're passionate about?",
                "What's your dream project to work on?",
                "Do you contribute to open source?"
            ],
            "general": [
                "What brings you joy in your work?",
                "What are you most excited about these days?",
                "How do you like to spend your free time?",
                "What's something you're curious about?"
            ]
        }
        
        import random
        return random.choice(questions.get(topic, questions["general"]))
    
    def _build_persona(self, resume_data: Dict[str, Any]) -> Dict[str, str]:
        """Build persona information from resume data"""
        personal_info = resume_data.get("personal_info", {})
        experience = resume_data.get("experience", [])
        education = resume_data.get("education", [])
        skills = resume_data.get("skills", [])
        
        name = personal_info.get("name", "the person")
        
        # Build background summary
        background_parts = []
        
        if experience:
            exp_summary = f"Professional experience includes: " + "; ".join([
                exp.get("title", "Unknown role") for exp in experience[:3]
            ])
            background_parts.append(exp_summary)
        
        if education:
            edu_summary = f"Education: " + "; ".join([
                edu.get("institution", "Educational institution") for edu in education
            ])
            background_parts.append(edu_summary)
        
        if skills:
            skills_summary = f"Technical skills: {', '.join(skills[:5])}"
            background_parts.append(skills_summary)
        
        background = ". ".join(background_parts) if background_parts else "Professional background available."
        
        return {
            "name": name,
            "background": background
        }
    
    async def chat(self, user_input: str) -> tuple[str, str]:
        """Process user input and return response and question"""
        # Add user message to conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create state
        state = ConversationState(
            messages=self.conversation_history,
            resume_data=self.resume_data,
            context={},
            last_response="",
            last_question=""
        )
        
        # Run the graph
        result = await self.graph.ainvoke(state)
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant", 
            "content": result["last_response"]
        })
        
        return result["last_response"], result["last_question"]


async def main():
    """Main CLI interface for the digital twin agent"""
    print("🚀 Starting Digital Twin Agent...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=sk-your-key-here")
        return
    
    try:
        # Initialize agent
        print("🔧 Initializing agent...")
        agent = DigitalTwinAgent(api_key)
        
        # Load resume
        resume_path = "./files/BryanWong_Resume_20250710.pdf"
        print(f"📄 Loading resume from {resume_path}...")
        if not await agent.load_resume(resume_path):
            print(f"❌ Error: Could not load resume from {resume_path}")
            return
        
        # Get persona info
        persona = agent._build_persona(agent.resume_data)
        
        print(f"🤖 Digital Twin Agent for {persona['name']} is ready!")
        print("Type 'quit' to exit the conversation.\n")
        
        # Initial greeting
        print("<agent_response>")
        print(f"Hi there! I'm {persona['name']}. Nice to meet you!")
        print("</agent_response>\n")
        
        print("<agent_question>")
        print("What brings you here today? I'd love to learn more about you!")
        print("</agent_question>\n")
        
        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{persona['name']}: Great talking with you! Have a wonderful day! 👋")
                    break
                
                if not user_input:
                    continue
                
                # Get response from agent
                print("🤔 Thinking...")
                response, question = await agent.chat(user_input)
                
                print(f"\n<agent_response>")
                print(response)
                print("</agent_response>\n")
                
                print("<agent_question>")
                print(question)
                print("</agent_question>\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{persona['name']}: Thanks for the chat! Take care! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Let's try that again...")
    
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    asyncio.run(main())