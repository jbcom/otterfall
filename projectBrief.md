# Rivermarsh - Project Brief

## Overview

Rivermarsh is a **mobile-first 3D game** where the player controls a river otter navigating diverse biomes. The game combines:

- **React Three Fiber** for 3D rendering
- **Miniplex ECS** for entity-component-system architecture  
- **Yuka.js AI** for creature behaviors and steering
- **CrewAI** for autonomous AI-powered development tooling
- **Meshy API** for 3D asset generation

## Project Goals

1. **Playable MVP** - Otter character exploring a marshland environment
2. **AI-First Development** - CrewAI agents handle backend development
3. **Mobile Performance** - 60 FPS on mid-tier phones
4. **Content Generation** - Procedural creatures via Meshy 3D API

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  React Three Fiber Components (R3F)                         │
│  - client/src/components/ - Game rendering                  │
│  - Shader-based water, terrain, effects                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                     SIMULATION LAYER                         │
│  Yuka AI EntityManager                                       │
│  - client/src/ai/ - Steering behaviors                       │
│  - State machines for creature AI                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                        DATA LAYER                            │
│  Miniplex ECS World                                          │
│  - client/src/ecs/ - Components, Systems, Entities           │
│  - shared/contracts/ - TypeScript interfaces                 │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** (strict mode) - Type-safe development
- **React Three Fiber** - 3D rendering
- **Zustand** - State management
- **Miniplex** - ECS architecture

### Backend/Tooling
- **Python 3.13** - Backend tooling
- **CrewAI** - Autonomous AI agent framework
- **OpenRouter** - LLM API gateway
- **Meshy API** - 3D asset generation

### Build/CI
- **Vite 7** - Fast bundler
- **pnpm** - Package manager
- **GitHub Actions** - CI/CD
- **Capacitor** - Mobile deployment

## Directory Structure

```
/workspace/
├── client/                  # React Three Fiber frontend
│   └── src/
│       ├── components/      # R3F rendering components
│       ├── ecs/             # Miniplex ECS (components, entities, systems)
│       ├── ai/              # Yuka.js AI integration
│       └── lib/stores/      # Zustand state stores
├── python/                  # Python backend & tooling
│   ├── crew_agents/         # CrewAI development crews
│   │   ├── knowledge/       # Working code patterns for agents
│   │   ├── src/crew_agents/
│   │   │   ├── crews/       # Specialized agent teams
│   │   │   ├── tools/       # File manipulation tools
│   │   │   └── config/      # LLM configuration
│   │   └── README.md
│   └── mesh_toolkit/        # Meshy API integration
├── shared/                  # Shared contracts & types
│   ├── contracts/           # TypeScript interfaces
│   └── backend/             # Backend utilities
├── .ruler/                  # AI agent instructions
├── .cursor/                 # Cursor IDE config
└── process-compose.yaml     # Multi-process orchestration
```

## Development Workflow

1. **Define Contracts** - TypeScript interfaces in `shared/contracts/`
2. **CrewAI Builds Backend** - Agents generate ECS code from patterns
3. **Human Reviews** - Code review and frontend integration
4. **Iterate** - Test, refine, repeat

## Current Sprint Focus

- **ECS Component Schemas** - Biome, Combat, Movement components
- **Creature AI** - Yuka.js integration for predator/prey behaviors
- **Asset Pipeline** - Meshy API for 3D model generation
- **Game Builder Crew** - AI agents that write actual game code

## Performance Targets

| Metric | Target |
|--------|--------|
| FPS | 60 on iPhone 13 |
| Draw Calls | < 100 per frame |
| Vertices | < 500k per frame |
| Texture Memory | < 200MB |

## Key Files

- `AGENTS.md` - Root AI instructions
- `.ruler/ruler.toml` - MCP server configuration
- `python/crew_agents/README.md` - CrewAI documentation
- `client/src/ecs/ARCHITECTURE.md` - ECS architecture guide

## ConPort Usage

This project uses ConPort (Context Portal) for AI memory:

- **Product Context** - This brief and overall goals
- **Active Context** - Current sprint focus and tasks
- **Decisions** - Architectural and implementation decisions
- **Progress** - Task tracking and status
- **Custom Data** - Project glossary, patterns, specs

Initialize ConPort by running:
```bash
# Start ConPort server
uvx --from context-portal-mcp conport-mcp --mode stdio --workspace_id "$(pwd)"
```

## Team

- **Human Developer** - Frontend, integration, creative direction
- **CrewAI Agents** - Backend code generation, testing, documentation
