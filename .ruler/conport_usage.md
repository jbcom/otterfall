# ConPort (Context Portal) Usage Guide

## Overview

ConPort is the project's **memory bank** - a database-backed MCP server that stores structured context for AI agents. All AI agents (Cursor, Claude, Copilot, CrewAI) share the same ConPort instance.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    AI AGENTS (Consumers)                      │
│  Cursor │ Claude │ Copilot │ CrewAI │ Cline │ Windsurf       │
└────────────────────────┬─────────────────────────────────────┘
                         │ MCP Protocol
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    ConPort MCP Server                         │
│  uvx --from context-portal-mcp conport-mcp                    │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              SQLite Database (per workspace)                  │
│  /workspace/context_portal/context.db                         │
└──────────────────────────────────────────────────────────────┘
```

## Configuration

ConPort is configured in `.ruler/ruler.toml`:

```toml
[mcp_servers.conport]
command = "uvx"
args = ["--from", "context-portal-mcp", "conport-mcp"]

[mcp_servers.conport.env]
CONPORT_FILES = "projectbrief.md"
```

After running `ruler apply --nested`, this configuration is distributed to all enabled agents.

## Database Schema

ConPort stores the following entity types:

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| Product Context | Project-wide goals, architecture | JSON blob |
| Active Context | Current sprint focus, open issues | JSON blob |
| Decisions | Architectural/implementation choices | summary, rationale, tags |
| Progress | Task tracking | status, description, parent_id |
| System Patterns | Coding patterns | name, description, tags |
| Custom Data | Flexible key-value store | category, key, value |
| Links | Knowledge graph relationships | source, target, relationship |

## Agent Initialization Protocol

Every AI agent session MUST begin with:

### 1. Status Declaration
```
[CONPORT_ACTIVE]  - Database accessible
[CONPORT_INACTIVE] - Database unavailable
```

### 2. Context Loading Sequence
```yaml
# Load in this order:
1. get_product_context      # Overall project goals
2. get_active_context       # Current sprint focus
3. get_decisions(limit: 5)  # Recent decisions
4. get_progress(limit: 5)   # Recent progress
5. get_system_patterns      # Coding patterns
6. get_custom_data(category: "critical_settings")
7. get_custom_data(category: "ProjectGlossary")
```

### 3. New Workspace Bootstrap
If no `context.db` exists:
1. Check for `projectBrief.md` in workspace root
2. If found, offer to import to Product Context
3. Create initial Active Context with `mode: "PLAN"`

## Tool Reference

### Context Management

```yaml
# Get product context
get_product_context:
  workspace_id: "/workspace"

# Update product context (patch mode - partial update)
update_product_context:
  workspace_id: "/workspace"
  patch_content:
    new_key: "value"
    remove_key: "__DELETE__"  # Special sentinel to delete

# Get active context
get_active_context:
  workspace_id: "/workspace"

# Update active context
update_active_context:
  workspace_id: "/workspace"
  patch_content:
    current_focus: "Implementing SwimmingComponent"
    mode: "ACT"
    open_issues: ["Performance optimization needed"]
```

### Decision Logging

```yaml
# Log a new decision
log_decision:
  workspace_id: "/workspace"
  summary: "Use Miniplex ECS for entity management"
  rationale: "Lightweight, TypeScript-native, good React integration"
  implementation_details: "Components defined in client/src/ecs/components.ts"
  tags: ["architecture", "ecs", "frontend"]

# Search decisions by keyword
search_decisions_fts:
  workspace_id: "/workspace"
  query_term: "ECS component"
  limit: 10

# Get decisions by tag
get_decisions:
  workspace_id: "/workspace"
  tags_filter_include_any: ["architecture", "performance"]
  limit: 5
```

### Progress Tracking

```yaml
# Log new task
log_progress:
  workspace_id: "/workspace"
  status: "IN_PROGRESS"  # TODO, IN_PROGRESS, DONE, BLOCKED
  description: "Implement water shader for MarshlandTerrain"
  linked_item_type: "decision"
  linked_item_id: "42"

# Update existing task
update_progress:
  workspace_id: "/workspace"
  progress_id: 123
  status: "DONE"

# Get progress by status
get_progress:
  workspace_id: "/workspace"
  status_filter: "IN_PROGRESS"
  limit: 10
