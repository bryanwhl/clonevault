#!/usr/bin/env python3
"""
Initialize database with mock data including Bryan Wong's profile
"""

import uuid
from datetime import datetime
from database_manager import (
    DatabaseManager, User, Education, WorkExperience, Skill, 
    Project, ProfessionalInterest, NetworkingGoal
)


def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def get_current_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().isoformat()


def init_bryan_wong_profile(db: DatabaseManager):
    """Initialize Bryan Wong's profile based on his resume"""
    user_id = "bryan_wong_001"
    
    # User profile
    user = User(
        user_id=user_id,
        name="Bryan Wong",
        email="bryanwhl1999@gmail.com",
        phone="+65 9385 8356",
        linkedin="linkedin.com/in/bryan-wong-91b323156",
        github="bryanwhl",
        current_role="Backend Software Engineer",
        current_company="ByteDance (Singapore)",
        location="Singapore",
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp()
    )
    db.add_user(user)
    
    # Education
    education_bachelor = Education(
        education_id=generate_id(),
        user_id=user_id,
        institution="National University of Singapore (NUS)",
        degree="Bachelor of Engineering in Computer Engineering (with Honours)",
        field_of_study="Computer Engineering",
        start_date="2020-08",
        end_date="2023-05",
        gpa="4.51/5.00",
        honors="First Class Honours (Highest Distinction)",
        achievements="Engineering Scholars Programme scholarship, NUS Overseas College Silicon Valley Programme"
    )
    db.add_education(education_bachelor)
    
    education_master = Education(
        education_id=generate_id(),
        user_id=user_id,
        institution="National University of Singapore (NUS)",
        degree="Master of Science in Data Science & Machine Learning",
        field_of_study="Data Science & Machine Learning",
        start_date="2023-08",
        end_date="2024-12",
        gpa=None,
        honors=None,
        achievements="MSc programme sponsored by Engineering Scholars Programme Scholarship"
    )
    db.add_education(education_master)
    
    # Work Experience
    bytedance_exp = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="ByteDance (Singapore)",
        role="Backend Software Engineer",
        start_date="2024-12",
        end_date=None,
        location="Singapore",
        description="Machine Learning Platform team, building AI/ML infrastructure for TikTok's Ads, Recommendation & Search teams",
        key_achievements="Built RAG system with vector retrieval and DeepSeek API; Built parallelized data pipeline for >10000 codebases; Developed Web-based IDE in Golang with DAU of 800 Algorithm Engineers",
        technologies="PyTorch, Tensorflow, Golang, Vector Databases, RAG, DeepSeek API"
    )
    db.add_work_experience(bytedance_exp)
    
    alphalab_exp = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="AlphaLab Capital (Singapore)",
        role="Algo Developer",
        start_date="2023-05",
        end_date="2024-12",
        location="Singapore",
        description="High-frequency quantitative trading team developing trading infrastructure and algorithms",
        key_achievements="Developed sub-millisecond latency trading algorithms; Built big data pipeline for ML model fitting; Set up AWS trading infrastructure",
        technologies="Python, C++, C#, .NET, AWS, Pandas, Google BigQuery, Terraform, Ansible"
    )
    db.add_work_experience(alphalab_exp)
    
    rinse_exp = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="Rinse, Inc.",
        role="Software Engineer Intern",
        start_date="2022-01",
        end_date="2023-05",
        location="San Francisco, CA",
        description="Full-stack software engineer at logistics tech startup providing laundry delivery services",
        key_achievements="Created delivery rider onboarding tool increasing conversion by 31%; Developed new customer mobile app used by thousands; Built Backend APIs for website and mobile apps",
        technologies="Python, Django, Celery, TypeScript, React Native, Mobile Development"
    )
    db.add_work_experience(rinse_exp)
    
    protoslabs_exp = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="ProtosLabs (Singapore)",
        role="Software Engineer Intern",
        start_date="2021-08",
        end_date="2021-12",
        location="Singapore",
        description="Cybersecurity startup with Cyber Risk Management and InsurTech products",
        key_achievements="Developed frontend UI with React and Redux; Created Python microservices with AWS Lambda; Built ML pipeline for cyber attack prediction",
        technologies="React, Redux, Python, AWS Lambda, AWS Amplify, Machine Learning"
    )
    db.add_work_experience(protoslabs_exp)
    
    dso_exp = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="DSO National Laboratories",
        role="Software Engineer Intern",
        start_date="2021-05",
        end_date="2021-08",
        location="Singapore",
        description="Government research lab focusing on defense technology",
        key_achievements="Built Search Engine with Vue.js and Elasticsearch; Developed dockerized transcription microservice; Created monitoring tool with Prometheus and Grafana",
        technologies="Vue.js, Java, Elasticsearch, Docker, Prometheus, Grafana"
    )
    db.add_work_experience(dso_exp)
    
    # Skills
    programming_skills = [
        ("Python", "programming", "expert", 5),
        ("C++", "programming", "advanced", 4),
        ("C#", "programming", "advanced", 3),
        ("TypeScript", "programming", "advanced", 4),
        ("JavaScript", "programming", "advanced", 4),
        ("SQL", "database", "advanced", 4),
        ("Java", "programming", "intermediate", 3),
        ("Golang", "programming", "intermediate", 1),
    ]
    
    for skill_name, category, proficiency, years in programming_skills:
        skill = Skill(
            skill_id=generate_id(),
            user_id=user_id,
            skill_name=skill_name,
            category=category,
            proficiency_level=proficiency,
            years_experience=years
        )
        db.add_skill(skill)
    
    framework_skills = [
        ("PyTorch", "ml_framework", "advanced", 2),
        ("TensorFlow", "ml_framework", "advanced", 2),
        ("React", "web_framework", "advanced", 3),
        ("Django", "web_framework", "advanced", 2),
        ("React Native", "mobile_framework", "intermediate", 2),
    ]
    
    for skill_name, category, proficiency, years in framework_skills:
        skill = Skill(
            skill_id=generate_id(),
            user_id=user_id,
            skill_name=skill_name,
            category=category,
            proficiency_level=proficiency,
            years_experience=years
        )
        db.add_skill(skill)
    
    # Projects
    flashvault_project = Project(
        project_id=generate_id(),
        user_id=user_id,
        project_name="Flashvault AI Agent",
        description="AI cross-platform app that helps users retain information using customized flashcards. Agentic flow built using LangGraph and Model Context Protocol (MCP)",
        technologies="LangGraph, Model Context Protocol (MCP), AI/ML",
        start_date="2024-01",
        end_date=None,
        status="ongoing",
        github_url=None
    )
    db.add_project(flashvault_project)
    
    pet_social_project = Project(
        project_id=generate_id(),
        user_id=user_id,
        project_name="Pet Social",
        description="Full-fledged social media platform for pet owners to share posts and chat with each other",
        technologies="React, MongoDB, Express.js, GraphQL",
        start_date="2022-06",
        end_date="2022-12",
        status="completed",
        github_url=None
    )
    db.add_project(pet_social_project)
    
    # Professional Interests
    interests = [
        ("technology", "AI/ML Infrastructure", "Building scalable AI/ML systems for large-scale applications", "high"),
        ("technology", "Agentic AI", "Developing autonomous AI agents for real-world applications", "high"),
        ("technology", "High-Frequency Trading", "Algorithmic trading systems with sub-millisecond latency", "medium"),
        ("industry", "EdTech", "Educational technology and learning optimization", "medium"),
        ("technology", "Vector Databases", "Semantic search and RAG systems", "high"),
        ("role", "Technical Leadership", "Leading engineering teams and technical strategy", "medium"),
    ]
    
    for interest_type, name, description, priority in interests:
        interest = ProfessionalInterest(
            interest_id=generate_id(),
            user_id=user_id,
            interest_type=interest_type,
            interest_name=name,
            description=description,
            priority=priority
        )
        db.add_professional_interest(interest)
    
    # Networking Goals
    goals = [
        ("mentor", "Learn from AI/ML Leaders", "Connect with senior engineers and researchers in AI/ML infrastructure", "Technology, AI/ML", "Staff Engineer, Principal Engineer, Engineering Manager", "coffee_chat"),
        ("peer", "Connect with Fellow Engineers", "Build relationships with engineers working on similar technical challenges", "Technology, Finance", "Software Engineer, ML Engineer", "project_collaboration"),
        ("industry_expert", "Fintech and Trading Experts", "Learn from experts in quantitative trading and financial technology", "Finance, Trading", "Quant Developer, Trading Systems Engineer", "advice_session"),
        ("collaborator", "Open Source Contributors", "Collaborate on AI/ML and infrastructure projects", "Technology", "Software Engineer, Research Engineer", "project_collaboration"),
    ]
    
    for goal_type, description, full_desc, industries, roles, interaction in goals:
        goal = NetworkingGoal(
            goal_id=generate_id(),
            user_id=user_id,
            goal_type=goal_type,
            description=full_desc,
            target_industries=industries,
            target_roles=roles,
            preferred_interaction=interaction
        )
        db.add_networking_goal(goal)


