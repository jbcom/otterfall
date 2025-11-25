# ConPort Decisions Export

## Decision: Integrate Context Portal (ConPort) as Project Memory Bank
- **ID**: D-001
- **Summary**: Adopted ConPort MCP server as the centralized memory bank for all AI agents
- **Rationale**: ConPort provides structured database-backed storage for project context, enabling RAG and knowledge graph capabilities. Unlike file-based memory, it offers queryable, versioned, and linkable context storage.
- **Implementation Details**: 
  - ConPort configured in `.ruler/ruler.toml` as MCP server
  - Database stored at `./context_portal/context.db`
  - Integrated with process-compose for background operation
  - Created `projectBrief.md` as initialization source
- **Tags**: architecture, tooling, memory, mcp, conport
- **Timestamp**: 2025-11-25

## Decision: Add Process-Compose to Development Container
- **ID**: D-002
- **Summary**: Added process-compose v1.51.1 to the Cursor Dockerfile for multi-process orchestration
- **Rationale**: Process-compose enables running ConPort and other background services (CrewAI crews, monitors) in parallel with proper dependency management and logging.
- **Implementation Details**:
  - Downloaded from GitHub releases in Dockerfile
  - Installed to `/usr/local/bin/process-compose`
  - Added ConPort process definition to `process-compose.yaml`
- **Tags**: tooling, docker, infrastructure, process-compose
- **Timestamp**: 2025-11-25

## Decision: Implement Game Builder Crew for Code Generation
- **ID**: D-003
- **Summary**: Created GameBuilderCrew with custom file tools for actual code generation
- **Rationale**: Previous CrewAI setup generated documents but not actual game code. Game Builder Crew uses knowledge sources from working code patterns and custom file tools to write TypeScript directly to the codebase.
- **Implementation Details**:
  - Knowledge base in `python/crew_agents/knowledge/` with ECS patterns, R3F rendering, game architecture
  - Custom tools: GameCodeWriterTool, GameCodeReaderTool, DirectoryListTool
  - Agents: senior_typescript_engineer (code writer), qa_engineer (reviewer), chief_engineer (evaluator)
  - Features: planning=True, memory=True, allow_code_execution=True
- **Tags**: crewai, code-generation, tooling, agents
- **Timestamp**: 2025-11-25

## Decision: Use Python 3.13 Across All Configurations
- **ID**: D-004
- **Summary**: Standardized on Python 3.13 for all Python tooling
- **Rationale**: Python 3.11 was incorrectly set in some workflow files, causing inconsistency with the project's target of 3.13. Dependencies like onnxruntime require specific Python versions.
- **Implementation Details**:
  - Updated PYTHON_VERSION in: ci.yml, crewai-orchestrator.yml, meshy-asset-pipeline.yml
  - Updated requires-python in: python/pyproject.toml, crew_agents/pyproject.toml, mesh_toolkit/pyproject.toml
  - Updated ruff target-version to py313
- **Tags**: python, ci, configuration, dependencies
- **Timestamp**: 2025-11-25

## Decision: Create Comprehensive Cursor Rules for Background Agent ConPort Operation
- **ID**: D-005
- **Summary**: Established `.cursor/rules/10-background-agent-conport.mdc` with full ConPort integration protocol
- **Rationale**: Background agents need structured initialization and operation patterns to effectively use ConPort memory. Rule file ensures consistent behavior across sessions.
- **Implementation Details**:
  - Status prefix requirement ([CONPORT_ACTIVE]/[CONPORT_INACTIVE])
  - Initialization sequence with database checks
  - Tool usage examples for all ConPort operations
  - Sync routine for conversation-to-database synchronization
  - Error handling and fallback patterns
- **Tags**: cursor, rules, agents, conport, automation
- **Timestamp**: 2025-11-25
