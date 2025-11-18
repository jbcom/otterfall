# CrewAI Agent Usage Guide

## Overview

This project uses CrewAI agents with OpenRouter for autonomous game system development. Agents run as long-running background processes managed by `process-compose`.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    process-compose.yaml                      │
│  Orchestrates all CrewAI tasks as long-running processes    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ├─► Batch 1 (Parallel)
                   │   ├─► ecs_component_schemas
                   │   └─► dfu_data_analysis
                   │
                   └─► Sequential Tasks (Depends on Batch 1)
                       ├─► yuka_ai_integration
                       ├─► terrain_water_rendering
                       └─► quest_dialogue_systems
```

## Environment Setup

Required environment variables (set in `.envrc`):

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export MESHY_API_KEY="msy_..."
export OPENAI_API_BASE="https://openrouter.ai/api/v1"
export OPENAI_MODEL_NAME="openrouter/auto"
```

These are automatically loaded by `process-compose.yaml`.

## Agent Roles

### Technical Director (Manager)
- **Role**: Coordinates all specialist agents
- **Delegation**: Yes
- **Tools**: All MCP tools
- **Reasoning**: Up to 5 attempts
- **Max Iterations**: 40

### ECS Architect
- **Role**: Design type-safe ECS systems with Miniplex
- **Delegation**: No
- **Tools**: Code editing, docs, filesystem
- **Specialization**: TypeScript, game architecture

### Yuka AI Engineer
- **Role**: Implement creature AI with Yuka.js
- **Delegation**: No
- **Tools**: Code editing, testing, docs
- **Specialization**: Steering behaviors, state machines

### Rendering Engineer
- **Role**: Build R3F scenes with custom shaders
- **Delegation**: No
- **Tools**: Code editing, Vite dev server, docs
- **Specialization**: GLSL, Three.js, post-processing

### Systems Engineer
- **Role**: Implement game mechanics (quests, inventory, combat)
- **Delegation**: No
- **Tools**: Code editing, database, docs
- **Specialization**: Game systems, RPG mechanics

### DFU Analyst
- **Role**: Parse Daggerfall Unity data to natural world
- **Delegation**: No
- **Tools**: Filesystem, Python execution, docs
- **Specialization**: Legacy game data extraction

### QA Tester
- **Role**: Ensure performance and correctness
- **Delegation**: No
- **Tools**: Playwright, testing, profiling
- **Specialization**: Mobile performance, TypeScript validation

### Chief Architect
- **Role**: Maintain architectural vision and docs
- **Delegation**: No
- **Tools**: All MCP tools, Context7
- **Specialization**: Documentation, code review

## Running Tasks

### Start All Tasks

```bash
process-compose up
```

This starts all tasks defined in `process-compose.yaml` with automatic:
- Log rotation (daily, max 50MB, 7 backups)
- Restart on failure (max 3 attempts)
- Dependency management (sequential tasks wait for Batch 1)

### Start Specific Task

```bash
process-compose up ecs_component_schemas
```

### Monitor Progress

```bash
# Watch all logs
tail -f logs/crewai/*.log

# Monitor specific task
tail -f logs/crewai/ecs_component_schemas.log

# Check task status
uv run python python/scripts/monitor_crew_progress.py
```

### Stop Tasks

```bash
process-compose down
```

## Task Definitions

### Batch 1: Foundation (Parallel)

#### ecs_component_schemas
**Goal**: Generate TypeScript component definitions for Miniplex ECS

**Deliverables**:
- `shared/backend/ecs_world/components/*.ts` - All component types
- Unit tests for each component
- README with usage examples

**Expected Output**: Type-safe component schemas that match `client/src/ecs/components/`

#### dfu_data_analysis
**Goal**: Parse Daggerfall Unity creature/terrain data

**Deliverables**:
- `shared/backend/dfu_analysis/data/*.json` - Normalized DFU data
- Species mapping matrix (DFU → Rivermarsh)
- Python parser scripts

**Expected Output**: JSON data packs for all 28 species

### Sequential Tasks (Post-Batch 1)

