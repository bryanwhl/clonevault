# Digital Twin AI Agent

An autonomous AI agent that serves as a digital twin, capable of engaging in conversations and answering questions about a specific individual based on their resume. Built using LangGraph, MCP (Model Control Protocol), and Claude.

## Features

- 🤖 **LangGraph-based Conversation Flow** - Strategic conversation planning and response generation
- 🔍 **Dynamic LinkedIn Scraping** - Real-time profile data extraction for any user
- 💾 **SQLite Database Integration** - Comprehensive user profile storage and management
- 📝 **Dynamic Prompt Generation** - Conversation-specific prompt prefixes with user context
- 🌐 **Multi-user Support** - Parameterized startup for different users
- 📋 **Resume Processing** - PDF resume parsing with detailed attribute extraction
- 🔄 **Real-time Data Processing** - Automatic profile updates during agent initialization

## Architecture

- **LangGraph**: Manages conversation flow and state
- **MCP Server**: Parses resume data and provides structured information
- **OpenAI API**: Generates responses as the digital twin
- **Python 3.13.1**: Core runtime environment

## Quick Start

### 1. Setup

```bash
# Install dependencies and configure environment
python setup.py
```

### 2. Configure Environment

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=your_actual_api_key_here

# Optional: LinkedIn Scraping (for enhanced profile data)
LINKEDIN_EMAIL=your-email@domain.com
LINKEDIN_PASSWORD=your-password
```

### 3. Run the Agent

#### Web Interface (Recommended)
```bash
# Default user
python start_web_chat.py

# Specific user
python start_web_chat.py --user bryan_wong_001
```

#### Command Line Interface
```bash
python digital_twin_agent.py
```

## LinkedIn Scraping

The system includes advanced LinkedIn profile scraping capabilities for dynamic user data extraction.

### Data Extracted
- **Basic Profile**: Headline, summary, location, industry
- **Work Experience**: Job titles, companies, dates, descriptions, locations
- **Education**: Degrees, institutions, graduation dates, GPA, honors
- **Keywords**: Technical skills and industry-specific terms

### Authentication Levels

#### No Authentication (Default)
- Extracts basic profile information
- Intelligent fallbacks based on URL patterns
- Industry detection from profile identifiers

#### With Authentication (Enhanced)
- Complete work experience history
- Detailed education records
- Comprehensive skill extraction
- Full profile summaries

### Setup LinkedIn Credentials

1. **Add to .env file**:
   ```bash
   LINKEDIN_EMAIL=your-email@domain.com
   LINKEDIN_PASSWORD=your-password
   ```

2. **Security Considerations**:
   - Credentials are stored locally in `.env` (never committed to git)
   - Uses secure authentication through selenium
   - Respects LinkedIn's rate limiting and privacy settings

3. **How It Works**:
   - Real-time scraping during agent initialization
   - Automatic ChromeDriver management
   - Intelligent retry mechanisms with fallbacks
   - Works for any LinkedIn profile URL

## Detailed Setup & Usage Instructions

### Prerequisites

- Python 3.13.1 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)
- PDF resume file (already included: `./files/BryanWong_Resume_20250710.pdf`)

### Step-by-Step Setup

#### 1. Environment Setup

First, install the required dependencies:

```bash
# Option A: Use the automated setup script
python setup.py

# Option B: Manual installation
pip install -r requirements.txt
```

#### 2. API Key Configuration

Create and configure your environment file:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your favorite text editor
nano .env  # or vim .env, code .env, etc.
```

Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

#### 3. Verify Setup

Check that everything is configured correctly:

```bash
# Verify Python version
python --version

# Verify required files exist
ls -la files/
ls -la .env

# Test dependencies
python -c "import langgraph, openai, PyPDF2; print('All dependencies OK')"
```

### Running the Digital Twin Agent

#### Method 1: Direct Execution (Recommended)

The digital twin agent includes both the MCP server functionality and the conversation interface in a single script:

```bash
# Start the digital twin agent
python digital_twin_agent.py
```

This will:
1. Initialize the MCP client internally
2. Parse the resume file automatically
3. Start the interactive CLI conversation interface

#### Method 2: Standalone MCP Server (Advanced)

If you want to run the MCP server separately for development or testing:

**Terminal 1 - Start MCP Server:**
```bash
# Run the MCP server
python mcp_server.py
```

**Terminal 2 - Test MCP Server (Optional):**
```bash
# Test the server with sample input
echo '{"method": "tools/call", "params": {"name": "parse_resume", "arguments": {"file_path": "./files/BryanWong_Resume_20250710.pdf"}}}' | python mcp_server.py
```

Note: The digital twin agent uses the MCP server functionality internally, so running it separately is usually not necessary for normal usage.

### Interactive CLI Usage

Once the agent starts successfully, you'll see:

```
🤖 Digital Twin Agent for Bryan Wong is ready!
Type 'quit' to exit the conversation.

<agent_response>
Hi there! I'm Bryan Wong. Nice to meet you!
</agent_response>

<agent_question>
What brings you here today? I'd love to learn more about you!
</agent_question>

You: 
```

