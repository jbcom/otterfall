
# Rivermarsh - 3D Otter Adventure Game

## Project Identity

Rivermarsh is a cozy 3D adventure/RPG game where players control an otter in a marshland environment. The game combines exploration, fishing, questing, and relationship building, targeting **"Zelda: Breath of the Wild meets Stardew Valley"** vibes with realistic water physics and environmental interaction.

**Platforms:** Web + Mobile (iOS/Android)  
**Visual Style:** Painterly, cozy aesthetic  
**Performance Target:** 60 FPS on mid-tier phones

---

## Communication Style Preferences

- Speak like a normal human, not a corporate robot
- Use short sentences when possible
- No fake enthusiasm
- Call things what they are
- Prefer working, beautiful code over "correct" architecture

---

## Core Technology Stack

### Frontend
- **React 18** with **TypeScript**
- **React Three Fiber** (@react-three/fiber) + **@react-three/drei** for 3D rendering
- **ecctrl** for physics-based character controller
- **Zustand** for global state management
- **Miniplex** for ECS (Entity Component System)
- **Yuka.js** for AI steering behaviors and state machines

### Styling
- **Vite** build tool
- **Tailwind CSS** + **clsx** for utility-first styling
- **Radix UI** for accessible primitives
- **Lucide React** for icons

### Mobile
- **Capacitor** for native iOS/Android builds
- **nipplejs** for virtual joystick controls
- **Howler.js** for audio management

### Backend
- **Express** server with Vite middleware
- **Drizzle ORM** with **PostgreSQL**
- **Express Session** with memory store

### Asset Generation (Build-time)
- **Meshy SDK** for 3D model/texture/animation generation (webhook-only)
- **CrewAI agents** for autonomous game system building
- **Python tooling** (`uv`, `httpx`, `playwright`, `pytest`)

---

## Mandatory Architecture Rules

### 1. Folder Structure (STRICTLY ENFORCED)

```
src/
├── components/     # R3F components ONLY (3D scene elements)
├── systems/        # Game logic (Zustand + Miniplex systems)
├── scenes/         # Level/area definitions
├── shaders/        # GLSL shader files
├── lib/
│   └── stores/     # Zustand stores
├── stores/         # Additional state management
└── assets/         # Static assets (textures, models, audio)
```

**Rules:**
- Components = Visual/3D elements only
- Systems = Pure logic (no JSX)
- ONE Zustand store for game state (`useGameStore`)
- NO Redux, Recoil, MobX, or Jotai

### 2. Performance Targets (NON-NEGOTIABLE)

| Device | FPS | Draw Calls | Triangles |
|--------|-----|------------|-----------|
| iPhone 13 | 60 | <150 | <800k |
| Mid Android | 50-60 | <200 | <1M |
| Desktop | 120+ | <300 | <2M |

**Optimization Techniques:**
- **InstancedMesh** for repeated objects (trees, rocks, grass)
- **LOD system** (3 levels minimum)
- GPU culling for off-screen objects
- Texture compression (BC7, 1K max on mobile)
- Shader optimization (avoid branching)

### 3. Rendering Architecture

**Mandatory Post-Processing Stack (in order):**
1. Bloom (subtle glow)
2. Depth of Field (diorama effect)
3. SSAO/SSDO (ambient occlusion)
4. God rays (directional light shafts)
5. Color grading (painterly look)

**Rendering Techniques:**
- SDF/raymarched effects for water and fur details
- Gerstner waves for realistic water motion
- Marching cubes for dynamic terrain deformation
- Caustics shader for underwater light patterns

### 4. Camera System

**Diorama Camera (NOT first-person):**
- Smooth-following, angled-down perspective
- Target: Otter character center-mass
- Offset: ~8 units back, ~5 units up
- Mobile: Gyroscope tilt support (optional)

### 5. Input System

**Mobile-First Design:**
- **ecctrl** for movement physics
- **nipplejs** for virtual joystick (camera + actions)
- Managed by `useControlsStore` (Zustand)
- Desktop: Keyboard/mouse fallback

### 6. World Generation

