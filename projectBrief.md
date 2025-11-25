# Rivermarsh - Complete Project Brief

## What Is Rivermarsh?

Rivermarsh is a **mobile-first 3D game** where players control a river otter navigating diverse wetland biomes. Built with modern web technologies and an **AI-first development workflow**.

---

## Part 1: The Game

### Gameplay Overview
- **Player Character**: River otter with swimming, diving, and foraging abilities
- **Environment**: Procedurally-generated marshland with multiple biomes
- **Core Loop**: Explore → Forage → Survive → Discover
- **Combat**: Natural predator/prey interactions (herons, pike, snapping turtles)

### Biomes
| Biome | Description | Hazards |
|-------|-------------|---------|
| Reed Marsh | Dense reeds, shallow water | Herons, limited visibility |
| Open River | Fast currents, deep water | Pike, strong current |
| Beaver Dam | Complex structures | Territorial beavers |
| Mudflat | Exposed areas, tidal | Birds of prey, exposure |

### Performance Targets
- **60 FPS** on iPhone 13 / mid-tier Android
- **< 100 draw calls** per frame
- **< 500k vertices** per frame
- **< 200MB** texture memory

---

## Part 2: Runtime Architecture

### Frontend Stack
```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  React Three Fiber (R3F) - 3D Rendering                      │
│  └── client/src/components/                                  │
│      ├── Player.tsx          # Otter character               │
│      ├── MarshlandTerrain.tsx # Procedural terrain           │
│      └── RivermarshGame.tsx  # Main game scene               │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     SIMULATION LAYER                         │
│  Yuka.js AI - Steering Behaviors & State Machines            │
│  └── client/src/ai/                                          │
│      └── yukaManager.ts      # Entity manager integration    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                        DATA LAYER                            │
│  Miniplex ECS - Entity Component System                      │
│  └── client/src/ecs/                                         │
│      ├── world.ts            # ECS world instance            │
│      ├── components.ts       # Component definitions         │
│      └── components/                                         │
│          ├── BiomeComponent.ts                               │
│          └── CombatComponent.ts                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     STATE MANAGEMENT                         │
│  Zustand Stores                                              │
│  └── client/src/lib/stores/                                  │
│      └── useGame.ts          # Global game state             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| UI Framework | React 18 | Component rendering |
| 3D Engine | React Three Fiber | Three.js integration |
| ECS | Miniplex | Entity-component-system |
| AI | Yuka.js | Steering, pathfinding |
| State | Zustand | Global state management |
| Types | TypeScript (strict) | Type safety |
| Build | Vite 7 | Fast bundling |
| Mobile | Capacitor | iOS/Android deployment |

### Shared Contracts

All TypeScript interfaces live in `shared/contracts/`:
- `BiomeContract.ts` - Biome type definitions
- `SpeciesContract.ts` - Creature species types

These contracts are the **source of truth** for both frontend and backend.

---

## Part 3: Development Tools

### CrewAI - AI Agent Framework

CrewAI powers autonomous development through specialized agent crews:

```
python/crew_agents/
├── src/crew_agents/
│   ├── crews/
│   │   └── game_builder/      # Code-writing crew
│   │       ├── game_builder_crew.py
│   │       └── config/
│   │           ├── agents.yaml
│   │           └── tasks.yaml
│   ├── tools/
│   │   └── file_tools.py      # Safe file read/write
│   ├── config/
│   │   └── llm.py             # OpenRouter configuration
│   └── main.py                # CLI entry point
├── knowledge/                  # Working code patterns
│   ├── ecs_patterns/
│   ├── rendering_patterns/
│   └── game_components/
└── README.md
```

#### Running CrewAI

```bash
# Build a game component
cd python/crew_agents
uv run crew_agents build "SwimmingComponent with velocity, stamina, dive_depth"

# Train the crew with human feedback
uv run crew_agents train 5

# List available knowledge sources
uv run crew_agents list-knowledge

