# Rivermarsh - 3D Otter Adventure Game

## Overview

Rivermarsh is a 3D adventure game built with React Three Fiber, featuring an otter protagonist navigating a marshland environment. Players explore a procedurally-generated terrain, interact with NPC otters from different factions, complete quests, and engage in combat. The game combines exploration, RPG mechanics (health, stamina, inventory, quests), and real-time 3D graphics with shader-based effects.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- **React 18** with TypeScript for UI components and game logic
- **React Three Fiber (R3F)** with drei utilities for 3D rendering and scene management
- **Three.js** as the underlying WebGL library
- **Vite** for development and production builds with hot module replacement
- **TailwindCSS** with custom theming for UI overlays and menus

**Key Design Decisions:**
- **Component-based 3D architecture**: Each game element (player, terrain, NPCs) is a React component that manages its own state and rendering logic
- **Hook-based state management**: Zustand stores with selectors provide global state for game mechanics, audio, and player data
- **Shader-based rendering**: Custom GLSL shaders for water effects and terrain, with support for advanced visual effects via postprocessing (Bloom, Depth of Field)
- **Mobile-first input handling**: Dual control system supporting both keyboard/mouse and virtual joysticks for touch devices

**3D Rendering Approach:**
- Procedural terrain generation using plane geometries with vertex manipulation
- Instanced rendering for grass and reeds to optimize performance with many repeated objects
- Billboard text rendering for NPC labels and UI elements in 3D space
- **Advanced water shaders** with caustics, Perlin noise-based waves, Fresnel effects, and depth-based coloring (`client/src/components/AdvancedWater.tsx`)
- **Procedural dungeon generation** inspired by Daggerfall Unity architecture patterns with room-based layouts, water effects, and themed environments (`client/src/components/ProceduralDungeon.tsx`, `client/src/data/daggerfallDungeonReference.ts`)

**Rationale**: R3F was chosen over vanilla Three.js to leverage React's component model and hooks, making complex 3D scenes more maintainable. The shader-based approach enables smooth, organic visuals (referenced in attached_assets discussing raymarched SDFs) while maintaining good performance.

### State Management

**Zustand Stores:**
1. **useRivermarsh**: Core game state including player stats, inventory, quests, NPCs, and dialogue system
2. **useGame**: Game phase management (ready/playing/ended)
3. **useAudio**: Sound effects and background music with mute controls

**Store Design Pattern:**
- Subscriptions with selectors for fine-grained reactivity
- Action methods co-located with state for clear data flow
- In-memory only (no persistence) - game state resets on reload

**Alternatives Considered**: Redux was avoided due to boilerplate overhead; Context API was insufficient for the performance requirements of frame-by-frame updates.

### Input Systems

**Dual Control Schema:**
- **Desktop**: Keyboard controls (WASD/Arrows for movement, E for interact, F for attack, I/Q for menus) with mouse look
- **Mobile**: Virtual joysticks via nipplejs library - left stick for movement, right stick for camera control

**Implementation**: A unified `mobileInput` state object bridges both control schemes, allowing the Player component to handle input agnostically.

**Pros**: Accessibility across devices without separate codebases
**Cons**: Additional complexity in touch event handling and state synchronization

### Game Mechanics Architecture

**RPG Systems (Enhanced November 2025):**
- **Player progression**: Experience-based leveling with health/stamina resource management
- **Skill system**: 8 Daggerfall-inspired skills (Swimming, Diving, Fishing, Combat, Sneaking, Climbing, Foraging, Crafting) with independent experience tracking and multi-level progression support
- **Equipment system**: 5 equipment slots (weapon, shell_armor, diving_gear, fishing_rod, accessory) with item stats (attack, defense, swimSpeed, diveDepth, fishingBonus)
- **Inventory system**: Item-based with categorization (weapon, armor, tool, consumable, quest_item, treasure) and equipment management
- **Quest framework**: Multi-objective quests with status tracking (available/active/completed/failed)
  - Quest generation system with authored templates and procedural objectives
  - Faction-specific quest chains (River Clan, Marsh Raiders, Elder Council, Lone Wanderers)
  - Branching storylines with dynamic rewards based on player level
- **Faction reputation system**: Numerical reputation (0-100) for 5 factions with dynamic relationship tracking

**NPC Behavior:**
- State machine for NPC types (friendly/hostile/neutral/merchant/quest_giver)
- AI wandering using timer-based random target positions
- Proximity-based aggression for hostile NPCs
- Dialogue trees stored as string arrays per NPC

**Combat**: Simple collision-based damage system with health pools and player stamina costs for attacks.

### UI Layer

**Overlay Components:**
- Fixed-position HUD displaying player stats (health, stamina, level, experience)
- Modal panels for inventory and quest log
- Dialogue boxes for NPC conversations
- Help text for controls

**Styling Approach**: Radix UI primitives with Tailwind for consistent, accessible components. UI elements use `pointer-events: none` on containers with selective enabling on interactive elements to avoid blocking 3D scene interactions.

## External Dependencies

### Database & Backend

**Drizzle ORM Configuration:**
- Schema definition in `shared/schema.ts` with PostgreSQL dialect
- User table structure with username/password fields
- Migration output to `./migrations` directory
- Database connection via `DATABASE_URL` environment variable with Neon serverless driver

**Current State**: Backend routes (`server/routes.ts`) and storage layer (`server/storage.ts`) are scaffolded but not actively used by the game. In-memory storage class exists as an abstraction layer.

**Note**: The application uses Drizzle with PostgreSQL but game state is currently client-side only. Database integration is prepared for future multiplayer or persistence features.

### Asset Management

**Static Assets:**
- Textures loaded via Three.js TextureLoader (e.g., `/textures/grass.png`)
- Audio files (MP3/OGG/WAV) for background music and sound effects
- 3D models support (GLTF/GLB) configured in Vite
- Font: Inter via @fontsource package

**Asset Loading Strategy**: Lazy loading of textures and audio in component mount effects. No loading screens implemented - assets load asynchronously as components render.

### Third-Party Services

**UI Component Libraries:**
- **Radix UI**: Accessible primitive components (Dialog, Dropdown, Accordion, etc.) providing keyboard navigation and ARIA attributes
- **Lucide React**: Icon library for UI elements

**3D Graphics:**
- **@react-three/drei**: Helper components (Sky, Billboard, Text, OrbitControls, KeyboardControls)
- **@react-three/postprocessing**: Screen-space effects (EffectComposer, Bloom, DepthOfField)
- **vite-plugin-glsl**: GLSL shader imports for custom materials

**Input Handling:**
- **nipplejs**: Virtual joystick library for mobile touch controls

**Utilities:**
- **class-variance-authority**: Type-safe variant styling for component libraries
- **date-fns**: Date formatting (installed but not actively used in current game code)
- **nanoid**: Unique ID generation for server-side utilities

**Development Tools:**
- **@replit/vite-plugin-runtime-error-modal**: Enhanced error overlays during development
- **tsx**: TypeScript execution for server without compilation step

### Express Server

**Server Configuration:**
- Express with JSON/URL-encoded body parsing
- Request logging middleware capturing method, path, status, duration, and JSON responses
- Vite middleware integration in development mode with HMR over HTTP server
- Static file serving for production builds
- Error handling middleware with status code detection

**Production Build**: Client builds to `dist/public`, server bundles with esbuild to `dist/index.js` in ESM format with external packages.