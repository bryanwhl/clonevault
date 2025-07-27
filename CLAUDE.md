# Development Partnership

We're building production-quality code together. Your role is to create maintainable, efficient solutions while catching potential issues early.

When you seem stuck or overly complex, I'll redirect you - my guidance helps you stay on track.

## 🚨 AUTOMATED CHECKS ARE MANDATORY
**ALL hook issues are BLOCKING - EVERYTHING must be ✅ GREEN!**  
No errors. No formatting issues. No linting problems. Zero tolerance.  
These are not suggestions. Fix ALL issues before continuing.

## CRITICAL WORKFLOW - ALWAYS FOLLOW THIS!

### Research → Plan → Implement
**NEVER JUMP STRAIGHT TO CODING!** Always follow this sequence:
1. **Research**: Explore the codebase, understand existing patterns
2. **Plan**: Create a detailed implementation plan and verify it with me  
3. **Implement**: Execute the plan with validation checkpoints

When asked to implement any feature, you'll first say: "Let me research the codebase and create a plan before implementing."

For complex architectural decisions or challenging problems, use **"ultrathink"** to engage maximum reasoning capacity. Say: "Let me ultrathink about this architecture before proposing a solution."

### USE MULTIPLE AGENTS!
*Leverage subagents aggressively* for better results:

* Spawn agents to explore different parts of the codebase in parallel
* Use one agent to write tests while another implements features
* Delegate research tasks: "I'll have an agent investigate the database schema while I analyze the API structure"
* For complex refactors: One agent identifies changes, another implements them

Say: "I'll spawn agents to tackle different aspects of this problem" whenever a task has multiple independent parts.

### Reality Checkpoints
**Stop and validate** at these moments:
- After implementing a complete feature
- Before starting a new major component  
- When something feels wrong
- Before declaring "done"
- **WHEN HOOKS FAIL WITH ERRORS** ❌

**For Web App:**
```bash
cd web_app/
npm run lint && npm run build
```

**For Python Agents:**
```bash
cd agents/
python -m pytest test_agent.py
python digital_twin_agent.py  # Manual smoke test
```

> Why: You can lose track of what's actually working. These checkpoints prevent cascading failures.

### 🚨 CRITICAL: Hook Failures Are BLOCKING
**When hooks report ANY issues (exit code 2), you MUST:**
1. **STOP IMMEDIATELY** - Do not continue with other tasks
2. **FIX ALL ISSUES** - Address every ❌ issue until everything is ✅ GREEN
3. **VERIFY THE FIX** - Re-run the failed command to confirm it's fixed
4. **CONTINUE ORIGINAL TASK** - Return to what you were doing before the interrupt
5. **NEVER IGNORE** - There are NO warnings, only requirements

This includes:
- Formatting issues (gofmt, black, prettier, etc.)
- Linting violations (golangci-lint, eslint, etc.)
- Forbidden patterns (time.Sleep, panic(), interface{})
- ALL other checks

Your code must be 100% clean. No exceptions.

**Recovery Protocol:**
- When interrupted by a hook failure, maintain awareness of your original task
- After fixing all issues and verifying the fix, continue where you left off
- Use the todo list to track both the fix and your original task

## Working Memory Management

### When context gets long:
- Re-read this CLAUDE.md file
- Summarize progress in a PROGRESS.md file
- Document current state before major changes

### Maintain TODO.md:
```
## Current Task
- [ ] What we're doing RIGHT NOW

## Completed  
- [x] What's actually done and tested

## Next Steps
- [ ] What comes next
```

## Project-Specific Rules

### TwinNet Digital Twin Platform
This project consists of two main components:
1. **Python AI Agents** (`/agents/`) - LangGraph-based digital twin agents
2. **React Web App** (`/web_app/`) - TypeScript frontend for agent management

### Python Agent Rules

#### FORBIDDEN - NEVER DO THESE:
- **NO hardcoded API keys** - always use environment variables
- **NO time.sleep()** for polling - use proper async patterns
- **NO** keeping old and new code together
- **NO** migration functions or compatibility layers
- **NO** versioned function names (processV2, handleNew)
- **NO** unhandled exceptions in main flow
- **NO** TODOs in final code

#### Required Standards:
- **Delete** old code when replacing it
- **Meaningful names**: `user_id` not `id`
- **Type hints** on all functions
- **Proper error handling** with try/except blocks
- **Environment variables** for all configuration
- **Async/await** for I/O operations when possible
- **Virtual environment** activation before running

### React/TypeScript Web App Rules

#### FORBIDDEN - NEVER DO THESE:
- **NO `any` types** - use proper TypeScript types
- **NO inline styles** - use Tailwind CSS classes
- **NO** keeping old and new code together
- **NO** unused imports or variables
- **NO** console.log in production code
- **NO** TODOs in final code

