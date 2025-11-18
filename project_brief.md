# Rivermarsh - Project Brief

**Last Updated**: November 18, 2025  
**Status**: Active Development  
**Target Launch**: Q2 2026

## Executive Summary

Rivermarsh is a mobile-first 3D adventure/light RPG starring an otter protagonist in a vast, living marshland ecosystem. Players explore, fish, build relationships with otter factions, complete quests, and uncover secrets of the river.

**Core Feel**: Zelda: Breath of the Wild meets Stardew Valley meets Untitled Goose Game – but you're an otter, everything is wet, and the world is alive with realistic water physics and vegetation.

## Platform & Performance Targets

- **Primary**: Web (browser-playable)
- **Secondary**: iOS/Android via Capacitor
- **Target FPS**: 60 on mid-tier phones (iPhone 13+, mid-range Android)
- **Visual Quality**: Lush, painterly, stylized realism with custom shaders

## Technical Stack (FINAL - NO DEVIATIONS)

### Core Technologies
- **Frontend**: React 18 + TypeScript (strict mode)
- **3D Engine**: React Three Fiber (@react-three/fiber)
- **Helpers**: @react-three/drei (latest)
- **Physics**: @react-three/rapier OR ecctrl (ecctrl preferred)
- **State Management**: Zustand (single store pattern)
- **UI Framework**: Material UI (via @mui/mcp-server integration)
- **Styling**: Tailwind CSS + clsx
- **Build Tool**: Vite
- **Audio**: Howler.js
- **Mobile**: Capacitor

### ECS Architecture
- **Core**: Miniplex (entity-component system)
- **AI**: Yuka.js (steering behaviors, goal-driven AI)
- **World Simulation**: Custom systems (Time, Weather, Spawn, Combat)

### Development Tools
- **MCP Servers**: Material UI, Playwright, Context7, Vite-React, Context-portal
- **AI Development Crew**: Hierarchical CrewAI with 6 specialist agents
- **Asset Generation**: Meshy.ai (600+ animation library)

## Game Design Pillars

### 1. Water is the Star
- Gerstner waves + FFT (switchable)
- Caustics projector
- Depth-based color + foam
- Realistic wake trails
- Screen-space refraction/reflection

### 2. Living Ecosystem
- **Species**: 13 predators + 15 prey with full AI
- **Biomes**: Marsh, forest, river, lake (procedural + hand-authored)
- **Resources**: 9 gatherable types (cattails, berries, mushrooms, etc.)
- **Day/Night Cycle**: Affects NPC schedules and spawns
- **Weather**: Clear, rain, fog, storm (impacts gameplay)

### 3. Cozy Yet Deep
- Simple real-time combat (pausable, Zelda-style)
- Stamina-based actions (swim fast = drain stamina)
- Faction reputation system (3 otter factions)
- Crafting and fishing mechanics
- Quest system with branching choices

## World Structure

### Map Layout
- **Size**: 4 km × 4 km total
- **Chunk System**: 256 m chunks, 9 visible at once
- **Generation**: Layered simplex noise + hand-painted control map
- **Villages**: Pre-made bundles placed on valid terrain
- **Streaming**: Dynamic chunk loading for performance

### Biomes
1. **Marsh** (primary): Cattails, lily pads, shallow water
2. **Forest**: Trees, mushrooms, berry bushes
3. **River**: Fast-flowing water, fish spawns
4. **Lake**: Deep water, unique resources

## Character & Combat

### Player Character (Otter)
- **Movement**: Swim, walk, run, climb
- **Attacks**: Bite, Tail Slap, Rock Throw
- **Stats**: Health, Stamina, Faction Reputation
- **Inventory**: Items, equipment, quest items

### Combat System
- Real-time with pause
- Stamina-based attacks
- Simple enemy AI (Yuka steering behaviors)
- Weight + impact feel > complex combos

### Enemy Types
- 6 enemy types (from predator species list)
- Simple state machines (idle, patrol, chase, attack)
- Pack tactics for wolves
- Boss encounters with unique mechanics

## Quest & Progression

### Quest Types
- **Main Story**: 8 major quests uncovering marsh secrets
- **Faction Quests**: Build reputation with otter groups
- **Side Quests**: Help individual NPCs
- **Fetch/Gather**: Resource collection
- **Combat**: Defeat specific enemies

### Progression Systems
- **Skills**: Swimming, fishing, crafting, combat
- **Equipment**: Enchanted items augmenting natural abilities
- **Faction Ranks**: Unlock unique rewards per faction

## Current Development Status

### ✅ Completed
- ECS data layer (13 predators, 15 prey, 9 resources)
- Component initializers (Combat, Movement, AI, Equipment, Animation)
- Entity factories (createPredator, createPrey, createBiomeResource)
- Attack normalization helpers
- Species taxonomy with Meshy prompts
- CrewAI hierarchical setup with MCP integration
- Type safety validation (0 TypeScript errors)

### 🔧 In Progress
- YukaSyncSystem (ECS ↔ Yuka bridge)
- Core systems (Time, Weather, Spawn, Combat)
- Advanced water shader implementation

### ⏳ Next Steps
1. Complete core ECS systems
2. Implement TDD tests (combat balance, AI behavior)
3. Build Meshy pre-build script (idempotent generation)
4. Create R3F rendering components
5. Integrate full pipeline (ECS → Yuka → R3F)
6. Mobile optimization and testing

## Performance Budget

| Device | Target FPS | Max Draw Calls | Max Triangles |
|--------|-----------|----------------|---------------|
| iPhone 13 | 60 | < 150 | < 800k |
| Mid Android | 50-60 | < 200 | < 1M |
| Desktop | 120+ | < 300 | < 2M |

