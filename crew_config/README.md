# Advanced CrewAI Setup for Rivermarsh

## Overview

This is a **hierarchical AI development crew** with full MCP (Model Context Protocol) integration, enabling agents to use tools you don't have direct access to.

### Architecture

```
Manager Agent (Coordinator)
    ├─ ECS Architect (Code analysis tools)
    ├─ Yuka AI Engineer (Editing + testing tools)
    ├─ Rendering Engineer (Browser + React + Material UI tools)
    ├─ Systems Engineer (All tools)
    ├─ QA Tester (Testing + validation tools)
    └─ Chief Architect (Documentation + context tools)
```

## MCP Servers Integrated

### 1. **Material UI MCP** 🎨
- Component generation from descriptions
- Theme customization
- Layout assistance
- Best integration for React UIs
- **Package**: `@mui/mcp-server`

### 2. **Playwright MCP** 🎭
- Browser automation
- E2E testing
- Visual regression testing
- Screenshot capture
- **Package**: `@playwright/mcp-server`

### 3. **Context7 (Upstash)** 🧠
- Advanced context management
- Distributed state
- Real-time sync
- **Package**: `@upstash/context7-mcp`
- **Requires**: UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN

### 4. **Vite-React MCP** ⚛️
- React dev tooling
- HMR management
- Build optimization
- **Package**: `vite-react-mcp`

### 5. **Context-portal MCP** 📚
- Collaborative documentation
- Project knowledge management
- Context sharing across agents
- **Package**: `context-portal`

## Setup

### 1. Install Dependencies

```bash
# Python dependencies
pip install crewai crewai-tools pyyaml

# Enable MCP support
pip install crewai-tools[mcp]
```

### 2. Set Environment Variables

```bash
# LLM Provider (choose one)
export ANTHROPIC_API_KEY="sk-ant-..."      # Claude (recommended)
export OPENROUTER_API_KEY="sk-or-..."     # OpenRouter (flexible)
export OPENAI_API_KEY="sk-..."            # OpenAI (fallback)

# Upstash (for Context7 MCP)
export UPSTASH_REDIS_REST_URL="https://..."
export UPSTASH_REDIS_REST_TOKEN="..."
```

### 3. Run the Crew

```bash
# Basic run (uses Anthropic/OpenAI)
python game_dev_crew_advanced.py

# Or run the simple version (no MCP)
python game_dev_crew.py
```

## How It Works

### Tool Distribution

Each agent gets specialized tools based on their role:

```python
# Rendering Engineer gets UI-focused tools
rendering_tools = filter_tools(
    tools_list, 
    ['browser', 'playwright', 'vite', 'react', 'ui', 'mui', 'material']
)

# QA Tester gets testing tools
qa_tools = filter_tools(
    tools_list,
    ['test', 'validate', 'check', 'lint', 'playwright']
)
```

### Hierarchical Process

1. **Manager** (LLM-powered) coordinates the workflow
2. **Manager** delegates tasks to specialist agents
3. **Specialists** use their MCP tools to complete tasks
4. **Results** flow back through manager to next agent
5. **Final output** aggregated by manager

## Benefits of This Approach

### 🚀 **Capabilities Beyond Your Own**
- Agents can run Playwright tests (you can't)
- Agents can manage distributed context with Upstash (you can't)
- Agents can generate Material UI components with official tooling (better than you can)

### 🎯 **Specialized Intelligence**
- Each agent only sees tools relevant to their role
- Reduces token usage and improves focus
- Better tool selection by specialists

### 🔄 **Flexible LLM Routing**
- OpenRouter's `auto` model picks best LLM for each task
- Automatic fallback: OpenRouter → Anthropic → OpenAI
- Cost optimization built-in

### 📈 **Scalable Architecture**
- Add new MCP servers in `mcp_servers.json`
- Add new agents in `agents.yaml`
- Add new tasks in `tasks.yaml`
- No code changes needed

## Configuration Files

### `mcp_servers.json`
Defines which MCP servers to connect to:

```json
{
  "mcpServers": {
    "material_ui": {
      "command": "npx",
      "args": ["-y", "@mui/mcp-server"],
      "env": {}
    }
  }
}
```

### `agents.yaml`
Defines agent roles, goals, and backstories:

```yaml
ecs_architect:
  role: "Chief ECS Architect"
  goal: "Review and validate ECS architecture"
  backstory: "Expert in entity-component systems..."
```

### `tasks.yaml`
Defines tasks and expected outputs:

```yaml
review_ecs_layer:
  agent: "chief_architect"
  description: "Review the completed ECS data layer..."
  expected_output: "Detailed architecture review..."
```

## Adding New MCP Servers

1. Find the MCP server package (e.g., on npm)
2. Add to `crew_config/mcp_servers.json`:

```json
{
  "mcpServers": {
    "your_server": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}"
      }
    }
  }
}
```

3. Update tool filtering in `game_dev_crew_advanced.py` if needed
4. Run the crew - tools automatically discovered!

## Troubleshooting

### MCP Server Connection Failed
```bash
# Test MCP server manually
npx -y @mui/mcp-server

# Check if npx is available
which npx

# Ensure Node.js is installed
node --version
```

### No Tools Loaded
- Check that MCP server packages are accessible via `npx`
- Verify environment variables are set
- Look for errors in console output

### Agent Not Using Expected Tools
- Check tool filtering keywords in `filter_tools()` function
- Print available tools: `print([t.name for t in tools_list])`
- Verify tool names match your keywords

## Next Steps

1. **Add More MCP Servers**: Explore https://github.com/modelcontextprotocol/servers
2. **Custom MCP Server**: Build your own for game-specific tools
3. **Memory Integration**: Enable `memory=True` in Crew for learning
4. **Parallel Execution**: Experiment with `Process.parallel` for speed

## Resources

- **CrewAI Docs**: https://docs.crewai.com
- **MCP Specification**: https://modelcontextprotocol.io
- **MCP Servers List**: https://github.com/modelcontextprotocol/servers
- **Material UI MCP**: https://mui.com/material-ui/getting-started/mcp/
- **OpenRouter**: https://openrouter.ai

---

**Built for Rivermarsh** - A 3D otter adventure game with AI-powered development