def init_mock_profiles(db: DatabaseManager):
    """Initialize mock profiles for testing"""
    
    # Mock User 1: Sarah Chen - AI Researcher
    user_id = "sarah_chen_001"
    
    user = User(
        user_id=user_id,
        name="Sarah Chen",
        email="sarah.chen@tech.com",
        phone="+1 415 555 0123",
        linkedin="linkedin.com/in/sarah-chen-ai",
        github="sarahchen",
        current_role="Senior AI Researcher",
        current_company="OpenAI",
        location="San Francisco, CA",
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp()
    )
    db.add_user(user)
    
    # Sarah's education
    education = Education(
        education_id=generate_id(),
        user_id=user_id,
        institution="Stanford University",
        degree="PhD in Computer Science",
        field_of_study="Artificial Intelligence",
        start_date="2018-09",
        end_date="2022-06",
        gpa=None,
        honors="Summa Cum Laude",
        achievements="Stanford AI Fellowship, Best Paper Award at NeurIPS 2021"
    )
    db.add_education(education)
    
    # Sarah's work experience
    experience = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="OpenAI",
        role="Senior AI Researcher",
        start_date="2022-07",
        end_date=None,
        location="San Francisco, CA",
        description="Leading research on large language models and AI safety",
        key_achievements="Co-authored 5 papers on LLM safety; Led team that improved model alignment by 30%; Developed novel training techniques for RLHF",
        technologies="PyTorch, Python, Distributed Training, RLHF, Transformer Models"
    )
    db.add_work_experience(experience)
    
    # Professional interests
    interest = ProfessionalInterest(
        interest_id=generate_id(),
        user_id=user_id,
        interest_type="technology",
        interest_name="AI Safety",
        description="Ensuring AI systems are aligned with human values and behave safely",
        priority="high"
    )
    db.add_professional_interest(interest)
    
    # Networking goal
    goal = NetworkingGoal(
        goal_id=generate_id(),
        user_id=user_id,
        goal_type="mentor",
        description="Share knowledge about AI safety research with engineers building production AI systems",
        target_industries="Technology, AI/ML",
        target_roles="ML Engineer, AI Engineer, Research Engineer",
        preferred_interaction="advice_session"
    )
    db.add_networking_goal(goal)
    
    # Mock User 2: Alex Rodriguez - Product Manager
    user_id = "alex_rodriguez_001"
    
    user = User(
        user_id=user_id,
        name="Alex Rodriguez",
        email="alex.rodriguez@startup.com",
        phone="+1 650 555 0456",
        linkedin="linkedin.com/in/alex-rodriguez-pm",
        github="alexrod",
        current_role="Senior Product Manager",
        current_company="Stripe",
        location="San Francisco, CA",
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp()
    )
    db.add_user(user)
    
    # Alex's education
    education = Education(
        education_id=generate_id(),
        user_id=user_id,
        institution="UC Berkeley",
        degree="MBA",
        field_of_study="Technology Management",
        start_date="2019-08",
        end_date="2021-05",
        gpa="3.8/4.0",
        honors=None,
        achievements="Product Management Club President, Tech Trek to Silicon Valley"
    )
    db.add_education(education)
    
    # Alex's work experience
    experience = WorkExperience(
        experience_id=generate_id(),
        user_id=user_id,
        company="Stripe",
        role="Senior Product Manager",
        start_date="2021-06",
        end_date=None,
        location="San Francisco, CA",
        description="Leading product strategy for developer tools and API products",
        key_achievements="Launched 3 major API features used by 100k+ developers; Increased developer adoption by 40%; Led cross-functional team of 12 engineers and designers",
        technologies="Product Analytics, A/B Testing, SQL, APIs, Developer Tools"
    )
    db.add_work_experience(experience)
    
    # Professional interest
    interest = ProfessionalInterest(
        interest_id=generate_id(),
        user_id=user_id,
        interest_type="role",
        interest_name="Developer Experience",
        description="Creating exceptional experiences for software developers using APIs and tools",
        priority="high"
    )
    db.add_professional_interest(interest)
    
    # Networking goal
    goal = NetworkingGoal(
        goal_id=generate_id(),
        user_id=user_id,
        goal_type="peer",
        description="Connect with technical product managers working on developer tools",
        target_industries="Technology, SaaS, Developer Tools",
        target_roles="Product Manager, Technical Product Manager",
        preferred_interaction="coffee_chat"
    )
    db.add_networking_goal(goal)