### Optimization Strategies
- Instancing for repeated objects (grass, lilies, fish)
- LOD system (3 levels)
- GPU culling
- Shader optimization (minimize branching)
- Chunked terrain with marching cubes
- BC7 texture compression (1K max)

## Visual Style

### Rendering Approach
- **SDF/Raymarching**: Water, mud, reed bending, fur edges
- **InstancedMesh**: Everything repeated
- **Marching Cubes**: Deformable terrain (digging, building)
- **Post-Processing**: Bloom, DoF, SSAO, god rays, color grading

### Camera System
- **Type**: Diorama view (angled down, isometric-style)
- **NOT**: First-person
- **Features**: Smooth follow, adjustable zoom/rotation
- **Controls**: Right joystick (mobile), mouse (desktop)

## Input System (Mobile First)

### Controls
- **ecctrl**: Player movement + virtual joystick (left stick)
- **nipplejs**: Right virtual joystick (look/action/swim direction)
- **Touch Menu**: Tap-and-hold (Talk/Examine/Use/Attack)
- **Desktop Fallback**: WASD + mouse look (same code path)

### Implementation
- Single `useControls()` store for rebinding
- All input normalized through one system

## Audio Design

### Music
- Ambient marsh sounds (birds, water, wind)
- Dynamic music system (changes with biome/time/combat)
- Sample audio files provided (MP3/OGG/WAV)

### Sound Effects
- Swimming splashes
- Combat impacts
- UI feedback
- Environmental ambience

## Save System

- **Storage**: Zustand persist middleware → localStorage
- **Data**: Player state, world state, quest progress
- **Frequency**: Auto-save on major events, manual save option
- **Cross-platform**: Works on web + mobile

## Development Rules (MUST FOLLOW)

1. **No new dependencies without approval** - If not in tech stack → NO
2. **Mobile first** - Test on phone before committing
3. **Shader fallbacks** - Low-end devices get simpler shaders
4. **No floating point errors in UI** - Always round numbers
5. **Save system day 1** - Persist immediately, test early
6. **No crunch** - Fixed scope, done > perfect

## Folder Structure (LAW)

```
src/
├── components/          # Pure R3F components
│   ├── player/
│   ├── terrain/
│   ├── water/
│   ├── ui/
│   └── npc/
├── systems/             # Game logic systems
│   ├── questSystem.ts
│   ├── dialogueSystem.ts
│   ├── inventorySystem.ts
│   └── combatSystem.ts
├── scenes/              # Loaded levels/areas
├── shaders/             # .glsl files
├── lib/                 # Utilities, noise, save/load
├── stores/              # Zustand stores
├── assets/              # GLB, textures, audio
└── App.tsx             # Canvas + UI overlay only
```

## AI Development Crew

### Team Structure
- **Manager**: Coordinates workflow, delegates tasks
- **ECS Architect**: Reviews architecture, validates patterns
- **Yuka AI Engineer**: Implements AI systems
- **Rendering Engineer**: R3F components, shaders, post-processing
- **Systems Engineer**: Core game systems
- **QA Tester**: Testing, validation, Playwright automation
- **Chief Architect**: Documentation, final review

### MCP Tools Available
- **Material UI**: Component generation
- **Playwright**: Browser automation, E2E tests
- **Context7**: Distributed context (Upstash)
- **Vite-React**: Dev tooling, HMR
- **Context-portal**: This project brief + collaborative docs

## User Preferences

- Speak like a normal human, not corporate
- Short sentences when possible
- No fake enthusiasm
- Working, beautiful code > "correct" architecture
- Prefer fixing over rewriting from scratch

## Success Metrics

### Technical
- 60 FPS on iPhone 13 consistently
- < 5 second load time on mid-tier phone
- 0 TypeScript errors
- < 100 draw calls per frame (mobile)

### Gameplay
- 8 hours of main story content
- 15+ hours with side quests
- Satisfying water physics (the screenshot moment)
- Smooth, responsive controls
- Engaging but not punishing combat

## Risk Mitigation

### High Risk
- **Water performance**: Mitigate with quality presets, shader LOD
- **Mobile battery drain**: Optimize render loop, reduce calculations
- **Asset size**: BC7 compression, lazy loading, chunking

### Medium Risk
- **AI complexity**: Keep steering behaviors simple, limit entities
- **Quest bugs**: TDD approach, state machine validation
- **Cross-platform input**: Test early, unified input layer

## Timeline (Tentative)

- **Week 1-2**: Core systems implementation
- **Week 3-4**: Rendering pipeline + water shader
- **Week 5-6**: AI integration + combat testing
- **Week 7-8**: Quest system + first playable area
- **Week 9-12**: Content creation (NPCs, quests, areas)
- **Week 13-16**: Polish, optimization, mobile testing
- **Week 17-20**: Beta testing, bug fixes, final touches

## Resources

- **ECS Architecture**: `client/src/ecs/ARCHITECTURE.md`
- **Species Data**: `client/src/ecs/data/predatorSpecies.ts`, `preySpecies.ts`
- **Component Initializers**: `client/src/ecs/entities/componentInitializers.ts`
- **CrewAI Setup**: `crew_config/README.md`
- **Replit Docs**: `replit.md`

---

**This document is the source of truth for all development decisions.**  
**When in doubt, refer to this brief. When brief conflicts with code, brief wins.**

*Last edited by: AI Development Crew*  
*Next review: When major architectural decisions are needed*
