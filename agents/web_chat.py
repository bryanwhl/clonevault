#!/usr/bin/env python3
"""
Enhanced Flask Web Interface for Digital Twin Agent V2
Development and testing purposes only
"""

import asyncio
import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from digital_twin_agent import DigitalTwinAgent

app = Flask(__name__)
CORS(app)

# Global agent instance and configuration
agent = None
current_user_id = "bryan_wong_001"  # Default user ID

async def initialize_agent(user_id: str = None):
    """Initialize the enhanced digital twin agent"""
    global agent, current_user_id
    
    if user_id:
        current_user_id = user_id
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable not set")
    
    # Initialize enhanced agent with conversation ID
    import uuid
    conversation_id = str(uuid.uuid4())
    agent = DigitalTwinAgent(api_key, user_id=current_user_id, conversation_id=conversation_id)
    
    print(f"✅ Enhanced Digital Twin Agent initialized successfully for {current_user_id}")

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response, question = loop.run_until_complete(agent.chat(user_message))
        loop.close()
        
        return jsonify({
            'response': response,
            'question': question
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Check if agent is ready"""
    global agent
    
    if not agent:
        return jsonify({'status': 'not_initialized'})
    
    user_summary = agent.get_user_summary()
    user_info = agent.user_profile.get('user', {})
    
    return jsonify({
        'status': 'ready',
        'agent_name': user_info.get('name', 'Digital Twin'),
        'agent_role': user_info.get('current_role', ''),
        'agent_company': user_info.get('current_company', ''),
        'user_summary': user_summary,
        'database_enabled': True,
        'prompt_prefix_enabled': True
    })

@app.route('/api/profile')
def profile():
    """Get agent profile information"""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    profile = agent.user_profile
    user_info = profile.get('user', {})
    
    # Return summarized profile info
    return jsonify({
        'name': user_info.get('name'),
        'current_role': user_info.get('current_role'),
        'current_company': user_info.get('current_company'),
        'location': user_info.get('location'),
        'education_count': len(profile.get('education', [])),
        'experience_count': len(profile.get('work_experience', [])),
        'skills_count': len(profile.get('skills', [])),
        'projects_count': len(profile.get('projects', [])),
        'interests_count': len(profile.get('professional_interests', [])),
        'networking_goals_count': len(profile.get('networking_goals', []))
    })

@app.route('/api/user_context')
def user_context():
    """Get comprehensive user context from database"""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    try:
        # Get full user profile from database
        full_profile = agent.user_profile
        
        # Get LinkedIn and resume attributes if available
        linkedin_attrs = agent.db.get_linkedin_attributes(current_user_id)
        resume_attrs = agent.db.get_resume_attributes(current_user_id)
        
        # Structure the comprehensive user context
        context = {
            'user_info': full_profile.get('user', {}),
            'education': full_profile.get('education', []),
            'work_experience': full_profile.get('work_experience', []),
            'skills': full_profile.get('skills', []),
            'projects': full_profile.get('projects', []),
            'professional_interests': full_profile.get('professional_interests', []),
            'networking_goals': full_profile.get('networking_goals', []),
            'linkedin_attributes': linkedin_attrs,
            'resume_attributes': resume_attrs
        }
        
        return jsonify(context)
        
    except Exception as e:
        print(f"Error getting user context: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset')
def reset():
    """Reset conversation history"""
    global agent
    
    if agent:
        agent.conversation_history = []
        return jsonify({'status': 'reset'})
    
    return jsonify({'error': 'Agent not initialized'}), 500

@app.route('/api/users')
def users():
    """Get all users in the database"""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    try:
        users = agent.db.get_all_users()
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/switch_user/<user_id>')
def switch_user(user_id):
    """Switch to a different user"""
    global agent
    
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    try:
        # Check if user exists
        profile = agent.db.get_user_profile(user_id)
        if not profile:
            return jsonify({'error': 'User not found'}), 404
        
        # Reinitialize agent with new user and new conversation ID
        api_key = os.getenv("OPENAI_API_KEY")
        import uuid
        new_conversation_id = str(uuid.uuid4())
        agent = DigitalTwinAgent(api_key, user_id=user_id, conversation_id=new_conversation_id)
        
        user_summary = agent.get_user_summary()
        return jsonify({
            'status': 'switched',
            'user_summary': user_summary,
            'agent_name': profile['user']['name']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_app(user_id: str = "bryan_wong_001", host: str = "localhost", 
            port: int = 5000, debug: bool = True):
    """Run the Flask app with agent initialization"""
    print("🚀 Starting Enhanced Digital Twin Agent Web Interface...")
    
    # Initialize agent with specified user
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_agent(user_id))
        loop.close()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    print(f"🌐 Starting Flask web server on http://{host}:{port}")
    print("💾 Database integration enabled")
    print("📝 Prompt prefix system enabled")
    print("🔄 LinkedIn and resume processing enabled")
    app.run(debug=debug, host=host, port=port)

if __name__ == "__main__":
    run_app()
