# Rivermarsh CrewAI Development System

## Overview
Autonomous AI development crew using CrewAI + OpenRouter for accelerated game development.

## Quick Start

```bash
# 1. Ensure secrets are set in Replit
# Required: OPENROUTER_API_KEY
# Optional: ANTHROPIC_API_KEY (fallback)

# 2. Run the crew
python3 game_dev_crew_advanced.py
```

## Architecture

### 6 Specialist Agents
1. **ECS Architect** - Data structures, Miniplex systems, TypeScript validation
2. **Yuka AI Engineer** - Creature behaviors, steering, state machines
3. **Rendering Engineer** - R3F, shaders, post-processing, performance
4. **Systems Engineer** - Quests, dialogue, inventory, combat
5. **QA Tester** - Performance validation, testing, TypeScript checks
6. **Chief Architect** - Code review, documentation, alignment

### 10 MCP Servers
1. Material UI - Component library
2. Playwright - Browser testing
3. Context7 - Up-to-date docs (React, Three.js, etc.)
4. Vite-React - Dev tooling
5. ConPort - Project memory (project_brief.md)
6. Git - Version control
7. GitHub - PR/issue automation
8. Postgres - Database ops
9. Memory - Knowledge graph
10. Filesystem - File operations

### 6 Sequential Tasks
1. ECS data design & validation
2. Yuka AI integration
3. Terrain & water rendering
4. Quest & dialogue systems
5. Performance testing
6. Architecture review & docs update

## Configuration

### Environment Variables (via Replit Secrets)
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Model Selection
Default: `openrouter/anthropic/claude-3.5-sonnet`

OpenRouter auto-routes to optimal models based on task.

### File Structure
```
crew_config/
├── agents.yaml       # Agent definitions
├── tasks.yaml        # Task definitions
├── mcp_servers.json  # MCP server configs
└── README.md         # This file

project_brief.md      # ConPort context file
game_dev_crew_advanced.py  # Main crew script
```

## How It Works

1. **Load configs** from YAML files
2. **Setup OpenRouter** via environment variables
3. **Create MCP tools** for agent capabilities
4. **Assign specialized tools** to each agent
5. **Execute tasks sequentially** with full autonomy
6. **Agents use tools** to read/write code, test, commit

## Expected Output

The crew will:
- ✅ Review & enhance ECS data layer
- ✅ Implement Yuka AI creature behaviors
- ✅ Build chunked terrain + advanced water
- ✅ Create quest/dialogue systems
- ✅ Run performance tests (60fps target)
- ✅ Update architecture docs

## Monitoring

Watch agent progress in terminal output. Agents will:
- Read files to understand current state
- Write/edit code following architecture
- Run tests and validate changes
- Update documentation
- Self-review before completion

## Troubleshooting

**Error: "No auth credentials"**
- Ensure OPENROUTER_API_KEY is set in Replit Secrets

**Error: "Model not found"**
- Model name format: `openrouter/provider/model-name`

**Agent stuck on file read errors**
- Normal - agent is exploring codebase
- Will self-correct and continue

## Next Steps

After crew completes:
1. Review generated code
2. Test the game (restart workflow)
3. Iterate with new tasks
4. Let crew handle 90% of development

The goal: Let AI agents do the heavy lifting while you focus on creative direction.
