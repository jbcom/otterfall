# ConPort Custom Data Export

## Category: ProjectGlossary

### ConPort
```json
{
  "category": "ProjectGlossary",
  "key": "ConPort",
  "value": {
    "definition": "Context Portal - Database-backed MCP server for structured project memory",
    "full_name": "Context Portal MCP",
    "repository": "https://github.com/GreatScottyMac/context-portal",
    "related_terms": ["MCP", "Memory Bank", "RAG", "Knowledge Graph"]
  }
}
```

### Ruler
```json
{
  "category": "ProjectGlossary",
  "key": "Ruler",
  "value": {
    "definition": "Tool for generating consistent AI agent instructions across multiple IDEs",
    "config_file": ".ruler/ruler.toml",
    "command": "ruler apply --nested",
    "related_terms": ["MCP", "Agent Rules", "IDE Configuration"]
  }
}
```

### MCP
```json
{
  "category": "ProjectGlossary",
  "key": "MCP",
  "value": {
    "definition": "Model Context Protocol - Standard for AI assistants to interact with external tools",
    "specification": "https://modelcontextprotocol.io/",
    "related_terms": ["ConPort", "Ruler", "Tool Servers"]
  }
}
```

### Process-Compose
```json
{
  "category": "ProjectGlossary",
  "key": "ProcessCompose",
  "value": {
    "definition": "Multi-process orchestration tool similar to docker-compose but for native processes",
    "repository": "https://github.com/F1bonacc1/process-compose",
    "config_file": "process-compose.yaml",
    "related_terms": ["Background Services", "Service Orchestration"]
  }
}
```

### GameBuilderCrew
```json
{
  "category": "ProjectGlossary",
  "key": "GameBuilderCrew",
  "value": {
    "definition": "CrewAI crew that generates actual game code using knowledge patterns and custom file tools",
    "location": "python/crew_agents/src/crew_agents/crews/game_builder/",
    "agents": ["senior_typescript_engineer", "qa_engineer", "chief_engineer"],
    "related_terms": ["CrewAI", "Code Generation", "Knowledge Base"]
  }
}
```

### ECS
```json
{
  "category": "ProjectGlossary",
  "key": "ECS",
  "value": {
    "definition": "Entity Component System - Data-oriented architecture pattern for game development",
    "implementation": "Miniplex",
    "location": "client/src/ecs/",
    "related_terms": ["Miniplex", "Component", "Entity", "System"]
  }
}
```

## Category: critical_settings

### ConPort Configuration
```json
{
  "category": "critical_settings",
  "key": "conport_config",
  "value": {
    "database_path": "./context_portal/context.db",
    "mcp_command": "uvx --from context-portal-mcp conport-mcp",
    "log_file": "./logs/conport.log",
    "log_level": "INFO",
    "auto_detect_workspace": true
  }
}
```

### Python Version
```json
{
  "category": "critical_settings",
  "key": "python_version",
  "value": {
    "required": "3.13",
    "rationale": "Project standard, onnxruntime compatibility",
    "configured_in": [
      ".github/workflows/ci.yml",
      ".github/workflows/crewai-orchestrator.yml",
      ".github/workflows/meshy-asset-pipeline.yml",
      "python/pyproject.toml",
      "python/crew_agents/pyproject.toml",
      "python/mesh_toolkit/pyproject.toml"
    ]
  }
}
```

### LLM Configuration
```json
{
  "category": "critical_settings",
  "key": "llm_config",
  "value": {
    "provider": "OpenRouter",
    "model": "openrouter/auto",
    "api_base": "https://openrouter.ai/api/v1",
    "env_var": "OPENROUTER_API_KEY",
    "config_location": "python/crew_agents/src/crew_agents/config/llm.py"
  }
}
```

## Category: artifacts

### Session Documentation
```json
{
  "category": "artifacts",
  "key": "session_2025_11_25",
  "value": {
    "type": "doc",
    "description": "ConPort integration session - established AI memory infrastructure",
    "files_created": [
      "projectBrief.md",
      ".cursor/rules/10-background-agent-conport.mdc",
      ".ruler/conport_usage.md",
      "conport_export/session-2025-11-25/*"
    ],
    "files_modified": [
      ".cursor/Dockerfile",
      "process-compose.yaml",
      ".ruler/ruler.toml"
    ],
    "tags": ["session", "infrastructure", "conport"]
  }
}
```

### Game Builder Crew Knowledge Base
```json
{
  "category": "artifacts",
  "key": "game_builder_knowledge",
  "value": {
    "type": "knowledge_base",
    "description": "Working code patterns extracted from client/src for CrewAI agents",
    "location": "python/crew_agents/knowledge/",
    "subdirectories": [
      "ecs_patterns/components.md",
      "rendering_patterns/r3f_components.md",
      "game_components/architecture.md"
    ],
    "purpose": "RAG source for GameBuilderCrew code generation",
    "tags": ["crewai", "knowledge", "ecs", "r3f"]
  }
}
```