# Test file tools
uv run crew_agents test-tools
```

#### CrewAI Configuration

- **LLM**: OpenRouter with `openrouter/auto` model
- **API Key**: `OPENROUTER_API_KEY` environment variable
- **Features Enabled**:
  - `planning=True` - Step-by-step task planning
  - `memory=True` - Learning from interactions
  - `allow_code_execution=True` - Code generation capability

### Meshy API - 3D Asset Generation

```
python/mesh_toolkit/
├── src/mesh_toolkit/
│   ├── client.py              # Meshy API client
│   └── services/
│       └── factory.py         # Service factory
└── README.md
```

Generates 3D creature models via text prompts with webhook-based HITL review.

### Process-Compose - Multi-Process Orchestration

```bash
# Start all background processes
process-compose up -d

# View logs
process-compose logs

# Check status
process-compose ps

# Stop all
process-compose down
```

Processes defined in `process-compose.yaml`:
- `conport` - Context Portal memory bank
- `rivermarsh_crew` - Main development crew
- `crew_monitor` - Progress monitoring

---

## Part 4: AI Agent Configuration with Ruler

### What Is Ruler?

Ruler generates consistent AI agent instructions across multiple IDEs and tools. Configuration lives in `.ruler/ruler.toml`.

### Applying Rules

```bash
# Install ruler
cargo install ruler-ai

# Apply rules to all agents
ruler apply --nested

# Apply to specific agents
ruler apply --agents cursor,claude

# Dry run (preview changes)
ruler apply --dry-run
```

### Configuration Structure

```toml
# .ruler/ruler.toml

# Default agents to configure
default_agents = ["copilot", "claude", "cursor", "cline", "windsurf"]

# Enable nested rule loading (component-specific rules)
nested = true

# MCP Server Configuration (shared by all agents)
[mcp]
enabled = true
merge_strategy = "merge"

# MCP Servers
[mcp_servers.conport]
command = "uvx"
args = ["--from", "context-portal-mcp", "conport-mcp"]

[mcp_servers.conport.env]
CONPORT_FILES = "projectbrief.md"

[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "./"]

# Agent-specific settings
[agents.cursor]
enabled = true

