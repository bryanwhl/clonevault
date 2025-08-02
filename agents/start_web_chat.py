#!/usr/bin/env python3
"""
Starter script for the Enhanced Digital Twin Agent Web Chat Interface
"""

import os
import sys
import argparse
from pathlib import Path

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Start the Enhanced Digital Twin Agent Web Chat Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_web_chat.py                                    # Default user (bryan_wong_001)
  python start_web_chat.py --user bryan_wong_001              # Specific user
  python start_web_chat.py --user sarah_chen_001              # Different user
  python start_web_chat.py --user alex_rodriguez_001          # Another user
  
Available users can be found in the database. Use the web interface 
to switch between users or specify the user at startup.
        """
    )
    
    parser.add_argument(
        "--user", 
        "-u",
        default="bryan_wong_001",
        help="User ID for the digital twin agent (default: bryan_wong_001)"
    )
    
    parser.add_argument(
        "--port",
        "-p", 
        type=int,
        default=5000,
        help="Port number for the web server (default: 5000)"
    )
    
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host address for the web server (default: localhost)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    return parser.parse_args()

def main():
    """Start the enhanced web chat interface"""
    args = parse_arguments()
    
    print("🚀 Enhanced Digital Twin Agent Web Chat Interface")
    print("=" * 60)
    print(f"👤 User ID: {args.user}")
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"🐛 Debug Mode: {'Enabled' if args.debug else 'Disabled'}")
    print("=" * 60)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    required_files = [
        "digital_twin_agent.py",
        "database_manager.py", 
        "prompt_prefix.txt",
        "digital_twin.db"
    ]
    
    missing_files = []
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Error: Missing required files: {', '.join(missing_files)}")
        print(f"Current directory: {current_dir}")
        if "digital_twin.db" in missing_files:
            print("💡 Tip: Run 'python init_database.py' to create the database")
        return 1
    
    # Check for .env file
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("❌ Error: .env file not found")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=sk-your-key-here")
        return 1
    
    # Validate user exists in database
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager("digital_twin.db")
        user_profile = db.get_user_profile(args.user)
        
        if not user_profile:
            print(f"❌ Error: User '{args.user}' not found in database")
            print("\nAvailable users:")
            users = db.get_all_users()
            for user in users:
                print(f"  - {user['user_id']}: {user['name']} ({user['current_role']} at {user['current_company']})")
            return 1
        else:
            user_info = user_profile.get("user", {})
            print(f"✅ User found: {user_info.get('name')} - {user_info.get('current_role')} at {user_info.get('current_company')}")
            
    except Exception as e:
        print(f"❌ Error validating user: {e}")
        return 1
    
    print("✅ All requirements met")
    print("\n📋 Enhanced Features:")
    print("  💾 SQLite database with professional career context")
    print("  📝 Dynamic prompt prefix system per conversation")
    print("  👥 Multi-user support with parameterized startup")
    print("  🤔 Context-aware conversation flow")
    print("  🔄 LinkedIn and resume processing")
    print(f"\n🌐 Starting web interface for {user_info.get('name')}...")
    print(f"🌐 Open your browser to: http://{args.host}:{args.port}")
    print("💬 Chat with the enhanced digital twin agent")
    print("🛑 Press Ctrl+C to stop the server")
    print("\n" + "=" * 60)
    
    # Import and run the enhanced web chat
    try:
        from web_chat import run_app
        run_app(user_id=args.user, host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n\n👋 Enhanced web chat interface stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting enhanced web interface: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())