#### Required Standards:
- **Delete** old code when replacing it
- **Meaningful names**: `userId` not `id`
- **Proper TypeScript types** for all props and state
- **Functional components** with hooks
- **shadcn/ui components** for consistent UI
- **Accessibility** attributes (ARIA labels, roles)
- **Responsive design** with Tailwind breakpoints

## Implementation Standards

### Our code is complete when:
- ? All linters pass with zero issues
- ? All tests pass  
- ? Feature works end-to-end
- ? Old code is deleted
- ? Godoc on all exported symbols

### Testing Strategy
- Complex business logic ? Write tests first
- Simple CRUD ? Write tests after
- Hot paths ? Add benchmarks
- Skip tests for main() and simple CLI parsing

### Project Structure
```
/
├── agents/                    # Python AI agent backend
│   ├── digital_twin_agent.py  # Main agent implementation
│   ├── mcp_server.py          # MCP server for resume parsing
│   ├── requirements.txt       # Python dependencies
│   └── test_agent.py          # Agent tests
├── web_app/                   # React TypeScript frontend
│   ├── src/main.tsx           # React app entry point
│   ├── components/            # React components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── AgentConfig.tsx   # Agent configuration
│   │   ├── Dashboard.tsx     # Main dashboard
│   │   └── ...
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Build configuration
├── files/                    # Resume PDFs and assets
└── CLAUDE.md                 # This development guide
```

## Problem-Solving Together

When you're stuck or confused:
1. **Stop** - Don't spiral into complex solutions
2. **Delegate** - Consider spawning agents for parallel investigation
3. **Ultrathink** - For complex problems, say "I need to ultrathink through this challenge" to engage deeper reasoning
4. **Step back** - Re-read the requirements
5. **Simplify** - The simple solution is usually correct
6. **Ask** - "I see two approaches: [A] vs [B]. Which do you prefer?"

My insights on better approaches are valued - please ask for them!

## Performance & Security

### **Measure First**:
- No premature optimization
- Benchmark before claiming something is faster
- Use pprof for real bottlenecks

### **Security Always**:
- Validate all inputs
- Use crypto/rand for randomness
- Prepared statements for SQL (never concatenate!)

## Communication Protocol

### Progress Updates:
```
✓ Implemented authentication (all tests passing)
✓ Added rate limiting  
✗ Found issue with token expiration - investigating
```

### Suggesting Improvements:
"The current approach works, but I notice [observation].
Would you like me to [specific improvement]?"

## Working Together

- This is always a feature branch - no backwards compatibility needed
- When in doubt, we choose clarity over cleverness
- **REMINDER**: If this file hasn't been referenced in 30+ minutes, RE-READ IT!

Avoid complex abstractions or "clever" code. The simple, obvious solution is probably better, and my guidance helps you stay focused on what matters.

## Automated Documentation Update System

### Documentation Files Overview

#### Primary Documentation
- **`CLAUDE.md`** - Development guidelines and project conventions (this file)
- **`agents/README.md`** - Python AI agent setup and usage instructions
- **`web_app/README.md`** - React frontend setup and development guide
- **`web_app/Attributions.md`** - Licensing and attribution information

#### Missing Documentation (Recommended)
- **`CONTRIBUTING.md`** - Contribution guidelines and workflow
- **`TROUBLESHOOTING.md`** - Common issues and solutions
- **`PATTERNS.md`** - Code patterns and architectural decisions
- **`DEPLOYMENT.md`** - Production deployment instructions

### Documentation Update Rules

#### When to Update Documentation
- **Before major feature implementation** - Update patterns and conventions
- **After architectural changes** - Reflect new project structure
- **When adding new dependencies** - Update setup instructions
- **After discovering patterns** - Document for future reference
- **Before final commit** - Ensure all changes are documented

#### Documentation Approval Process
1. **Propose Changes** - Describe what documentation needs updating and why
2. **Get Approval** - Ask: "Should I update [documentation] to include [change]?"
3. **Make Updates** - Only update after explicit approval
4. **Verify Accuracy** - Ensure instructions are complete and correct

#### Constraints and Security
- **NO sensitive information** - Never include API keys, passwords, or secrets
- **NO auto-updates** - Always get approval before changing documentation
- **Version control** - All documentation changes must be committed
- **Accuracy first** - Test all instructions before documenting them

#### Documentation Standards
- **Clear instructions** - Step-by-step with expected outcomes
- **Up-to-date dependencies** - Verify all versions and commands work
- **Cross-platform notes** - Include OS-specific instructions when needed
- **Error handling** - Document common issues and solutions