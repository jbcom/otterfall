# NEXT AGENT — CONPORT MEMORY SYSTEM ACTIVE

Status: ✅ CONPORT INTEGRATION COMPLETE  
Mode: Ready for AI-Assisted Development

---

## Session Summary (2025-11-25)

### What Was Done

#### 1. Context Portal (ConPort) Integration
- Cloned and analyzed context-portal repository
- Created comprehensive `projectBrief.md` for ConPort initialization
- Configured ConPort as MCP server in `.ruler/ruler.toml`
- Added ConPort to `process-compose.yaml` as background service

#### 2. Cursor Background Agent Rules
- Created `.cursor/rules/10-background-agent-conport.mdc`
- Defines initialization sequence for loading ConPort context
- Includes tool reference for all ConPort operations
- Establishes sync protocol for conversation → database

#### 3. Infrastructure Updates
- Added process-compose v1.51.1 to `.cursor/Dockerfile`
- Created `/workspace/logs/` and `/workspace/context_portal/` directories
- Created `.ruler/conport_usage.md` documentation

#### 4. Session Documentation
- Exported session work to `conport_export/session-2025-11-25/`
- Includes: decisions, progress, system patterns, custom data

---

## ConPort Quick Start

### 1. Initialize ConPort

```bash
# Start all background services (including ConPort)
process-compose up -d

# Or run ConPort standalone
uvx --from context-portal-mcp conport-mcp \
  --mode stdio \
  --workspace_id "$(pwd)" \
  --log-file ./logs/conport.log
```

### 2. Agent Initialization Protocol

At the start of EVERY session, execute:

```
[CONPORT_ACTIVE] or [CONPORT_INACTIVE]
```

Then load context:
```yaml
1. get_product_context      # Project goals from projectBrief.md
2. get_active_context       # Current sprint focus
3. get_decisions(limit: 5)  # Recent architectural decisions
4. get_progress(limit: 5)   # Recent task progress
5. get_system_patterns      # Coding patterns
```

### 3. Sync Protocol

Tell any AI agent:
```
Sync ConPort
```

This triggers full conversation → database synchronization.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI AGENTS (Consumers)                       │
│  Cursor │ Claude │ Copilot │ CrewAI │ Cline │ Windsurf         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ MCP Protocol
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ConPort MCP Server                           │
│  uvx --from context-portal-mcp conport-mcp                      │
│  Database: ./context_portal/context.db                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CREWAI GAME BUILDER                          │
│  python/crew_agents/                                            │
│  - GameBuilderCrew (code generation)                            │
│  - Knowledge Base (working code patterns)                       │
│  - Custom File Tools (safe read/write)                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Files

| File | Purpose |
|------|---------|
| `projectBrief.md` | ConPort initialization source |
| `.ruler/ruler.toml` | MCP server configuration |
| `.ruler/conport_usage.md` | ConPort tool reference |
| `.cursor/rules/10-background-agent-conport.mdc` | Agent rules |
| `process-compose.yaml` | Background service definitions |
| `conport_export/session-2025-11-25/` | Today's session export |

---

## Next Steps

### 1. Import Session Data to ConPort

Once ConPort is running, import today's session:
```bash
# Using ConPort MCP tool
import_markdown_to_conport:
  workspace_id: "/workspace"
  input_path: "./conport_export/session-2025-11-25/"
```

### 2. Apply Ruler Configuration

```bash
ruler apply --nested
```

### 3. Test GameBuilderCrew

```bash
cd python/crew_agents
export OPENROUTER_API_KEY=your-key
uv run crew_agents build "SwimmingComponent with velocity, stamina, dive_depth"
```

### 4. Verify ConPort Connection

```bash
# Check process-compose status
process-compose ps

# View ConPort logs
process-compose logs conport
```

---

## Environment Requirements

```bash
# Required environment variables
export OPENROUTER_API_KEY="your-openrouter-key"
export MESHY_API_KEY="your-meshy-key"         # For asset generation
export GITHUB_PERSONAL_ACCESS_TOKEN="your-gh-token"  # Optional

# Python 3.13 (project standard)
python --version  # Should be 3.13+
```

---

## Troubleshooting

### ConPort Not Responding
```bash
# Check if uvx can run ConPort
uvx --from context-portal-mcp conport-mcp --help

# Restart via process-compose
process-compose restart conport
```

### Database Not Found
Database auto-creates on first tool call. If missing:
```bash
# Trigger creation with any ConPort call
# Or manually create directory
mkdir -p ./context_portal
```

### MCP Server Not Configured
```bash
# Regenerate MCP configuration
ruler apply --nested --agents cursor
```

---

## Documentation References

- **ConPort Docs**: https://github.com/GreatScottyMac/context-portal
- **Ruler Docs**: https://github.com/ruler-ai/ruler
- **CrewAI Docs**: https://docs.crewai.com
- **Project Brief**: `/workspace/projectBrief.md`
- **ConPort Usage**: `/workspace/.ruler/conport_usage.md`