**Procedural 4km × 4km Environment:**
- Streaming in 256m chunks (3×3 active window)
- Layered simplex noise for terrain
- Environment-driven biomes (marsh, forest, river, ruins)
- Pre-made structures (villages, dungeons)

### 7. Combat System

- Real-time, pausable combat
- Stamina-based (3 attack types: light, heavy, special)
- Enemy AI: Simple steering behaviors (Yuka.js)

### 8. Quest & Dialogue

- JSON-based definitions
- Zustand flags for progress tracking
- NPC schedules (time-of-day behavior)

---

## Development Workflow

### CrewAI Background Tasks

The project uses **CrewAI agents** running via `process-compose` for autonomous development:

```bash
# Start all agents
process-compose up

# Individual tasks
process-compose up ecs_component_schemas
process-compose up yuka_ai_integration
process-compose up terrain_water_rendering
```

**Agent Roles:**
- **Technical Director** (Manager): Coordinates all agents
- **ECS Architect**: Type-safe Miniplex systems
- **Yuka AI Engineer**: Creature AI behaviors
- **Rendering Engineer**: R3F + custom shaders
- **Systems Engineer**: Quests, inventory, combat
- **DFU Analyst**: Parse Daggerfall Unity data
- **QA Tester**: Performance validation

**Logs:** `logs/crewai/*.log`

### Asset Generation Pipeline

**Meshy SDK** (webhook-only architecture):
1. Text → 3D model generation
2. Rigging (skeleton/joints)
3. Animation (attack, idle, walk, etc.)
4. Retexturing (seasonal variants)

**Workflow:**
```bash
# Generate otter model
uv run python python/scripts/generate_assets.py

# Monitor webhook server
uv run python python/scripts/run_webhook_server.py
```

---

## Code Quality Standards

### TypeScript
- Strict mode enabled
- Explicit types for all function signatures
- No `any` types (use `unknown` if necessary)
- Prefer `interface` over `type` for objects

### React/R3F
- Functional components only
- Hooks for state management
- Memoization for expensive computations (`useMemo`, `React.memo`)
- Proper cleanup in `useEffect` (return cleanup functions)

### Shaders (GLSL)
- Prefix all uniforms with `u_`
- Prefix all attributes with `a_`
- Prefix all varyings with `v_`
- Comments for complex math operations
- Fallbacks for mobile (avoid high-precision floats)

### Performance
- Profile before optimizing
- Measure draw calls with R3F DevTools
- Use `<Perf>` component from `@react-three/drei`
- Batch state updates in Zustand

---

## Deployment

**Production Build:**
```bash
npm run build
npm run preview  # Test production build locally
```

**Replit Deployment:**
- Deployment target: `autoscale`
- Build command: `npm run build`
- Run command: `npm run preview`
- Port 5000 → External 80/443

---

## Scope Discipline

### ✅ In Scope
- Otter player character + 5 NPC species
- 4 biomes (marsh, forest, river, ruins)
- 10 quest archetypes (fetch, escort, combat, puzzle)
- Basic fishing mechanic
- Inventory system (20 slots)
- Day/night cycle (12-minute loop)

### ❌ Out of Scope (DO NOT IMPLEMENT)
- Multiplayer/networking
- Procedural dungeons (pre-made only)
- Crafting system (future)
- Player housing (future)
- Mounts/vehicles (future)

---

## Critical Reminders

1. **Mobile-first development** - Test on iPhone 13 equivalent
2. **No new dependencies without approval** - Justify with performance data
3. **Shader fallbacks mandatory** - Progressive enhancement for low-end devices
4. **Day-one save system** - LocalStorage + optional cloud sync
5. **Accurate UI numbers** - No "fake" progress bars or misleading stats

---

## Getting Help

- **Architecture questions:** Review `/docs/architecture/`
- **ECS patterns:** See `/client/src/ecs/ARCHITECTURE.md`
- **CrewAI usage:** See `/docs/architecture/crewai_usage.md`
- **Asset generation:** See `/docs/asset_generation/otter_pipeline_poc.md`
