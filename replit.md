
# Rivermarsh - 3D Otter Adventure Game

> **Note:** This project uses [Ruler](https://github.com/intellectronica/ruler) for distributed agent instructions. All detailed documentation is managed through `.ruler/` directories.

## Quick Reference

- **Architecture:** See [.ruler/AGENTS.md](.ruler/AGENTS.md) for cross-cutting standards
- **Frontend:** See [client/.ruler/AGENTS.md](client/.ruler/AGENTS.md) for React/R3F patterns
- **Backend:** See [python/.ruler/AGENTS.md](python/.ruler/AGENTS.md) for Python conventions
- **Documentation:** See [docs/.ruler/writing_style.md](docs/.ruler/writing_style.md) for writing standards
- **Shared Contracts:** See [shared/.ruler/AGENTS.md](shared/.ruler/AGENTS.md) for type definitions

## Running the Project

### Development Mode
```bash
npm run dev                    # Start Vite dev server only
process-compose up             # Start CrewAI background tasks
npm run dev & process-compose up  # Both (or use "dev-with-crewai" workflow)
```

### Applying Ruler Instructions
When you switch AI agents (Cursor, Claude, Cline, etc.):
```bash
ruler apply
```

This generates agent-specific instruction files from all `.ruler/` directories.

## Project Overview

Rivermarsh is a cozy 3D adventure/RPG where you play as an otter in a marshland ecosystem. Built with React Three Fiber, TypeScript, and an Entity-Component-System architecture.

**Core Technologies:**
- React 18 + TypeScript
- React Three Fiber (@react-three/drei)
- Miniplex ECS
- Zustand (state management)
- Material UI (interface)
- CrewAI (autonomous development)
- Meshy API (3D asset generation)

**Deployment:** Replit Deployments (not transitioning off Replit)

## Architecture Highlights

### ECS + Rendering
- Hybrid architecture: ECS for game logic, R3F for rendering
- Mandatory system execution order (see [.ruler/ecs_patterns.md](.ruler/ecs_patterns.md))
- SDF raymarching for water/fog/fur
- Instanced meshes for grass/reeds

### Material UI Integration
- Throttled `useUIState` store bridges ECS → React
- HUD components receive snapshots, not direct ECS access
- See [client/.ruler/AGENTS.md](client/.ruler/AGENTS.md)

### CrewAI Agents
- 8 specialist agents orchestrated by Technical Director
- Background tasks via `process-compose`
- Deliverables in `shared/backend/`
- See [docs/architecture/crewai_usage.md](docs/architecture/crewai_usage.md)

## User Preferences

- Speak like a normal human, not a corporate robot
- Short sentences when possible
- No fake enthusiasm
- Call things what they are
- Prefer working, beautiful code over "correct" architecture

## File Structure

```
.ruler/                    # Root-level cross-cutting standards
client/.ruler/             # Frontend-specific patterns
python/.ruler/             # Backend conventions
python/crew_agents/.ruler/ # CrewAI workflow configuration
docs/.ruler/               # Documentation style guide
shared/.ruler/             # Contract patterns

docs/                      # Detailed documentation
  architecture/            # System design docs
  asset_generation/        # Meshy pipeline guides
  troubleshooting/         # Runbooks

shared/
  contracts/               # TypeScript type definitions
  backend/                 # CrewAI deliverables
    ecs_world/
    dfu_analysis/
    yuka_ai/
    rendering_pipeline/
    rpg_systems/

crew_config/               # CrewAI agent/task definitions
```

## Key Constraints

1. **ZERO asset generation** until core systems complete (exception: ONE otter PoC)
2. **Mobile-first development** (60 FPS on iPhone 13)
3. **No new dependencies** without approval
4. **Mandatory post-processing stack** (see [client/.ruler/rendering_pipeline.md](client/.ruler/rendering_pipeline.md))
5. **Strict performance budgets** (see [.ruler/AGENTS.md](.ruler/AGENTS.md))

## External Dependencies

**Required APIs:**
- OpenRouter (CrewAI model routing)
- Meshy (3D asset generation)

**Database:**
- File-based persistence (TaskRepository in Python)

**Asset Sources:**
- Daggerfall Unity data files (creature stats, terrain algorithms)

## Getting Help

- **CrewAI Issues:** See [docs/troubleshooting/CREWAI_RUNBOOK.md](docs/troubleshooting/CREWAI_RUNBOOK.md)
- **Integration Questions:** See [docs/architecture/INTEGRATION_GUIDE.md](docs/architecture/INTEGRATION_GUIDE.md)
- **Parallel Development:** See [docs/PARALLEL_DEVELOPMENT.md](docs/PARALLEL_DEVELOPMENT.md)

## Session State

Active decisions and current status tracked in:
- [docs/SESSION_STATE.md](docs/SESSION_STATE.md)
- [docs/DECISION_LOG.md](docs/DECISION_LOG.md)

---

**For complete technical specifications, run `ruler apply` and consult the generated agent-specific files.**