[agents.cursor.mcp]
enabled = true
merge_strategy = "merge"
```

### Rule Loading Order

1. `/AGENTS.md` - Root executive summary
2. `/.ruler/AGENTS.md` - Cross-cutting standards
3. `/.ruler/*.md` - ECS patterns, shaders, R3F guidelines
4. `/client/.ruler/AGENTS.md` - Client-specific rules
5. `/python/.ruler/AGENTS.md` - Python backend rules
6. `/python/crew_agents/.ruler/*.md` - CrewAI workflows
7. `/docs/.ruler/*.md` - Documentation standards
8. `/shared/.ruler/AGENTS.md` - Contracts & types

### Key Rule Files

| File | Purpose |
|------|---------|
| `.ruler/AGENTS.md` | TypeScript standards, error handling |
| `.ruler/ecs_patterns.md` | Miniplex ECS patterns |
| `.ruler/react_three_fiber.md` | R3F rendering guidelines |
| `.ruler/shaders.md` | GLSL shader development |
| `client/.ruler/AGENTS.md` | Frontend-specific rules |
| `python/.ruler/AGENTS.md` | Python standards |

---

## Part 5: Context Portal (ConPort) - Project Memory

### What Is ConPort?

ConPort is a **database-backed memory bank** for AI agents. It stores:
- Product Context (this brief, overall goals)
- Active Context (current sprint focus)
- Decisions (architectural choices)
- Progress (task tracking)
- System Patterns (coding patterns)
- Custom Data (glossary, specs)

### Database Location

```
/workspace/context_portal/context.db
```

### Initialization

ConPort auto-initializes on first use. To bootstrap with this brief:

1. ConPort reads `projectBrief.md` on startup
2. Content imported to Product Context
3. Available to all AI agents via MCP

### MCP Integration

ConPort is configured as an MCP server in `.ruler/ruler.toml`:

```toml
[mcp_servers.conport]
command = "uvx"
args = ["--from", "context-portal-mcp", "conport-mcp"]

[mcp_servers.conport.env]
CONPORT_FILES = "projectbrief.md"
```

### Running Standalone

```bash
# Start ConPort server
uvx --from context-portal-mcp conport-mcp \
  --mode stdio \
  --workspace_id "$(pwd)" \
  --log-file ./logs/conport.log \
  --log-level INFO
```

### Via Process-Compose

```bash
# Start with all services
process-compose up -d

# Check ConPort logs
process-compose logs conport
```

---

## Part 6: Directory Structure

```
/workspace/
├── AGENTS.md                    # Root AI instructions
├── projectBrief.md              # This file (ConPort source)
├── process-compose.yaml         # Multi-process orchestration
│
├── .ruler/
│   ├── ruler.toml               # Ruler configuration
│   ├── AGENTS.md                # Cross-cutting standards
│   ├── ecs_patterns.md          # ECS patterns
│   ├── react_three_fiber.md     # R3F guidelines
│   └── shaders.md               # GLSL development
│
├── .cursor/
│   ├── Dockerfile               # Development container
│   ├── docker-compose.yml       # Container orchestration
│   ├── environment.json         # Build configuration
│   ├── rules/                   # Cursor-specific rules
│   │   ├── 00-loader.mdc        # Rule loader
│   │   └── 10-background-agent-conport.mdc
│   └── supervisord.conf         # Process supervision
│
├── client/                      # React Three Fiber frontend
│   ├── src/
│   │   ├── components/          # R3F components
│   │   ├── ecs/                 # Miniplex ECS
│   │   ├── ai/                  # Yuka.js integration
│   │   └── lib/stores/          # Zustand stores
│   └── .ruler/
│       └── AGENTS.md            # Client-specific rules
│
├── python/                      # Python tooling
│   ├── crew_agents/             # CrewAI development crews
│   │   ├── src/crew_agents/
│   │   ├── knowledge/           # Code patterns for agents
│   │   └── README.md
│   ├── mesh_toolkit/            # Meshy API integration
│   └── .ruler/
│       └── AGENTS.md            # Python standards
│
├── shared/
│   ├── contracts/               # TypeScript interfaces
│   │   ├── BiomeContract.ts
│   │   └── SpeciesContract.ts
│   └── backend/
│       └── ecs_world/           # Backend ECS utilities
│
├── docs/
│   ├── architecture/            # Architecture docs
│   ├── asset_generation/        # Asset pipeline docs
│   └── troubleshooting/         # Runbooks
│
├── .github/
│   └── workflows/               # CI/CD pipelines
│       ├── ci.yml
│       ├── crewai-orchestrator.yml
│       └── meshy-asset-pipeline.yml
│
└── context_portal/              # ConPort database (auto-created)
    └── context.db
```

---

## Part 7: Getting Started

### Prerequisites

- Node.js 24+ with pnpm
- Python 3.13+ with uv
- Docker (optional, for containerized dev)

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-org/rivermarsh.git
cd rivermarsh

# Install Node dependencies
pnpm install

# Install Python dependencies
cd python && uv sync && cd ..

# Apply Ruler configuration
ruler apply --nested

# Start development server
pnpm dev

# Start background processes (including ConPort)
process-compose up -d
```

### Environment Variables

```bash
# Required for CrewAI
export OPENROUTER_API_KEY="your-key"

# Required for Meshy
export MESHY_API_KEY="your-key"

# Optional GitHub integration
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token"
```

---

## Part 8: Development Workflow

### Human + AI Collaboration

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Human defines  │────▶│  CrewAI agents  │────▶│  Human reviews  │
│  contracts &    │     │  generate code  │     │  & integrates   │
│  requirements   │     │  from patterns  │     │  to frontend    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         └──────────────────────┴───────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │   ConPort Memory    │
                    │   (decisions,       │
                    │   progress, context)│
                    │                     │
                    └─────────────────────┘
```

### Typical Session

1. **Initialize**: AI agent loads ConPort context
2. **Plan**: Review active context, identify next task
3. **Act**: Generate code using knowledge patterns
4. **Review**: Human reviews, provides feedback
5. **Sync**: Update ConPort with decisions/progress
6. **Iterate**: Repeat until sprint complete

### ConPort Sync Command

Tell any AI agent:
```
Sync ConPort
```

This triggers a full synchronization of the conversation into ConPort memory.

---

## Contact & Resources

- **Repository**: `https://github.com/your-org/rivermarsh`
- **Ruler Docs**: `https://github.com/ruler-ai/ruler`
- **ConPort Docs**: `https://github.com/GreatScottyMac/context-portal`
- **CrewAI Docs**: `https://docs.crewai.com`