```

### System Patterns

```yaml
# Log a coding pattern
log_system_pattern:
  workspace_id: "/workspace"
  name: "ECS Component Factory"
  description: |
    Create factory functions for common entity archetypes:
    ```typescript
    export function createOtter(position: Vector3): Entity {
      return world.add({
        transform: { position, rotation: new Quaternion(), scale: new Vector3(1,1,1) },
        health: { current: 100, max: 100, invulnerable: false },
        species: { type: 'otter', variant: 'river' }
      });
    }
    ```
  tags: ["ecs", "miniplex", "factory"]

# Get patterns by tag
get_system_patterns:
  workspace_id: "/workspace"
  tags_filter_include_any: ["ecs"]
```

### Custom Data

```yaml
# Store glossary term
log_custom_data:
  workspace_id: "/workspace"
  category: "ProjectGlossary"
  key: "ECS"
  value:
    definition: "Entity Component System - data-oriented architecture"
    related_terms: ["Miniplex", "Component", "System"]

# Store artifact reference
log_custom_data:
  workspace_id: "/workspace"
  category: "artifacts"
  key: "architecture_doc"
  value:
    type: "doc"
    path: "docs/architecture/ECS_SYSTEMS.md"
    tags: ["architecture", "ecs"]

# Search custom data
search_custom_data_value_fts:
  workspace_id: "/workspace"
  query_term: "value_text:\"definition\""
  category_filter: "ProjectGlossary"
  limit: 10
```

### Knowledge Graph Links

```yaml
# Link decision to progress
link_conport_items:
  workspace_id: "/workspace"
  source_item_type: "decision"
  source_item_id: "42"
  target_item_type: "progress_entry"
  target_item_id: "123"
  relationship_type: "IMPLEMENTS"
  description: "This task implements the ECS decision"

# Valid relationship types:
# IMPLEMENTS, BLOCKED_BY, VERIFIES, DEPENDS_ON, 
# RELATED_TO, CLARIFIES, RESOLVES, DERIVED_FROM, TRACKS

# Get linked items
get_linked_items:
  workspace_id: "/workspace"
  item_type: "decision"
  item_id: "42"
```

## Sync Protocol

Trigger with: **"Sync ConPort"** or **"ConPort Sync"**

Agent behavior:
1. Output `[CONPORT_SYNCING]`
2. Review entire conversation history
3. Extract and log:
   - New decisions
   - Progress updates
   - Context changes
   - Pattern discoveries
   - Item relationships
4. Confirm: "ConPort synchronized"

## Export/Import

```yaml
# Export to markdown (for review/backup)
export_conport_to_markdown:
  workspace_id: "/workspace"
  output_path: "./conport_export/2024-01-15/"

# Import from markdown
import_markdown_to_conport:
  workspace_id: "/workspace"
  input_path: "./conport_export/2024-01-15/"
```

## Process-Compose Integration

ConPort runs as a background service:

```yaml
# process-compose.yaml
processes:
  conport:
    command: "uvx --from context-portal-mcp conport-mcp --mode stdio --workspace_id ${PWD}"
    availability:
      restart: "always"
```

Commands:
```bash
process-compose up -d        # Start all services
process-compose logs conport # View ConPort logs
process-compose ps           # Check status
```

## Best Practices

### DO
- ✅ Always include `workspace_id` in every call
- ✅ Use `patch_content` for partial context updates
- ✅ Tag decisions consistently for searchability
- ✅ Link related items to build knowledge graph
- ✅ Export before major refactors (backup)
- ✅ Use semantic search for conceptual queries

### DON'T
- ❌ Store large code blocks (use file references instead)
- ❌ Duplicate information across entities
- ❌ Overwrite full context when patching suffices
- ❌ Skip initialization sequence
- ❌ Ignore `[CONPORT_INACTIVE]` state

## Troubleshooting

### Database Not Found
```bash
# Check if database exists
ls -la ./context_portal/context.db

# Database auto-creates on first ConPort tool call
```

### MCP Connection Failed
```bash
# Test ConPort server directly
uvx --from context-portal-mcp conport-mcp --help

# Check process-compose logs
process-compose logs conport
```

### Context Not Loading
```yaml
# Verify workspace_id is absolute path
get_product_context:
  workspace_id: "/workspace"  # NOT "./workspace"
```

## Related Documentation

- [Context Portal GitHub](https://github.com/GreatScottyMac/context-portal)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Ruler Configuration](.ruler/ruler.toml)
- [Background Agent Rules](.cursor/rules/10-background-agent-conport.mdc)
