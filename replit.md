# Rivermarsh - 3D Otter Adventure Game

## Overview
Rivermarsh is a cozy yet deep 3D adventure / light RPG starring an otter protagonist in a vast, living marshland. The player explores, fishes, builds relationships with otter factions, completes quests, fights (or talks) their way out of trouble, and uncovers the secrets of the river.

**Core feel**: Zelda: Breath of the Wild meets Stardew Valley meets Untitled Goose Game – but you're an otter, everything is wet, and the world is alive with water physics, reeds that sway realistically, and otters that actually swim properly.

**Target platforms**: Web first (playable in browser), 60 fps on mid-tier phones, native iOS/Android via Capacitor.

**Visual style**: Lush, painterly, slightly stylised realism. Heavy use of custom shaders, SDF/raymarched details, instanced foliage, and post-processing (bloom, god rays, depth-based fog) to make it look expensive while staying performant.

**Current date**: November 18, 2025 – we are building for 2026 phones, not 2020 ones.

## User Preferences (LAW)
- Speak like a normal human, not a corporate robot
- Short sentences when possible
- No fake enthusiasm
- Call things what they are
- Prefer working, beautiful code over "correct" architecture

## System Architecture (FINAL – NO DEVIATIONS)

### Technology Stack (Locked)
- React 18 + TypeScript (strict mode on)
- React Three Fiber (@react-three/fiber)
- @react-three/drei (latest)
- **@react-three/rapier or ecctrl for physics** (ecctrl preferred – it just works)
- Zustand for global state (no context hell)
- Vite + vanilla-extract or Tailwind + clsx for styling
- GLSL shaders only (no three-meshui, no react-spring for 3D)
- Capacitor for mobile builds
- Howler.js for audio
- **NO Redux, NO Recoil, NO MobX, NO Jotai, NO Signals, NO Unity, NO Godot**

### Folder Structure (THIS IS LAW)
```
src/
├── components/          # Pure R3F components
│   ├── player/
│   ├── terrain/
│   ├── water/
│   ├── ui/
│   └── npc/
├── systems/             # Game logic systems (Zustand + Miniplex if needed)
│   ├── questSystem.ts
│   ├── dialogueSystem.ts
│   ├── inventorySystem.ts
│   └── combatSystem.ts
├── scenes/              # Loaded levels / areas (procedural + hand-tweaked)
├── shaders/             # .glsl files
├── lib/                 # Utilities, noise, save/load, etc.
├── stores/              # Zustand stores
├── assets/              # GLB, textures, audio
└── App.tsx             # Only the Canvas + UI overlay
```

### Rendering Philosophy (NON-NEGOTIABLE)
- **Everything that can be SDF/raymarched = do it**
  - Water, mud, reeds bending, otter fur edges, magical effects, UI health bars (as SDF capsules)
- **InstancedMesh for everything repeated** – grass, lilies, fish schools, bubbles
- **Marching cubes** only for dynamic deformable terrain (otter digs holes, beavers build dams → regenerate chunks)
- **Post-processing stack (mandatory)**:
  - Bloom (for fireflies, magic)
  - Depth of Field (cinematic focus on NPCs)
  - SSAO or SSDO
  - God rays (volumetric light through mist)
  - Color grading LUT (warm golden hour default)
- **Mobile = 60 fps target**
  - LOD system mandatory (three levels)
  - 1K textures max, BC7 compression
  - No 4K anything
  - Instancing + GPU-driven rendering where possible

