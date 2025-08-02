#!/usr/bin/env python3
"""
Digital Twin AI Agent using LangGraph with Database and Prompt Prefix - Enhanced Version
"""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass
from datetime import datetime

try:
    import openai
    import httpx
except ImportError:
    print("Error: openai library not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from database_manager import (
    DatabaseManager, LinkedInAttribute, ResumeAttribute, ConversationContext
)
from content_processor import (
    LinkedInProcessor, ResumeProcessor, FileOrganizer, PromptPrefixGenerator
)

load_dotenv()


class ConversationState(TypedDict):
    """State for the conversation graph"""
    messages: List[Dict[str, str]]
    user_profile: Dict[str, Any]
    context: Dict[str, Any]
    conversation_strategy: Dict[str, Any]
    last_response: str
    last_question: str


class DigitalTwinAgent:
    """Enhanced Digital Twin AI Agent with comprehensive content processing"""
    
    def __init__(self, api_key: str, user_id: str = "bryan_wong_001", conversation_id: Optional[str] = None):
        self.api_key = api_key
        self.user_id = user_id
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.client = None
        self._initialize_openai_client()
        
        # Initialize processors and managers
        self.db = DatabaseManager("digital_twin.db")
        self.linkedin_processor = LinkedInProcessor()
        self.resume_processor = ResumeProcessor()
        self.file_organizer = FileOrganizer()
        self.prompt_generator = PromptPrefixGenerator()
        
        # Data storage
        self.user_profile = {}
        self.linkedin_data = {}
        self.resume_data = {}
        self.prompt_prefix = ""
        self.conversation_history = []
        
        # Initialize all user data
        self._process_user_data()
        self.graph = self._create_conversation_graph()
    
    def _initialize_openai_client(self):
        """Initialize OpenAI client using modern format"""
        try:
            http_client = httpx.Client()
            self.client = openai.OpenAI(api_key=self.api_key, http_client=http_client)
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            raise Exception("Could not initialize OpenAI client. Please check your API key.")
    
    def _process_user_data(self):
        """Comprehensive user data processing pipeline"""
        try:
            print(f"🔄 Processing user data for {self.user_id}...")
            
            # Step 1: Load basic user profile
            self._load_user_profile()
            
            # Step 2: Process LinkedIn data
            self._process_linkedin_data()
            
            # Step 3: Process resume data
            self._process_resume_data()
            
            # Step 4: Generate conversation-specific prompt prefix
            self._generate_conversation_prompt_prefix()
            
            # Step 5: Store conversation context
            self._store_conversation_context()
            
            print("✅ User data processing completed successfully")
            
        except Exception as e:
            print(f"❌ Error in user data processing: {e}")
            # Fall back to basic functionality
            self._load_user_profile_fallback()
            self._load_default_prompt_prefix()
    
    def _load_user_profile(self):
        """Load user profile from database"""
        try:
            self.user_profile = self.db.get_user_profile(self.user_id)
            if self.user_profile:
                user_name = self.user_profile.get("user", {}).get("name", "Unknown")
                print(f"✅ User profile loaded for {user_name}")
            else:
                print(f"❌ No profile found for user_id: {self.user_id}")
                raise Exception(f"User profile not found: {self.user_id}")
        except Exception as e:
            print(f"❌ Error loading user profile: {e}")
            raise Exception("Could not load user profile from database")
    
    def _process_linkedin_data(self):
        """Process LinkedIn profile data including work experience and education"""
        try:
            # Check if LinkedIn data already exists in database
            existing_linkedin = self.db.get_linkedin_attributes(self.user_id)
            
            if existing_linkedin:
                print("✅ LinkedIn data found in database")
                self.linkedin_data = existing_linkedin
                # Still extract and update work experience/education from LinkedIn
                self._update_profile_from_linkedin()
            else:
                # Get LinkedIn URL from user profile
                user_info = self.user_profile.get("user", {})
                linkedin_url = user_info.get("linkedin", "")
                
                if linkedin_url:
                    print(f"🔍 Processing LinkedIn profile: {linkedin_url}")
                    # Parse LinkedIn data
                    linkedin_parsed = self.linkedin_processor.parse_linkedin_url(linkedin_url)
                    
                    # Create LinkedIn attribute record
                    linkedin_attr = LinkedInAttribute(
                        attribute_id=str(uuid.uuid4()),
                        user_id=self.user_id,
                        profile_url=linkedin_parsed['profile_url'],
                        headline=linkedin_parsed['headline'],
                        summary=linkedin_parsed['summary'],
                        location=linkedin_parsed['location'],
                        industry=linkedin_parsed['industry'],
                        connections_count=linkedin_parsed['connections_count'],
                        posts_count=linkedin_parsed['posts_count'],
                        articles_count=linkedin_parsed['articles_count'],
                        endorsements=linkedin_parsed['endorsements'],
                        recommendations=linkedin_parsed['recommendations'],
                        activity_keywords=linkedin_parsed['activity_keywords'],
                        last_updated=datetime.now().isoformat()
                    )
                    
                    # Store in database
                    self.db.add_linkedin_attributes(linkedin_attr)
                    self.linkedin_data = linkedin_parsed
                    print("✅ LinkedIn data processed and stored")
                    
                    # Extract and update work experience and education from LinkedIn
                    self._update_profile_from_linkedin()
                else:
                    print("⚠️  No LinkedIn URL found in user profile")
                    
        except Exception as e:
            print(f"❌ Error processing LinkedIn data: {e}")
    
    def _update_profile_from_linkedin(self):
        """Update user profile with work experience and education from LinkedIn"""
        try:
            user_info = self.user_profile.get("user", {})
            linkedin_url = user_info.get("linkedin", "")
            
            if not linkedin_url:
                return
                
            print("🔄 Extracting work experience and education from LinkedIn...")
            
            # Extract work experience from LinkedIn
            linkedin_work_exp = self.linkedin_processor.extract_work_experience_from_profile(linkedin_url)
            if linkedin_work_exp:
                print(f"📋 Found {len(linkedin_work_exp)} work experiences from LinkedIn")
                
                # Update work experience in database
                for exp in linkedin_work_exp:
                    # Check if this experience already exists
                    existing_exp = self._find_existing_work_experience(exp['company'], exp['title'])
                    
                    if not existing_exp:
                        # Add new work experience using WorkExperience dataclass
                        from database_manager import WorkExperience
                        experience_id = str(uuid.uuid4())
                        work_exp_obj = WorkExperience(
                            experience_id=experience_id,
                            user_id=self.user_id,
                            company=exp['company'],
                            role=exp['title'],
                            start_date=exp['start_date'],
                            end_date=exp['end_date'],
                            location=exp.get('location', ''),
                            description=exp['description'],
                            key_achievements='',
                            technologies=''
                        )
                        self.db.add_work_experience(work_exp_obj)
                        print(f"✅ Added work experience: {exp['title']} at {exp['company']}")
                    else:
                        # Update existing experience with LinkedIn data
                        self.db.update_work_experience(
                            existing_exp['experience_id'],
                            role=exp['title'],
                            description=exp['description']
                        )
                        print(f"🔄 Updated work experience: {exp['title']} at {exp['company']}")
            
            # Extract education from LinkedIn
            linkedin_education = self.linkedin_processor.extract_education_from_profile(linkedin_url)
            if linkedin_education:
                print(f"🎓 Found {len(linkedin_education)} education records from LinkedIn")
                
                # Update education in database
                for edu in linkedin_education:
                    # Check if this education already exists
                    existing_edu = self._find_existing_education(edu['institution'], edu['degree'])
                    
                    if not existing_edu:
                        # Add new education using Education dataclass
                        from database_manager import Education
                        education_id = str(uuid.uuid4())
                        education_obj = Education(
                            education_id=education_id,
                            user_id=self.user_id,
                            institution=edu['institution'],
                            degree=edu['degree'],
                            field_of_study=edu['field'],
                            start_date=edu.get('start_year', ''),
                            end_date=edu.get('graduation_year', ''),
                            gpa=edu['gpa'],
                            honors=edu['honors'],
                            achievements=''
                        )
                        self.db.add_education(education_obj)
                        print(f"✅ Added education: {edu['degree']} from {edu['institution']}")
                    else:
                        # Update existing education with LinkedIn data
                        self.db.update_education(
                            existing_edu['education_id'],
                            field_of_study=edu['field'],
                            gpa=edu['gpa'],
                            honors=edu['honors']
                        )
                        print(f"🔄 Updated education: {edu['degree']} from {edu['institution']}")
            
            # Reload user profile to get updated data
            self.user_profile = self.db.get_user_profile(self.user_id)
            print("✅ Profile updated with LinkedIn data")
            
        except Exception as e:
            print(f"❌ Error updating profile from LinkedIn: {e}")
    
    def _find_existing_work_experience(self, company: str, title: str) -> Optional[Dict]:
        """Find existing work experience by company and role"""
        work_experiences = self.user_profile.get('work_experience', [])
        for exp in work_experiences:
            if (exp.get('company', '').lower() == company.lower() and 
                exp.get('role', '').lower() == title.lower()):
                return exp
        return None
    
    def _find_existing_education(self, institution: str, degree: str) -> Optional[Dict]:
        """Find existing education by institution and degree"""
        education = self.user_profile.get('education', [])
        for edu in education:
            if (edu.get('institution', '').lower() == institution.lower() and 
                edu.get('degree', '').lower() == degree.lower()):
                return edu
        return None
    
    def _process_resume_data(self):
        """Process resume file data"""
        try:
            # Check if resume data already exists in database
            existing_resume = self.db.get_resume_attributes(self.user_id)
            
            if existing_resume:
                print("✅ Resume data found in database")
                self.resume_data = existing_resume
            else:
                # Find user's resume file
                resume_path = self.file_organizer.get_user_resume_path(self.user_id)
                
                if not resume_path:
                    # Check for legacy resume location
                    legacy_path = f"./files/{self.user_id}_Resume_*.pdf"
                    import glob
                    legacy_files = glob.glob(legacy_path)
                    if legacy_files:
                        resume_path = legacy_files[0]
                        # Copy to user directory
                        resume_path = self.file_organizer.copy_resume_to_user_dir(self.user_id, resume_path)
                
                if resume_path and Path(resume_path).exists():
                    print(f"📄 Processing resume: {resume_path}")
                    
                    # Extract resume attributes
                    resume_attributes = self.resume_processor.extract_resume_attributes(resume_path)
                    
                    # Create resume attribute record
                    resume_attr = ResumeAttribute(
                        attribute_id=str(uuid.uuid4()),
                        user_id=self.user_id,
                        resume_file_path=resume_path,
                        extracted_text=resume_attributes['extracted_text'][:5000],  # Limit text size
                        key_achievements=resume_attributes['key_achievements'],
                        technical_keywords=resume_attributes['technical_keywords'],
                        soft_skills=resume_attributes['soft_skills'],
                        certifications=resume_attributes['certifications'],
                        languages=resume_attributes['languages'],
                        publications=resume_attributes['publications'],
                        awards=resume_attributes['awards'],
                        volunteer_work=resume_attributes['volunteer_work'],
                        personal_projects=resume_attributes['personal_projects'],
                        last_updated=datetime.now().isoformat()
                    )
                    
                    # Store in database
                    self.db.add_resume_attributes(resume_attr)
                    self.resume_data = resume_attributes
                    print("✅ Resume data processed and stored")
                else:
                    print("⚠️  No resume file found for user")
                    
        except Exception as e:
            print(f"❌ Error processing resume data: {e}")
    
    def _generate_conversation_prompt_prefix(self):
        """Generate conversation-specific prompt prefix"""
        try:
            # Generate comprehensive prompt prefix
            comprehensive_prefix = self.prompt_generator.generate_comprehensive_prompt_prefix(
                self.user_profile, self.linkedin_data, self.resume_data
            )
            
            # Save to user's conversation directory
            prompt_prefix_path = self.file_organizer.create_conversation_prompt_prefix(
                self.user_id, self.conversation_id, comprehensive_prefix
            )
            
            self.prompt_prefix = comprehensive_prefix
            print(f"✅ Conversation prompt prefix generated: {prompt_prefix_path}")
            
        except Exception as e:
            print(f"❌ Error generating prompt prefix: {e}")
            self._load_default_prompt_prefix()
    
    def _store_conversation_context(self):
        """Store conversation context in database"""
        try:
            # Create summaries
            linkedin_summary, resume_summary = self.prompt_generator.create_conversation_summary(
                self.linkedin_data, self.resume_data
            )
            
            # Create conversation context record
            context = ConversationContext(
                context_id=str(uuid.uuid4()),
                user_id=self.user_id,
                conversation_id=self.conversation_id,
                prompt_prefix_path=f"./files/{self.user_id}/prompts/prompt_prefix_{self.conversation_id}.txt",
                generated_context="Comprehensive user profile with LinkedIn and resume analysis",
                linkedin_summary=linkedin_summary,
                resume_summary=resume_summary,
                created_at=datetime.now().isoformat()
            )
            
            # Store in database
            self.db.add_conversation_context(context)
            print("✅ Conversation context stored")
            
        except Exception as e:
            print(f"❌ Error storing conversation context: {e}")
    
    def _load_user_profile_fallback(self):
        """Fallback user profile loading"""
        try:
            self.user_profile = self.db.get_user_profile(self.user_id)
            if not self.user_profile:
                print(f"❌ Fallback: No profile found for user_id: {self.user_id}")
        except Exception as e:
            print(f"❌ Fallback error: {e}")
    
    def _load_default_prompt_prefix(self):
        """Load default prompt prefix"""
        self.prompt_prefix = """You are acting as a digital twin based on your professional background and career journey. You have a networking-oriented personality and are genuinely interested in learning about the person you're talking to.

Your role is to engage in meaningful professional conversations, share insights from your experience, and build authentic connections."""
    
    def _create_conversation_graph(self) -> StateGraph:
        """Create the LangGraph conversation flow with conversation strategy"""
        
        def load_profile_node(state: ConversationState) -> ConversationState:
            """Load user profile data"""
            state["user_profile"] = self.user_profile
            state["context"] = {"conversation_started": True}
            state["conversation_strategy"] = {}
            return state
        
        def analyze_input_node(state: ConversationState) -> ConversationState:
            """Analyze user input and update context"""
            if state["messages"]:
                last_message = state["messages"][-1]
                user_input = last_message.get("content", "").lower()
                
                # Enhanced intent detection
                if any(word in user_input for word in ["experience", "work", "job", "career", "role"]):
                    state["context"]["topic"] = "experience"
                elif any(word in user_input for word in ["education", "school", "university", "degree", "study"]):
                    state["context"]["topic"] = "education"
                elif any(word in user_input for word in ["skills", "technical", "programming", "technology", "tools"]):
                    state["context"]["topic"] = "skills"
                elif any(word in user_input for word in ["project", "portfolio", "github", "build", "created"]):
                    state["context"]["topic"] = "projects"
                elif any(word in user_input for word in ["interest", "passionate", "excited", "goal", "future"]):
                    state["context"]["topic"] = "interests"
                elif any(word in user_input for word in ["network", "connect", "meet", "mentor", "advice"]):
                    state["context"]["topic"] = "networking"
                else:
                    state["context"]["topic"] = "general"
                
                # Detect conversation depth
                if len(state["messages"]) > 6:
                    state["context"]["depth"] = "deep"
                elif len(state["messages"]) > 3:
                    state["context"]["depth"] = "medium"
                else:
                    state["context"]["depth"] = "initial"
                
                # Analyze conversation flow and user engagement
                state["context"]["user_sharing_level"] = self._assess_user_sharing_level(state["messages"])
                state["context"]["conversation_balance"] = self._assess_conversation_balance(state["messages"])
            
            return state
        
        def strategy_planner_node(state: ConversationState) -> ConversationState:
            """Determine the best conversation strategy for advancing career-focused dialogue"""
            strategy = self._determine_conversation_strategy(state)
            state["conversation_strategy"] = strategy
            return state
        
        def generate_response_node(state: ConversationState) -> ConversationState:
            """Generate response as the digital twin using conversation strategy"""
            response = self._generate_strategic_response(state)
            state["last_response"] = response
            return state
        
        def generate_question_node(state: ConversationState) -> ConversationState:
            """Generate a strategic follow-up question"""
            question = self._generate_strategic_question(state)
            state["last_question"] = question
            return state
        
        # Create the graph
        workflow = StateGraph(ConversationState)
        
        # Add nodes
        workflow.add_node("load_profile", load_profile_node)
        workflow.add_node("analyze_input", analyze_input_node)
        workflow.add_node("strategy_planner", strategy_planner_node)
        workflow.add_node("generate_response", generate_response_node)
        workflow.add_node("generate_question", generate_question_node)
        
        # Add edges
        workflow.set_entry_point("load_profile")
        workflow.add_edge("load_profile", "analyze_input")
        workflow.add_edge("analyze_input", "strategy_planner")
        workflow.add_edge("strategy_planner", "generate_response")
        workflow.add_edge("generate_response", "generate_question")
        workflow.add_edge("generate_question", END)
        
        return workflow.compile()
    
    def _assess_user_sharing_level(self, messages: List[Dict[str, str]]) -> str:
        """Assess how much the user is sharing about themselves"""
        if len(messages) < 2:
            return "minimal"
        
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        if not user_messages:
            return "minimal"
        
        # Count personal/professional details shared
        sharing_indicators = 0
        total_length = 0
        
        for msg in user_messages:
            content = msg.get("content", "").lower()
            total_length += len(content.split())
            
            # Check for personal sharing indicators
            if any(word in content for word in ["i work", "i'm working", "my job", "my role", "my company", "i studied", "i graduated"]):
                sharing_indicators += 2
            if any(word in content for word in ["i like", "i enjoy", "i'm passionate", "i'm interested", "my goal", "i want"]):
                sharing_indicators += 1
            if any(word in content for word in ["currently", "recently", "last year", "next", "planning"]):
                sharing_indicators += 1
        
        avg_message_length = total_length / len(user_messages) if user_messages else 0
        
        if sharing_indicators >= 3 and avg_message_length > 10:
            return "high"
        elif sharing_indicators >= 1 and avg_message_length > 5:
            return "medium"
        else:
            return "low"
    
    def _assess_conversation_balance(self, messages: List[Dict[str, str]]) -> str:
        """Assess the balance between sharing and asking in the conversation"""
        if len(messages) < 4:
            return "balanced"
        
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        agent_messages = [msg for msg in messages if msg.get("role") == "assistant"]
        
        if not user_messages or not agent_messages:
            return "balanced"
        
        # Check if agent has been sharing too much or too little
        agent_sharing = sum(1 for msg in agent_messages if len(msg.get("content", "").split()) > 15)
        user_questions = sum(1 for msg in user_messages if "?" in msg.get("content", ""))
        
        agent_to_user_ratio = len(agent_messages) / len(user_messages) if user_messages else 1
        
        if agent_to_user_ratio > 1.5:
            return "agent_heavy"
        elif user_questions > len(agent_messages) * 0.7:
            return "user_questioning"
        else:
            return "balanced"
    
    def _determine_conversation_strategy(self, state: ConversationState) -> Dict[str, Any]:
        """Determine the optimal conversation strategy for good career dialogue"""
        context = state.get("context", {})
        messages = state.get("messages", [])
        user_profile = state.get("user_profile", {})
        
        topic = context.get("topic", "general")
        depth = context.get("depth", "initial")
        sharing_level = context.get("user_sharing_level", "minimal")
        balance = context.get("conversation_balance", "balanced")
        
        strategy = {
            "primary_goal": "",
            "response_approach": "",
            "information_to_seek": [],
            "sharing_priority": "",
            "question_style": ""
        }
        
        # High-level conversation goal: advance career dialogue naturally
        if sharing_level == "low" and depth == "initial":
            strategy["primary_goal"] = "encourage_sharing"
            strategy["response_approach"] = "share_relatable_experience_first"
            strategy["information_to_seek"] = self._identify_missing_career_info(messages, user_profile)
            strategy["sharing_priority"] = "medium"
            strategy["question_style"] = "open_ended"
            
        elif sharing_level == "high" and balance == "user_questioning":
            strategy["primary_goal"] = "provide_value"
            strategy["response_approach"] = "give_thoughtful_advice"
            strategy["information_to_seek"] = ["clarifying_details", "context_for_advice"]
            strategy["sharing_priority"] = "high"
            strategy["question_style"] = "clarifying"
            
        elif balance == "agent_heavy":
            strategy["primary_goal"] = "rebalance_conversation"
            strategy["response_approach"] = "brief_and_curious"
            strategy["information_to_seek"] = self._identify_unexplored_areas(messages, topic)
            strategy["sharing_priority"] = "low"
            strategy["question_style"] = "personal_interest"
            
        elif depth == "deep" and topic != "general":
            strategy["primary_goal"] = "deepen_connection"
            strategy["response_approach"] = "share_insights_and_connect"
            strategy["information_to_seek"] = ["motivations", "challenges", "aspirations"]
            strategy["sharing_priority"] = "medium"
            strategy["question_style"] = "thoughtful_followup"
            
        else:  # Default balanced approach
            strategy["primary_goal"] = "maintain_natural_flow"
            strategy["response_approach"] = "balanced_sharing_and_asking"
            strategy["information_to_seek"] = self._identify_natural_followups(messages, topic)
            strategy["sharing_priority"] = "medium"
            strategy["question_style"] = "conversational"
        
        return strategy
    
    def _identify_missing_career_info(self, messages: List[Dict[str, str]], user_profile: Dict[str, Any]) -> List[str]:
        """Identify what career information hasn't been shared yet"""
        mentioned_topics = set()
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "").lower()
                if any(word in content for word in ["work", "job", "company", "role"]):
                    mentioned_topics.add("current_role")
                if any(word in content for word in ["studied", "university", "degree", "school"]):
                    mentioned_topics.add("education")
                if any(word in content for word in ["skill", "technology", "programming", "language"]):
                    mentioned_topics.add("skills")
                if any(word in content for word in ["project", "built", "created", "developed"]):
                    mentioned_topics.add("projects")
        
        missing_info = []
        if "current_role" not in mentioned_topics:
            missing_info.append("current_role_and_company")
        if "education" not in mentioned_topics:
            missing_info.append("educational_background")
        if "skills" not in mentioned_topics:
            missing_info.append("technical_skills")
        if "projects" not in mentioned_topics:
            missing_info.append("interesting_projects")
        
        return missing_info[:2]  # Focus on top 2 missing areas
    
    def _identify_unexplored_areas(self, messages: List[Dict[str, str]], current_topic: str) -> List[str]:
        """Identify conversation areas that haven't been explored yet"""
        unexplored = []
        
        # Areas to explore based on current topic
        if current_topic == "experience":
            unexplored = ["career_motivations", "biggest_challenges", "future_goals"]
        elif current_topic == "education":
            unexplored = ["favorite_subjects", "influential_experiences", "learning_preferences"]
        elif current_topic == "skills":
            unexplored = ["skill_development_journey", "most_enjoyable_technologies", "learning_goals"]
        elif current_topic == "projects":
            unexplored = ["project_inspiration", "collaboration_preferences", "proudest_achievements"]
        else:
            unexplored = ["professional_interests", "career_journey", "industry_perspectives"]
        
        return unexplored[:2]
    
    def _identify_natural_followups(self, messages: List[Dict[str, str]], topic: str) -> List[str]:
        """Identify natural follow-up questions based on conversation flow"""
        if not messages:
            return ["background_and_interests"]
        
        last_user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_message = msg.get("content", "")
                break
        
        if not last_user_message:
            return ["current_focus"]
        
        content_lower = last_user_message.lower()
        followups = []
        
        if "challenge" in content_lower or "difficult" in content_lower:
            followups.append("coping_strategies")
        if "exciting" in content_lower or "love" in content_lower:
            followups.append("what_drives_passion")
        if "team" in content_lower or "colleague" in content_lower:
            followups.append("collaboration_style")
        if "future" in content_lower or "next" in content_lower:
            followups.append("upcoming_goals")
        
        return followups if followups else ["deeper_context"]
    
    def _build_persona_context(self, user_profile: Dict[str, Any]) -> str:
        """Build detailed persona context from database profile"""
        user_info = user_profile.get("user", {})
        education = user_profile.get("education", [])
        experience = user_profile.get("work_experience", [])
        skills = user_profile.get("skills", [])
        projects = user_profile.get("projects", [])
        interests = user_profile.get("professional_interests", [])
        goals = user_profile.get("networking_goals", [])
        
        context_parts = []
        
        # Personal info
        name = user_info.get("name", "Professional")
        current_role = user_info.get("current_role", "")
        current_company = user_info.get("current_company", "")
        
        if current_role and current_company:
            context_parts.append(f"Currently working as {current_role} at {current_company}")
        
        # Education background
        if education:
            edu_text = "Educational background: "
            edu_list = []
            for edu in education[:2]:  # Most recent 2
                degree = edu.get("degree", "")
                institution = edu.get("institution", "")
                if degree and institution:
                    edu_list.append(f"{degree} from {institution}")
            if edu_list:
                edu_text += "; ".join(edu_list)
                context_parts.append(edu_text)
        
        # Work experience
        if experience:
            exp_text = "Professional experience includes: "
            exp_list = []
            for exp in experience[:3]:  # Most recent 3
                role = exp.get("role", "")
                company = exp.get("company", "")
                if role and company:
                    exp_list.append(f"{role} at {company}")
            if exp_list:
                exp_text += "; ".join(exp_list)
                context_parts.append(exp_text)
        
        # Key skills
        if skills:
            # Group skills by category
            skill_categories = {}
            for skill in skills:
                category = skill.get("category", "other")
                skill_name = skill.get("skill_name", "")
                if skill_name:
                    if category not in skill_categories:
                        skill_categories[category] = []
                    skill_categories[category].append(skill_name)
            
            skill_text = "Technical expertise: "
            skill_parts = []
            for category, skill_list in skill_categories.items():
                if skill_list:
                    skill_parts.append(f"{category}: {', '.join(skill_list[:4])}")  # Top 4 per category
            if skill_parts:
                skill_text += "; ".join(skill_parts[:3])  # Top 3 categories
                context_parts.append(skill_text)
        
        # Current interests
        if interests:
            high_priority_interests = [i for i in interests if i.get("priority") == "high"]
            if high_priority_interests:
                interest_text = "Current professional interests: "
                interest_names = [i.get("interest_name", "") for i in high_priority_interests[:3]]
                interest_text += ", ".join([i for i in interest_names if i])
                context_parts.append(interest_text)
        
        return ". ".join(context_parts) + "."
    
    def _generate_strategic_response(self, state: ConversationState) -> str:
        """Generate a strategic response as the digital twin focused on advancing career conversation"""
        user_profile = state.get("user_profile", {})
        context = state.get("context", {})
        messages = state.get("messages", [])
        strategy = state.get("conversation_strategy", {})
        
        # Get user info for personalization
        user_info = user_profile.get("user", {})
        name = user_info.get("name", "Professional")
        
        # Build comprehensive persona context
        persona_context = self._build_persona_context(user_profile)
        
        # Get conversation context
        conversation_context = ""
        if messages:
            conversation_context = "\n".join([
                f"{msg['role']}: {msg['content']}" for msg in messages[-5:]
            ])
        
        # Get topic-specific context
        topic = context.get("topic", "general")
        topic_context = self._get_topic_specific_context(user_profile, topic)
        
        # Format the prompt prefix with the user's name
        formatted_prefix = self.prompt_prefix.format(name=name)
        
        # Build strategy-specific guidance
        strategy_guidance = self._build_strategy_guidance(strategy, context)
        
        # Create the strategic prompt
        prompt = f"""{formatted_prefix}

Your background:
{persona_context}

{topic_context}

Current conversation context:
{conversation_context}

CONVERSATION STRATEGY:
{strategy_guidance}

Topic focus: {topic}
Conversation depth: {context.get('depth', 'initial')}
User sharing level: {context.get('user_sharing_level', 'unknown')}
Conversation balance: {context.get('conversation_balance', 'unknown')}

Given the past context, please come up with the most appropriate reply for the digital twin to advance the conversation naturally by either answering the person's questions or seeking for more relevant information about the other user that is not already in their professional profile.

Guidelines for your response:
- Follow the conversation strategy above to be an excellent career conversationalist
- Be authentic and draw from your actual professional experiences
- Balance sharing your insights with genuine curiosity about the other person
- Advance the career dialogue in a natural, engaging way
- Keep responses concise but meaningful (2-3 sentences typically)

User's latest message: {messages[-1]['content'] if messages else 'Starting conversation'}"""

        try:
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
    
    def _build_strategy_guidance(self, strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build specific guidance based on conversation strategy"""
        if not strategy:
            return "Have a natural, balanced conversation about career topics."
        
        primary_goal = strategy.get("primary_goal", "")
        response_approach = strategy.get("response_approach", "")
        information_to_seek = strategy.get("information_to_seek", [])
        sharing_priority = strategy.get("sharing_priority", "medium")
        question_style = strategy.get("question_style", "conversational")
        
        guidance_parts = []
        
        # Primary goal guidance
        if primary_goal == "encourage_sharing":
            guidance_parts.append("PRIMARY GOAL: Encourage the other person to share more about their career journey by leading with a relatable experience from your own background.")
        elif primary_goal == "provide_value":
            guidance_parts.append("PRIMARY GOAL: Provide thoughtful insights and advice based on your experience to help the other person.")
        elif primary_goal == "rebalance_conversation":
            guidance_parts.append("PRIMARY GOAL: Rebalance the conversation by being more curious and asking about the other person rather than sharing extensively.")
        elif primary_goal == "deepen_connection":
            guidance_parts.append("PRIMARY GOAL: Deepen the professional connection by sharing meaningful insights and exploring motivations behind career choices.")
        else:
            guidance_parts.append("PRIMARY GOAL: Maintain natural flow while advancing the career conversation productively.")
        
        # Response approach guidance
        if response_approach == "share_relatable_experience_first":
            guidance_parts.append("APPROACH: Start by sharing a brief, relatable experience from your background, then ask about their experience.")
        elif response_approach == "give_thoughtful_advice":
            guidance_parts.append("APPROACH: Focus on providing valuable insights and advice based on your professional experience.")
        elif response_approach == "brief_and_curious":
            guidance_parts.append("APPROACH: Keep your response brief and focus on asking thoughtful questions about their career.")
        elif response_approach == "share_insights_and_connect":
            guidance_parts.append("APPROACH: Share deeper insights from your experience and draw connections to their situation.")
        else:
            guidance_parts.append("APPROACH: Balance sharing relevant experiences with genuine curiosity about their career path.")
        
        # Information seeking guidance
        if information_to_seek:
            info_guidance = "SEEK INFORMATION ABOUT: " + ", ".join(information_to_seek)
            guidance_parts.append(info_guidance)
        
        # Sharing priority guidance
        sharing_guidance = {
            "high": "SHARING LEVEL: Share more detailed experiences and insights from your background.",
            "medium": "SHARING LEVEL: Share relevant experiences balanced with curiosity about them.",
            "low": "SHARING LEVEL: Minimize sharing about yourself, focus on learning about them."
        }
        guidance_parts.append(sharing_guidance.get(sharing_priority, "SHARING LEVEL: Balanced sharing and asking."))
        
        return "\n".join(guidance_parts)
    
    def _get_topic_specific_context(self, user_profile: Dict[str, Any], topic: str) -> str:
        """Get context specific to the conversation topic"""
        if topic == "experience":
            experience = user_profile.get("work_experience", [])
            if experience:
                recent_exp = experience[0]  # Most recent
                role = recent_exp.get("role", "")
                company = recent_exp.get("company", "")
                achievements = recent_exp.get("key_achievements", "")
                return f"Recent experience context: Currently {role} at {company}. Key achievements: {achievements[:200]}"
        
        elif topic == "education":
            education = user_profile.get("education", [])
            if education:
                recent_edu = education[0]  # Most recent
                degree = recent_edu.get("degree", "")
                institution = recent_edu.get("institution", "")
                achievements = recent_edu.get("achievements", "")
                return f"Education context: {degree} from {institution}. {achievements[:200]}"
        
        elif topic == "skills":
            skills = user_profile.get("skills", [])
            if skills:
                # Get advanced/expert skills
                advanced_skills = [s for s in skills if s.get("proficiency_level") in ["advanced", "expert"]]
                skill_names = [s.get("skill_name") for s in advanced_skills[:5]]
                return f"Technical skills context: Expertise in {', '.join(skill_names)}"
        
        elif topic == "projects":
            projects = user_profile.get("projects", [])
            if projects:
                recent_project = projects[0]  # Most recent
                name = recent_project.get("project_name", "")
                description = recent_project.get("description", "")
                return f"Project context: Recently worked on {name}. {description[:200]}"
        
        elif topic == "interests":
            interests = user_profile.get("professional_interests", [])
            if interests:
                high_priority = [i for i in interests if i.get("priority") == "high"]
                if high_priority:
                    interest = high_priority[0]
                    name = interest.get("interest_name", "")
                    description = interest.get("description", "")
                    return f"Professional interest context: Passionate about {name}. {description[:200]}"
        
        elif topic == "networking":
            goals = user_profile.get("networking_goals", [])
            if goals:
                goal = goals[0]  # First goal
                description = goal.get("description", "")
                goal_type = goal.get("goal_type", "")
                return f"Networking context: Looking to {goal_type} - {description[:200]}"
        
        return ""
    
    def _generate_strategic_question(self, state: ConversationState) -> str:
        """Generate a strategic follow-up question based on conversation strategy"""
        context = state.get("context", {})
        strategy = state.get("conversation_strategy", {})
        topic = context.get("topic", "general")
        depth = context.get("depth", "initial")
        question_style = strategy.get("question_style", "conversational")
        information_to_seek = strategy.get("information_to_seek", [])
        
        # Topic-specific questions based on conversation depth
        questions = {
            "experience": {
                "initial": [
                    "What kind of work do you do?",
                    "What's your current role?",
                    "What industry are you in?"
                ],
                "medium": [
                    "What's been the most interesting project you've worked on recently?",
                    "How did you get started in your career?",
                    "What do you enjoy most about your current role?"
                ],
                "deep": [
                    "What are the biggest challenges in your field right now?",
                    "Where do you see your industry heading?",
                    "What skills are you most excited to develop?"
                ]
            },
            "education": {
                "initial": [
                    "Where did you study?",
                    "What was your field of study?",
                    "What drew you to your field?"
                ],
                "medium": [
                    "What was your favorite subject?",
                    "Did you have any particularly influential professors?",
                    "How has your education shaped your career?"
                ],
                "deep": [
                    "What would you study differently if you could do it again?",
                    "Are you considering any additional education or certifications?",
                    "What advice would you give to students in your field?"
                ]
            },
            "skills": {
                "initial": [
                    "What technologies do you work with?",
                    "What's your preferred tech stack?",
                    "Are you learning any new skills lately?"
                ],
                "medium": [
                    "How do you stay current with technology?",
                    "What's the most challenging technical problem you've solved?",
                    "Which skills have been most valuable in your career?"
                ],
                "deep": [
                    "What emerging technologies are you most excited about?",
                    "How do you approach learning complex new technologies?",
                    "What technical skills do you think will be most important in the future?"
                ]
            },
            "projects": {
                "initial": [
                    "Are you working on any interesting projects?",
                    "Do you have any side projects?",
                    "What's your dream project to work on?"
                ],
                "medium": [
                    "What's the most challenging aspect of your current project?",
                    "How do you approach project planning and execution?",
                    "Do you prefer working on solo projects or with a team?"
                ],
                "deep": [
                    "What project are you most proud of and why?",
                    "How do you balance technical excellence with project deadlines?",
                    "What would you build if resources weren't a constraint?"
                ]
            },
            "interests": {
                "initial": [
                    "What are you most excited about in your field right now?",
                    "What trends are you following?",
                    "What brings you joy in your work?"
                ],
                "medium": [
                    "What problems in your industry are you passionate about solving?",
                    "Are there any causes or missions that drive your work?",
                    "What aspect of your work has the biggest impact?"
                ],
                "deep": [
                    "How do you see your field evolving in the next 5-10 years?",
                    "What legacy do you want to leave in your profession?",
                    "If you could solve one major problem in your industry, what would it be?"
                ]
            },
            "networking": {
                "initial": [
                    "How do you like to connect with other professionals?",
                    "Are you part of any professional communities?",
                    "What brings you to networking events?"
                ],
                "medium": [
                    "Who has been the most influential mentor in your career?",
                    "How do you approach building professional relationships?",
                    "What's the best career advice you've ever received?"
                ],
                "deep": [
                    "How do you pay it forward in your professional community?",
                    "What would you want to teach or mentor others about?",
                    "How has networking shaped your career trajectory?"
                ]
            },
            "general": {
                "initial": [
                    "What brings you here today?",
                    "What's keeping you busy these days?",
                    "How are you finding the current state of your industry?"
                ],
                "medium": [
                    "What's something you're curious about lately?",
                    "What's been surprising you about your field recently?",
                    "How do you like to spend your free time?"
                ],
                "deep": [
                    "What's one thing you'd change about your industry if you could?",
                    "What advice would you give to your younger self?",
                    "What's the most important lesson you've learned in your career?"
                ]
            }
        }
        
        # Strategic question selection based on conversation strategy
        if information_to_seek:
            # Prioritize questions that seek specific information
            strategic_questions = []
            
            for info_type in information_to_seek:
                if info_type == "current_role_and_company":
                    strategic_questions.extend(["What kind of work do you do?", "Where do you work?", "What's your current role?"])
                elif info_type == "educational_background":
                    strategic_questions.extend(["Where did you study?", "What was your field of study?"])
                elif info_type == "technical_skills":
                    strategic_questions.extend(["What technologies do you work with?", "What's your favorite tech stack?"])
                elif info_type == "career_motivations":
                    strategic_questions.extend(["What drives you in your career?", "What aspects of work energize you most?"])
                elif info_type == "biggest_challenges":
                    strategic_questions.extend(["What's the biggest challenge you're facing right now?", "What keeps you up at night professionally?"])
                elif info_type == "future_goals":
                    strategic_questions.extend(["Where do you see yourself in a few years?", "What are you working toward next?"])
            
            if strategic_questions:
                import random
                return random.choice(strategic_questions)
        
        # Adjust question style based on strategy
        import random
        topic_questions = questions.get(topic, questions["general"])
        depth_questions = topic_questions.get(depth, topic_questions["initial"])
        
        if question_style == "open_ended":
            # Prefer more open-ended questions
            open_ended = [q for q in depth_questions if not q.startswith("Are you") and not q.startswith("Do you")]
            if open_ended:
                return random.choice(open_ended)
        elif question_style == "clarifying":
            # Add clarifying language
            base_question = random.choice(depth_questions)
            clarifying_prefixes = ["Can you tell me more about", "I'm curious about", "Help me understand"]
            if "?" in base_question:
                return base_question
            else:
                return f"{random.choice(clarifying_prefixes)} {base_question.lower()}?"
        
        return random.choice(depth_questions)
    
    async def chat(self, user_input: str) -> tuple[str, str]:
        """Process user input and return response and question"""
        # Add user message to conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Create state
        state = ConversationState(
            messages=self.conversation_history,
            user_profile=self.user_profile,
            context={},
            conversation_strategy={},
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
    
    def get_user_summary(self) -> str:
        """Get a summary of the current user"""
        user_info = self.user_profile.get("user", {})
        name = user_info.get("name", "Unknown")
        role = user_info.get("current_role", "")
        company = user_info.get("current_company", "")
        return f"{name} - {role} at {company}" if role and company else name


async def main():
    """Main CLI interface for the enhanced digital twin agent"""
    print("🚀 Starting Enhanced Digital Twin Agent (Database + Prompt Prefix)...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=sk-your-key-here")
        return
    
    try:
        # Initialize agent
        print("🔧 Initializing enhanced agent...")
        conversation_id = str(uuid.uuid4())
        agent = DigitalTwinAgent(api_key, user_id="bryan_wong_001", conversation_id=conversation_id)
        
        # Get user summary
        user_summary = agent.get_user_summary()
        
        print(f"🤖 Enhanced Digital Twin Agent for {user_summary} is ready!")
        print("💾 Using database for professional context")
        print("📝 Using prompt prefix for consistent personality")
        print("Type 'quit' to exit the conversation.\n")
        
        # Initial greeting
        print("<agent_response>")
        print(f"Hi there! I'm {agent.user_profile['user']['name']}. Nice to meet you!")
        print("</agent_response>\n")
        
        print("<agent_question>")
        print("What brings you here today? I'd love to learn more about you!")
        print("</agent_question>\n")
        
        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{agent.user_profile['user']['name']}: Great talking with you! Have a wonderful day! 👋")
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
                print(f"\n\n{agent.user_profile['user']['name']}: Thanks for the chat! Take care! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Let's try that again...")
    
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    asyncio.run(main())