#### Commands and Interaction

- **Chat normally**: Type your message and press Enter
- **Exit**: Type `quit`, `exit`, or `bye` to end the conversation
- **Interrupt**: Press `Ctrl+C` to force quit

#### Example Conversation Flow

```bash
You: Hi Bryan! I'm a software engineer working in AI/ML.

<agent_response>
That's fantastic! AI/ML is such an exciting field. I've been working in software development myself, with experience in various technologies and always eager to learn about new developments in the space.
</agent_response>

<agent_question>
What specific area of AI/ML are you focusing on? Are you working more on the research side or implementing production systems?
</agent_question>

You: I focus on implementing production ML systems, especially MLOps.

<agent_response>
MLOps is crucial for successful AI implementations! The gap between ML models in notebooks and production systems is huge. I really appreciate the engineering discipline that MLOps brings to make AI actually work reliably in real-world applications.
</agent_response>

<agent_question>
What's been your biggest challenge in transitioning models from development to production?
</agent_question>

You: quit
```

### Troubleshooting

#### Common Issues and Solutions

**1. "OPENAI_API_KEY not set" Error**
```bash
# Check if .env file exists
ls -la .env

# Check if API key is set correctly
cat .env

# Ensure no extra spaces or quotes around the key
```

**2. "Resume file not found" Error**
```bash
# Verify resume file exists
ls -la files/BryanWong_Resume_20250710.pdf

# Check file permissions
chmod 644 files/BryanWong_Resume_20250710.pdf
```

**3. "Module not found" Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific missing modules
pip install langgraph openai PyPDF2
```

**4. "Permission denied" Error**
```bash
# Make scripts executable
chmod +x digital_twin_agent.py
chmod +x setup.py

# Or run with python explicitly
python digital_twin_agent.py
```

**5. PDF Parsing Issues**
```bash
# Check if PDF is readable
python -c "import PyPDF2; print('PDF library working')"

# Verify PDF file is not corrupted
file files/BryanWong_Resume_20250710.pdf
```

#### Debug Mode

For detailed debugging information, you can modify the agent script to enable verbose logging:

```bash
# Add debug prints by editing digital_twin_agent.py
# Look for the main() function and add:
# import logging
# logging.basicConfig(level=logging.DEBUG)
```

### Advanced Configuration

#### Customizing the Agent

You can modify the agent's behavior by editing `digital_twin_agent.py`:

- **Response length**: Change `max_tokens` parameter in `_generate_response()`
- **Personality**: Modify the prompt template in `_generate_response()`
- **Question types**: Edit the questions dictionary in `_generate_question()`
- **Conversation topics**: Update topic detection in `analyze_input_node()`

#### Using Different Resume Files

To use a different resume:

1. Place your PDF file in the `./files/` directory
2. Update the `resume_path` variable in `digital_twin_agent.py`:
   ```python
   resume_path = "./files/your_resume.pdf"
   ```

#### API Configuration

You can adjust OpenAI API settings in the `_generate_response()` method:

```python
response = self.client.chat.completions.create(
    model="gpt-4",                      # Change model here (gpt-3.5-turbo, gpt-4, etc.)
    max_tokens=300,                     # Adjust response length
    temperature=0.7,                    # Add for creativity control
    messages=[{"role": "user", "content": prompt}]
)
```

## Project Structure

```
.
├── digital_twin_agent.py              # Main agent implementation
├── mcp_server.py                      # MCP server for resume parsing
├── requirements.txt                   # Python dependencies
├── setup.py                          # Setup script
├── .env.example                      # Environment template
├── .env                              # Your API configuration (create this)
├── README.md                         # This file
└── files/
    └── BryanWong_Resume_20250710.pdf  # Resume file
```

## Technical Details

### Components

1. **MCPClient**: Handles resume parsing and data extraction
2. **DigitalTwinAgent**: Main agent class with LangGraph workflow
3. **ConversationState**: State management for conversation flow
4. **Response Generation**: OpenAI-powered response generation
5. **Question Generation**: Context-aware follow-up questions

### Conversation Flow

```
Load Resume → Analyze Input → Generate Response → Generate Question → End
```

### Error Handling

- PDF parsing errors
- API connection issues
- Missing configuration files
- Invalid resume formats

## Requirements

- Python 3.13.1+
- OpenAI API key
- PDF resume file
- Required Python packages (see requirements.txt)

## Output Format

The agent provides responses in a structured format:

```xml
<agent_response>
[Agent's answer as the digital twin]
</agent_response>

<agent_question>
[Follow-up question to learn about you]
</agent_question>
```

## Future Improvements

- Support for multiple resume formats (Word, text)
- Enhanced personality modeling
- Memory of previous conversations
- Web interface option
- Voice interaction capabilities
- Multi-language support

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- The API key has access to your OpenAI account - treat it like a password
- Resume data is processed locally and only sent to OpenAI for response generation