### State Management (Zustand Only)
```typescript
// stores/useGameStore.ts
interface GameStore {
  player: {
    health: number
    stamina: number
    position: [number, number, number]
    inventory: Item[]
    quests: Quest[]
    factionRep: Record<string, number>
  }
  world: {
    timeOfDay: number // 0-1
    weather: 'clear' | 'rain' | 'fog' | 'storm'
  }
  ui: {
    activeDialogue: DialogueNode | null
    showInventory: boolean
  }
}
```
**One store. No splitting unless it becomes unmanageable (it won't).**

### Input System (Mobile First)
- **ecctrl** for player movement + built-in virtual joystick (left stick)
- **nipplejs** for right virtual joystick (look / action / swim direction)
- Touch action menu on tap-and-hold (Talk / Examine / Use / Attack)
- Desktop fallback: WASD + mouse look, same code path
- All input goes through a single `useControls()` store so you can rebind instantly

### Camera System
- **Diorama view** (angled down, isometric-style)
- NOT first-person
- Smooth follow camera tracking the player otter
- Adjustable zoom and rotation via right joystick

### Procedural World Generation (Rules – NOT chaos)
The world is procedurally generated but hand-authored in feel.
- **Heightmap** = layered simplex noise + hand-painted control map (you paint rivers, lakes, villages in Photoshop → import as texture)
- **Biomes** driven by height + moisture + temperature noise
- **Villages / dungeons** = pre-made "Daggerfall-style bundles" placed only on valid terrain (slope < 20°, near water, etc.)
- **No infinite world** – 4 km × 4 km total, streamed in 256 m chunks (9 chunks visible)
  - This gives the illusion of infinite while keeping it sane

### Water System (The Star of the Show)
Use AdvancedWater.tsx with:
- Gerstner waves + FFT (switchable)
- Caustics projector
- Depth-based color + foam at shoreline
- Refraction + reflection (screen-space or cubemap)
- Otters leave wake trails (particle or SDF)
- **This is the thing people screenshot. Make it perfect.**

### Combat System (Simple & Juicy)
- Real-time but pausable (like Zelda)
- Stamina-based attacks (swim fast = drain stamina)
- Three attack types: Bite, Tail Slap, Rock Throw
- Enemy AI via simple steering behaviors (Yuka is fine)
- No complex combos – weight + impact feel matters more than depth

### Quest & Dialogue System
- JSON-based dialogue trees (Yarn Spinner style or simple custom)
- Flags stored in Zustand
- Quests are objects with `stages[]` and `flagsRequired`
- NPCs have schedules (sleep, fish, gossip) using simple state machine

## Performance Targets (Non-Negotiable)

| Device | Target FPS | Max Draw Calls | Max Triangles (visible) |
|--------|-----------|----------------|------------------------|
| iPhone 13 | 60 | < 150 | < 800k |
| Mid Android | 50–60 | < 200 | < 1M |
| Desktop | 120+ | < 300 | < 2M |

Achieved via:
- Instancing
- Chunked terrain
- LOD (three levels)
- GPU culling
- Shader optimisation (no branching where possible)

## Development Rules (Print This)
1. **No new dependencies without approval**
   - If it's not in the stack list above → no.
2. **Every new feature must work on mobile first**
   - Test on phone before committing.
3. **All shaders must have fallback for low-end**
   - Mobile = simpler wave calculation, no caustics if performance < 50 fps.
4. **No floating point errors in UI**
   - Round numbers. Always.
5. **Save system day 1**
   - Zustand persist middleware → localStorage. Works everywhere.
6. **No crunch**
   - Scope is fixed: one beautiful marsh, 8 quests, 3 factions, 6 enemy types. Done is better than perfect.

## Immediate Next Steps (Next 14 Days)
1. Get ecctrl + nipplejs working with otter model (swimming + land movement)
2. Implement chunked terrain with proper water intersection
3. Build one complete otter village (5 houses, 8 NPCs, shop, quest giver)
4. Implement dialogue system with one full quest ("Find the lost pup")
5. Add save/load
6. Polish water until it looks like a $60 game
7. Mobile build + test on actual phone

## Current Implementation Status (Nov 18, 2025)

### ✅ ECS Data Layer COMPLETE (Type-Safe)
- **Species Data**: 13 predators + 15 prey with full stats (health, attacks, movement, AI personalities)
- **Component Initializers**: Centralized defaults for Combat, Movement, AI, Equipment, Animation
- **Attack Normalization**: Helper functions add missing attack properties (type, knockback, stun, animation)
- **Entity Factories**: createPredator(), createPrey(), createBiomeResource() using component initializers
- **Biome Resources**: 9 gatherable types (cattails, berries, mushrooms, etc.) with spawn rules
- **Yuka AI Setup**: Type declarations, manager class, and bridge pattern ready for integration

### 🔧 What Needs to Change
- **Camera**: Currently first-person, needs to be diorama/angled-down view
- **Input**: Currently keyboard-focused with custom KeyboardInputBridge, needs ecctrl + nipplejs mobile-first
- **State**: Currently split across multiple stores, needs consolidation into single useGameStore
- **Folder structure**: Doesn't match mandated structure (src/components, src/systems, src/scenes)
- **Terrain/Water**: Single meshes, needs chunking and advanced shader-based water
- **ECS Systems**: Need to implement YukaSyncSystem, TimeSystem, WeatherSystem, SpawnSystem, CombatSystem

### 💾 Salvageable Elements
- NPC data structures and dialogue system scaffolding
- Quest framework and faction reputation logic
- Skill/equipment/inventory data models
- Audio assets and sound management
- UI component library (Radix + Tailwind)
- Complete species taxonomy with Meshy prompts

### External Dependencies

**Database & Backend**:
- Drizzle ORM with PostgreSQL (scaffolded but not actively used)
- Express server with Vite middleware in development

**Asset Management**:
- Textures in `/textures` folder
- Audio files (MP3/OGG/WAV) for background music and sound effects
- 3D models support (GLTF/GLB)
- Font: Inter via @fontsource

**UI Libraries**:
- Radix UI for accessible primitives
- Lucide React for icons
- Tailwind + clsx for styling

**3D Graphics**:
- @react-three/drei for helper components
- @react-three/postprocessing for effects
- vite-plugin-glsl for shader imports