#### yuka_ai_integration
**Dependencies**: ecs_component_schemas, dfu_data_analysis

**Goal**: Implement Yuka AI bridges for ECS entities

**Deliverables**:
- `shared/backend/yuka_ai/` - Pooled bridge system
- State machines for 3+ species
- Performance tests

#### terrain_water_rendering
**Dependencies**: ecs_component_schemas

**Goal**: Build SDF rendering pipeline

**Deliverables**:
- `shared/backend/rendering_pipeline/sdf/` - Water/fog shaders
- Instancing system for grass/reeds
- LOD management

#### quest_dialogue_systems
**Dependencies**: ecs_component_schemas, dfu_data_analysis

**Goal**: Implement RPG systems

**Deliverables**:
- `shared/backend/rpg_systems/quests/` - Quest engine
- `shared/backend/rpg_systems/dialogue/` - Dialogue trees
- Integration with ECS

## Log Management

### Log Structure

```
logs/crewai/
├── ecs_component_schemas.log       # Rolling daily logs
├── dfu_data_analysis.log
├── yuka_ai_integration.log
├── terrain_water_rendering.log
└── quest_dialogue_systems.log
```

### Log Rotation

- **Frequency**: Daily
- **Max Size**: 50MB per file
- **Retention**: 7 backups
- **Format**: Timestamped entries with task context

### Reading Logs

```bash
# Latest entries
tail -n 100 logs/crewai/ecs_component_schemas.log

# Follow live
tail -f logs/crewai/ecs_component_schemas.log

# Search for errors
grep ERROR logs/crewai/*.log

# Search for completions
grep "Task completed" logs/crewai/*.log
```

## Configuration Files

### crew_config/agents.yaml
Defines all 8 agents with their roles, goals, backstories, and capabilities.

### crew_config/tasks.yaml
Defines all tasks with descriptions, expected outputs, and tool requirements.

### crew_config/tasks_batch1.yaml
Subset of tasks for parallel Batch 1 execution.

### crew_config/mcp_servers.json
MCP server configurations for tool access (Git, GitHub, Vite, Playwright, etc.)

### process-compose.yaml
Orchestration config with dependencies, restarts, and logging.

## MCP Tools Available (Native Integration)

CrewAI uses **native MCP integration** - no custom adapters needed!

All MCP servers are defined in [`.ruler/ruler.toml`](../.ruler/ruler.toml) and shared across:
- **IDE Agents**: Cursor, Claude, Cline, Windsurf, etc.
- **CrewAI Agents**: Technical Director, ECS Architect, etc.

Run `ruler apply --nested` to generate `.mcp.json` from the Ruler config.

Available MCP servers:

- **ConPort**: Context Portal for project knowledge (6 tools)
- **Git**: Version control operations (2 tools)
- **GitHub**: Issue creation, PR management (1 tool)
- **Vite**: Dev server management (1 tool)
- **Playwright**: Browser testing (1 tool)
- **Filesystem**: File read/write (3 tools)
- **Memory**: Persistent knowledge storage (2 tools)
- **Material-UI/Context7**: Documentation fetching (2 tools)

Each agent gets a **filtered subset** based on their role.

## Integration Workflow

```
┌─────────────┐
│  CrewAI     │
│  Delivers   │
│  Backend    │
└──────┬──────┘
       │
       ├─► Unit Tests (Auto CI)
       │
       ├─► Schema Validation
       │
       ├─► Headless Simulation
       │
       ▼
┌─────────────┐
│   Agent     │
│  Reviews &  │
│  Integrates │
└──────┬──────┘
       │
       ├─► R3F Adapter Test
       │
       ├─► Prototype Integration
       │
       ├─► User Validation
       │
       ▼
┌─────────────┐
│   Merge to  │
│     Main    │
└─────────────┘
```

## Deliverable Standards

All CrewAI deliverables must include:

1. **README.md** - Usage documentation
2. **Unit Tests** - Passing test suite
3. **Type Exports** - TypeScript type definitions
4. **Integration Notes** - How to connect to frontend