def main():
    """Initialize database with all data"""
    print("🗄️ Initializing Digital Twin Database...")
    
    # Create database manager
    db = DatabaseManager("digital_twin.db")
    
    print("📝 Adding Bryan Wong's profile...")
    init_bryan_wong_profile(db)
    
    print("👥 Adding mock profiles...")
    init_mock_profiles(db)
    
    print("✅ Database initialization complete!")
    
    # Verify data
    users = db.get_all_users()
    print(f"📊 Total users in database: {len(users)}")
    
    for user in users:
        print(f"  - {user['name']} ({user['current_role']} at {user['current_company']})")
    
    # Show Bryan's complete profile
    print("\n🔍 Bryan Wong's Profile Preview:")
    bryan_profile = db.get_user_profile("bryan_wong_001")
    print(f"  Education: {len(bryan_profile['education'])} records")
    print(f"  Work Experience: {len(bryan_profile['work_experience'])} roles")
    print(f"  Skills: {len(bryan_profile['skills'])} skills")
    print(f"  Projects: {len(bryan_profile['projects'])} projects")
    print(f"  Professional Interests: {len(bryan_profile['professional_interests'])} interests")
    print(f"  Networking Goals: {len(bryan_profile['networking_goals'])} goals")


if __name__ == "__main__":
    main()