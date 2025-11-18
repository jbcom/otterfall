# Rivermarsh - Game Development Project Brief

## Current Sprint: AI Development Automation

**Goal**: Build an autonomous AI development crew using CrewAI to accelerate Rivermarsh game development.

**Approach**: 6 specialist AI agents with 10 MCP servers for tool access, using OpenRouter's `auto` model routing for optimal performance per task.

## Project Status

### Completed
- ✅ ECS data layer (0 TypeScript errors)
- ✅ Species taxonomy (13 predators, 15 prey)
- ✅ Component initializers and entity factories
- ✅ Basic 3D scene with diorama camera
- ✅ Node 24 + Python 3.13 environment

### In Progress
- 🔄 CrewAI autonomous development system
- 🔄 Yuka AI integration
- 🔄 Chunked terrain + advanced water
- 🔄 Quest/dialogue systems

### Next Priorities
1. Get CrewAI running with openrouter/auto
2. Implement YukaSyncSystem for creature AI
3. Build procedural marshland terrain
4. Quest system with first complete quest

## Technical Stack (LOCKED)

- **Frontend**: React 18 + TypeScript (strict)
- **3D**: React Three Fiber + @react-three/drei
- **Physics/Controls**: ecctrl (NOT Rapier - ecctrl preferred)
- **AI**: Yuka.js for creature behaviors
- **State**: Zustand (single store pattern)
- **ECS**: Miniplex for world simulation
- **Mobile**: nipplejs for virtual joysticks
- **Build**: Vite 7 + pnpm
- **Deployment**: Capacitor for native mobile

## Architecture Rules

1. **Folder structure** (mandated):
   - `src/components/` - R3F components only
   - `src/systems/` - Game logic (Zustand + Miniplex)
   - `src/scenes/` - Level/area definitions
   - `src/shaders/` - GLSL files
   - `src/stores/` - Zustand stores

2. **Performance targets**:
   - 60fps on iPhone 13 / mid-tier Android
   - <150 draw calls
   - <800k triangles visible
   - LOD system (3 levels)

3. **State management**:
   - ONE Zustand store (useGameStore)
   - No Redux, Recoil, MobX, Jotai
   - ECS for world state (Miniplex)

4. **Rendering**:
   - SDF/raymarched effects where possible
   - InstancedMesh for repeated objects
   - Post-processing: bloom, DOF, god rays
   - Diorama camera (NOT first-person)

## MCP Servers (10 Total)

1. **Material UI** - Component library access
2. **Playwright** - Browser testing automation
3. **Context7** - Up-to-date library docs (React, Three.js, etc.)
4. **Vite-React** - Dev tooling
5. **ConPort** - Project memory (this file)
6. **Git** - Version control
7. **GitHub** - PR/issue automation
8. **Postgres** - Database operations
9. **Memory** - Knowledge graph
10. **Filesystem** - File operations

## AI Agent Roles

1. **ECS Architect** - Data structures, Miniplex systems
2. **Yuka Engineer** - Creature AI, steering behaviors
3. **Rendering Engineer** - R3F, shaders, performance
4. **Systems Engineer** - Quests, dialogue, inventory
5. **QA Tester** - Testing, performance validation
6. **Chief Architect** - Code review, documentation, alignment

## Current Session Context

Working on: Recreating CrewAI setup after it was lost (not committed)
Blockers: None - all secrets configured, build fixed
Next action: Run game_dev_crew_advanced.py with openrouter/auto