## Troubleshooting

### Task Fails to Start

```bash
# Check logs
cat logs/crewai/[task_name].log

# Verify environment
env | grep OPENROUTER
env | grep MESHY
```

### Task Hangs

```bash
# Kill specific process
process-compose process stop [task_name]

# Restart
process-compose process start [task_name]
```

### Out of Memory

Tasks have automatic restart limits (max 3). If OOM persists:

1. Reduce reasoning attempts in `crew_config/agents.yaml`
2. Decrease max iterations
3. Split task into smaller subtasks

### API Rate Limits

OpenRouter auto-routing handles rate limits. If issues persist:

1. Check OpenRouter dashboard for credits
2. Verify `OPENROUTER_API_KEY` is valid
3. Consider upgrading OpenRouter plan

## Performance Metrics

Expected task durations:

- **ecs_component_schemas**: 15-30 minutes
- **dfu_data_analysis**: 20-40 minutes
- **yuka_ai_integration**: 30-60 minutes
- **terrain_water_rendering**: 40-90 minutes
- **quest_dialogue_systems**: 30-60 minutes

## Next Steps

After Batch 1 completes:

1. Review deliverables in `shared/backend/`
2. Run unit tests
3. Integrate with frontend prototypes
4. Start sequential tasks

## References

- [CrewAI Documentation](https://docs.crewai.com)
- [OpenRouter Models](https://openrouter.ai/models)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Process Compose](https://github.com/F1bonacc1/process-compose)

### Using a `projectbrief.md` File (Recommended)

[Permalink: Using a projectbrief.md File (Recommended)](https://github.com/GreatScottyMac/context-portal/tree/main#using-a-projectbriefmd-file-recommended)

1. **Create `projectbrief.md`:** In the root directory of your project workspace, create a file named `projectbrief.md`.

### Using a `projectbrief.md` File (Recommended)

[Permalink: Using a projectbrief.md File (Recommended)](https://github.com/GreatScottyMac/context-portal/tree/main#using-a-projectbriefmd-file-recommended)

1. **Create `projectbrief.md`:** In the root directory of your project workspace, create a file named `projectbrief.md`.

3. **Automatic Prompt for Import:** When an LLM agent using one of the provided ConPort custom instruction sets (e.g., `roo_code_conport_strategy`) initializes in the workspace, it is designed to:

   - Check for the existence of `projectbrief.md`.
   - If found, it will read the file and ask you if you'd like to import its content into the ConPort **Product Context**.

### Manual Initialization

[Permalink: Manual Initialization](https://github.com/GreatScottyMac/context-portal/tree/main#manual-initialization)

If `projectbrief.md` is not found, or if you choose not to import it:

### Using a `projectbrief.md` File (Recommended)

[Permalink: Using a projectbrief.md File (Recommended)](https://github.com/GreatScottyMac/context-portal/tree/main#using-a-projectbriefmd-file-recommended)

1. **Create `projectbrief.md`:** In the root directory of your project workspace, create a file named `projectbrief.md`.

### Using a `projectbrief.md` File (Recommended)

[Permalink: Using a projectbrief.md File (Recommended)](https://github.com/GreatScottyMac/context-portal/tree/main#using-a-projectbriefmd-file-recommended)

1. **Create `projectbrief.md`:** In the root directory of your project workspace, create a file named `projectbrief.md`.

3. **Automatic Prompt for Import:** When an LLM agent using one of the provided ConPort custom instruction sets (e.g., `roo_code_conport_strategy`) initializes in the workspace, it is designed to:

   - Check for the existence of `projectbrief.md`.
   - If found, it will read the file and ask you if you'd like to import its content into the ConPort **Product Context**.

### Manual Initialization

[Permalink: Manual Initialization](https://github.com/GreatScottyMac/context-portal/tree/main#manual-initialization)

If `projectbrief.md` is not found, or if you choose not to import it:

Update final reference in initialization section
By providing initial context, either through `projectbrief.md` or manual entry, you enable ConPort and the connected LLM agent to have a better foundational understanding of the project's Product Context.