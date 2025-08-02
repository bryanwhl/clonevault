#!/usr/bin/env python3
"""
Database Manager for Digital Twin Agent Professional Context
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class User:
    """User profile data"""
    user_id: str
    name: str
    email: str
    phone: str
    linkedin: str
    github: str
    current_role: str
    current_company: str
    location: str
    created_at: str
    updated_at: str


@dataclass
class Education:
    """Education record"""
    education_id: str
    user_id: str
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    gpa: Optional[str]
    honors: Optional[str]
    achievements: Optional[str]


@dataclass
class WorkExperience:
    """Work experience record"""
    experience_id: str
    user_id: str
    company: str
    role: str
    start_date: str
    end_date: Optional[str]
    location: str
    description: str
    key_achievements: str
    technologies: str


@dataclass
class Skill:
    """Technical/professional skill"""
    skill_id: str
    user_id: str
    skill_name: str
    category: str
    proficiency_level: str
    years_experience: int


@dataclass
class Project:
    """Project information"""
    project_id: str
    user_id: str
    project_name: str
    description: str
    technologies: str
    start_date: str
    end_date: Optional[str]
    status: str
    github_url: Optional[str]


@dataclass
class ProfessionalInterest:
    """Professional interests and goals"""
    interest_id: str
    user_id: str
    interest_type: str  # 'technology', 'industry', 'role', 'goal'
    interest_name: str
    description: str
    priority: str  # 'high', 'medium', 'low'


@dataclass
class NetworkingGoal:
    """Networking goals and preferences"""
    goal_id: str
    user_id: str
    goal_type: str  # 'mentor', 'mentee', 'peer', 'industry_expert', 'collaborator'
    description: str
    target_industries: str
    target_roles: str
    preferred_interaction: str  # 'coffee_chat', 'project_collaboration', 'advice_session'


@dataclass
class LinkedInAttribute:
    """LinkedIn profile attributes"""
    attribute_id: str
    user_id: str
    profile_url: str
    headline: str
    summary: str
    location: str
    industry: str
    connections_count: Optional[str]
    posts_count: Optional[str]
    articles_count: Optional[str]
    endorsements: Optional[str]
    recommendations: Optional[str]
    activity_keywords: Optional[str]
    last_updated: str


@dataclass
class ResumeAttribute:
    """Resume document attributes"""
    attribute_id: str
    user_id: str
    resume_file_path: str
    extracted_text: str
    key_achievements: str
    technical_keywords: str
    soft_skills: str
    certifications: str
    languages: str
    publications: str
    awards: str
    volunteer_work: str
    personal_projects: str
    last_updated: str


@dataclass
class ConversationContext:
    """Conversation-specific context and prompt prefix"""
    context_id: str
    user_id: str
    conversation_id: str
    prompt_prefix_path: str
    generated_context: str
    linkedin_summary: str
    resume_summary: str
    created_at: str


class DatabaseManager:
    """Manages the SQLite database for digital twin professional context"""
    
    def __init__(self, db_path: str = "digital_twin.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with schema"""
        with self.get_connection() as conn:
            # Users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    linkedin TEXT,
                    github TEXT,
                    current_role TEXT,
                    current_company TEXT,
                    location TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # Education table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS education (
                    education_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    institution TEXT NOT NULL,
                    degree TEXT NOT NULL,
                    field_of_study TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    gpa TEXT,
                    honors TEXT,
                    achievements TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Work Experience table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS work_experience (
                    experience_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    location TEXT,
                    description TEXT,
                    key_achievements TEXT,
                    technologies TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Skills table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    skill_name TEXT NOT NULL,
                    category TEXT,
                    proficiency_level TEXT,
                    years_experience INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Projects table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    project_name TEXT NOT NULL,
                    description TEXT,
                    technologies TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    status TEXT,
                    github_url TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Professional Interests table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS professional_interests (
                    interest_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    interest_type TEXT,
                    interest_name TEXT,
                    description TEXT,
                    priority TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Networking Goals table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS networking_goals (
                    goal_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    goal_type TEXT,
                    description TEXT,
                    target_industries TEXT,
                    target_roles TEXT,
                    preferred_interaction TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # LinkedIn Attributes table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS linkedin_attributes (
                    attribute_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    profile_url TEXT,
                    headline TEXT,
                    summary TEXT,
                    location TEXT,
                    industry TEXT,
                    connections_count TEXT,
                    posts_count TEXT,
                    articles_count TEXT,
                    endorsements TEXT,
                    recommendations TEXT,
                    activity_keywords TEXT,
                    last_updated TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Resume Attributes table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resume_attributes (
                    attribute_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    resume_file_path TEXT,
                    extracted_text TEXT,
                    key_achievements TEXT,
                    technical_keywords TEXT,
                    soft_skills TEXT,
                    certifications TEXT,
                    languages TEXT,
                    publications TEXT,
                    awards TEXT,
                    volunteer_work TEXT,
                    personal_projects TEXT,
                    last_updated TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Conversation Context table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_contexts (
                    context_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    conversation_id TEXT,
                    prompt_prefix_path TEXT,
                    generated_context TEXT,
                    linkedin_summary TEXT,
                    resume_summary TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
    
    def add_user(self, user: User) -> bool:
        """Add a new user"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user.user_id, user.name, user.email, user.phone, user.linkedin,
                    user.github, user.current_role, user.current_company, user.location,
                    user.created_at, user.updated_at
                ))
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def add_education(self, education: Education) -> bool:
        """Add education record"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO education VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    education.education_id, education.user_id, education.institution,
                    education.degree, education.field_of_study, education.start_date,
                    education.end_date, education.gpa, education.honors, education.achievements
                ))
            return True
        except Exception as e:
            print(f"Error adding education: {e}")
            return False
    
    def add_work_experience(self, experience: WorkExperience) -> bool:
        """Add work experience record"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO work_experience VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    experience.experience_id, experience.user_id, experience.company,
                    experience.role, experience.start_date, experience.end_date,
                    experience.location, experience.description, experience.key_achievements,
                    experience.technologies
                ))
            return True
        except Exception as e:
            print(f"Error adding work experience: {e}")
            return False
    
    def add_skill(self, skill: Skill) -> bool:
        """Add skill record"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO skills VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    skill.skill_id, skill.user_id, skill.skill_name,
                    skill.category, skill.proficiency_level, skill.years_experience
                ))
            return True
        except Exception as e:
            print(f"Error adding skill: {e}")
            return False
    
    def add_project(self, project: Project) -> bool:
        """Add project record"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project.project_id, project.user_id, project.project_name,
                    project.description, project.technologies, project.start_date,
                    project.end_date, project.status, project.github_url
                ))
            return True
        except Exception as e:
            print(f"Error adding project: {e}")
            return False
    
    def add_professional_interest(self, interest: ProfessionalInterest) -> bool:
        """Add professional interest"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO professional_interests VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    interest.interest_id, interest.user_id, interest.interest_type,
                    interest.interest_name, interest.description, interest.priority
                ))
            return True
        except Exception as e:
            print(f"Error adding professional interest: {e}")
            return False
    
    def add_networking_goal(self, goal: NetworkingGoal) -> bool:
        """Add networking goal"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO networking_goals VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal.goal_id, goal.user_id, goal.goal_type, goal.description,
                    goal.target_industries, goal.target_roles, goal.preferred_interaction
                ))
            return True
        except Exception as e:
            print(f"Error adding networking goal: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get complete user profile with all related data"""
        with self.get_connection() as conn:
            # Get user info
            user = conn.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchone()
            
            if not user:
                return {}
            
            # Get education
            education = conn.execute(
                "SELECT * FROM education WHERE user_id = ? ORDER BY start_date DESC", (user_id,)
            ).fetchall()
            
            # Get work experience
            experience = conn.execute(
                "SELECT * FROM work_experience WHERE user_id = ? ORDER BY start_date DESC", (user_id,)
            ).fetchall()
            
            # Get skills
            skills = conn.execute(
                "SELECT * FROM skills WHERE user_id = ? ORDER BY category, skill_name", (user_id,)
            ).fetchall()
            
            # Get projects
            projects = conn.execute(
                "SELECT * FROM projects WHERE user_id = ? ORDER BY start_date DESC", (user_id,)
            ).fetchall()
            
            # Get professional interests
            interests = conn.execute(
                "SELECT * FROM professional_interests WHERE user_id = ? ORDER BY priority DESC", (user_id,)
            ).fetchall()
            
            # Get networking goals
            goals = conn.execute(
                "SELECT * FROM networking_goals WHERE user_id = ?", (user_id,)
            ).fetchall()
            
            return {
                "user": dict(user),
                "education": [dict(row) for row in education],
                "work_experience": [dict(row) for row in experience],
                "skills": [dict(row) for row in skills],
                "projects": [dict(row) for row in projects],
                "professional_interests": [dict(row) for row in interests],
                "networking_goals": [dict(row) for row in goals]
            }
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        with self.get_connection() as conn:
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(user) for user in users]
    
    def add_linkedin_attributes(self, linkedin_attr: LinkedInAttribute) -> bool:
        """Add LinkedIn attributes"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO linkedin_attributes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    linkedin_attr.attribute_id, linkedin_attr.user_id, linkedin_attr.profile_url,
                    linkedin_attr.headline, linkedin_attr.summary, linkedin_attr.location,
                    linkedin_attr.industry, linkedin_attr.connections_count, linkedin_attr.posts_count,
                    linkedin_attr.articles_count, linkedin_attr.endorsements, linkedin_attr.recommendations,
                    linkedin_attr.activity_keywords, linkedin_attr.last_updated
                ))
            return True
        except Exception as e:
            print(f"Error adding LinkedIn attributes: {e}")
            return False
    
    def add_resume_attributes(self, resume_attr: ResumeAttribute) -> bool:
        """Add resume attributes"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO resume_attributes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    resume_attr.attribute_id, resume_attr.user_id, resume_attr.resume_file_path,
                    resume_attr.extracted_text, resume_attr.key_achievements, resume_attr.technical_keywords,
                    resume_attr.soft_skills, resume_attr.certifications, resume_attr.languages,
                    resume_attr.publications, resume_attr.awards, resume_attr.volunteer_work,
                    resume_attr.personal_projects, resume_attr.last_updated
                ))
            return True
        except Exception as e:
            print(f"Error adding resume attributes: {e}")
            return False
    
    def add_conversation_context(self, context: ConversationContext) -> bool:
        """Add conversation context"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO conversation_contexts VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    context.context_id, context.user_id, context.conversation_id,
                    context.prompt_prefix_path, context.generated_context,
                    context.linkedin_summary, context.resume_summary, context.created_at
                ))
            return True
        except Exception as e:
            print(f"Error adding conversation context: {e}")
            return False
    
    def get_linkedin_attributes(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn attributes for a user"""
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM linkedin_attributes WHERE user_id = ?", (user_id,)
            ).fetchone()
            return dict(result) if result else None
    
    def get_resume_attributes(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get resume attributes for a user"""
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM resume_attributes WHERE user_id = ?", (user_id,)
            ).fetchone()
            return dict(result) if result else None
    
    def get_conversation_context(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation context by conversation ID"""
        with self.get_connection() as conn:
            result = conn.execute(
                "SELECT * FROM conversation_contexts WHERE conversation_id = ?", (conversation_id,)
            ).fetchone()
            return dict(result) if result else None
    
    def update_work_experience(self, experience_id: str, role: str = None, description: str = None) -> bool:
        """Update work experience record"""
        try:
            with self.get_connection() as conn:
                updates = []
                params = []
                
                if role is not None:
                    updates.append("role = ?")
                    params.append(role)
                
                if description is not None:
                    updates.append("description = ?")
                    params.append(description)
                
                if not updates:
                    return True  # Nothing to update
                
                params.append(experience_id)
                query = f"UPDATE work_experience SET {', '.join(updates)} WHERE experience_id = ?"
                
                conn.execute(query, params)
            return True
        except Exception as e:
            print(f"Error updating work experience: {e}")
            return False
    
    def update_education(self, education_id: str, field_of_study: str = None, gpa: str = None, honors: str = None) -> bool:
        """Update education record"""
        try:
            with self.get_connection() as conn:
                updates = []
                params = []
                
                if field_of_study is not None:
                    updates.append("field_of_study = ?")
                    params.append(field_of_study)
                
                if gpa is not None:
                    updates.append("gpa = ?")
                    params.append(gpa)
                
                if honors is not None:
                    updates.append("honors = ?")
                    params.append(honors)
                
                if not updates:
                    return True  # Nothing to update
                
                params.append(education_id)
                query = f"UPDATE education SET {', '.join(updates)} WHERE education_id = ?"
                
                conn.execute(query, params)
            return True
        except Exception as e:
            print(f"Error updating education: {e}")
            return False