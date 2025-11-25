# ConPort System Patterns Export

## Pattern: ConPort MCP Integration
- **ID**: SP-001
- **Name**: ConPort MCP Server Configuration
- **Description**: Standard pattern for configuring ConPort as an MCP server in Ruler
- **Tags**: conport, mcp, ruler, configuration
- **Code**:
```toml
[mcp_servers.conport]
command = "uvx"
args = [
  "--from", "context-portal-mcp", 
  "conport-mcp", 
  "--mode", "stdio",
  "--log-level", "INFO"
]

[mcp_servers.conport.env]
CONPORT_FILES = "projectBrief.md"
```

## Pattern: Background Agent Initialization
- **ID**: SP-002
- **Name**: ConPort Agent Initialization Sequence
- **Description**: Standard initialization sequence for AI agents to load ConPort context
- **Tags**: conport, agents, initialization
- **Code**:
```yaml
initialization_sequence:
  - step: 1
    action: "Check for context_portal/context.db"
  - step: 2
    condition: "db exists"
    actions:
      - get_product_context
      - get_active_context
      - get_decisions(limit: 5)
      - get_progress(limit: 5)
      - get_system_patterns
  - step: 3
    output: "[CONPORT_ACTIVE]"
```

## Pattern: Process-Compose Service Definition
- **ID**: SP-003
- **Name**: ConPort Process-Compose Configuration
- **Description**: Standard process-compose definition for running ConPort as background service
- **Tags**: conport, process-compose, infrastructure
- **Code**:
```yaml
conport:
  command: "uvx --from context-portal-mcp conport-mcp --mode stdio --workspace_id ${PWD} --log-file ./logs/conport.log --log-level INFO"
  working_dir: "."
  availability:
    restart: "always"
  log_configuration:
    rolling: "daily"
    max_size_mb: 20
    max_backups: 7
```

## Pattern: CrewAI Game Builder with Custom Tools
- **ID**: SP-004
- **Name**: Game Builder Crew Pattern
- **Description**: CrewAI crew structure for code generation with custom file tools
- **Tags**: crewai, code-generation, tools
- **Code**:
```python
@CrewBase
class GameBuilderCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.code_writer = GameCodeWriterTool()
        self.code_reader = GameCodeReaderTool()
        self.dir_lister = DirectoryListTool()

    @agent
    def senior_typescript_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_typescript_engineer"],
            llm=get_llm(),
            tools=[self.code_writer, self.code_reader, self.dir_lister],
            allow_code_execution=True,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            planning=True,
            memory=True,
        )
```

## Pattern: Custom File Tool with Safety Checks
- **ID**: SP-005
- **Name**: Safe File Write Tool Pattern
- **Description**: Pattern for creating CrewAI tools with directory and extension validation
- **Tags**: crewai, tools, safety
- **Code**:
```python
ALLOWED_WRITE_DIRS = [
    "client/src/ecs/components",
    "client/src/components",
    "shared/contracts",
]
ALLOWED_EXTENSIONS = {".ts", ".tsx", ".json", ".md"}

class GameCodeWriterTool(BaseTool):
    def _run(self, file_path: str, content: str) -> str:
        # Validate directory
        if not any(file_path.startswith(d) for d in ALLOWED_WRITE_DIRS):
            return f"Error: Directory not allowed"
        
        # Validate extension
        if Path(file_path).suffix not in ALLOWED_EXTENSIONS:
            return f"Error: Extension not allowed"
        
        # Check for path traversal
        if ".." in file_path:
            return f"Error: Path traversal not allowed"
        
        # Write file
        full_path = workspace_root / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        return f"Successfully wrote {file_path}"
```
