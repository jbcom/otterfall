# Rivermarsh - 3D Otter Adventure Game

## Overview
Rivermarsh is a cozy 3D adventure/RPG game where players control an otter in a marshland. The game blends exploration, fishing, questing, and relationship building, aiming for a "Zelda: Breath of the Wild meets Stardew Valley" feel. It emphasizes realistic water physics, environmental interaction, and a dynamic world. The game targets web and mobile (iOS/Android), featuring a painterly visual style and aiming for 60 FPS on mid-tier phones.

## User Preferences
- Speak like a normal human, not a corporate robot
- Short sentences when possible
- No fake enthusiasm
- Call things what they are
- Prefer working, beautiful code over "correct" architecture

## System Architecture
Rivermarsh is built with React 18, TypeScript, React Three Fiber, and @react-three/drei for rendering, using ecctrl for physics and Zustand for global state management. Styling uses Vite with vanilla-extract or Tailwind + clsx. Capacitor enables mobile builds, and Howler.js handles audio. The project avoids heavy frameworks like Redux or Unity.

The project structure is strictly organized into `src/components`, `src/systems`, `src/scenes`, `src/shaders`, `src/lib`, `src/stores`, `src/assets`, and `App.tsx`.

Rendering utilizes SDF/raymarched details for water and fur, InstancedMesh for repeated elements, and marching cubes for dynamic terrain. A mandatory post-processing stack includes Bloom, Depth of Field, SSAO/SSDO, God rays, and color grading. Mobile optimization includes LODs, 1K max textures, BC7 compression, and GPU-driven rendering.

A single Zustand store (`useGameStore.ts`) manages game state. Input is mobile-first, using ecctrl for movement and nipplejs for camera/action, managed by a `useControls()` store. The camera uses a smooth-following, angled-down diorama view.

The world is a 4km × 4km procedurally generated environment, streamed in 256m chunks using layered simplex noise. Biomes are environment-driven, with pre-made structures. The water system features Gerstner waves, caustics, depth-based coloring, refraction, reflection, and otter wake trails. Combat is real-time, pausable, stamina-based with three attack types. Enemy AI uses simple steering behaviors. JSON-based quest and dialogue systems use Zustand for flags, and NPCs follow schedules.

Performance targets are strict: iPhone 13 (60 FPS, <150 Draw Calls, <800k Triangles), Mid Android (50-60 FPS, <200 Draw Calls, <1M Triangles), and Desktop (120+ FPS, <300 Draw Calls, <2M Triangles), achieved through instancing, chunking, LOD, GPU culling, and shader optimization. Development mandates no new dependencies without approval, mobile-first feature development, shader fallbacks, accurate UI numbers, a day-one save system, and strict scope.

Key architectural standards include an ECS + Rendering system with mandatory execution order, hybrid rendering (JSX for static, InstancedMesh for dense populations), a 3x3 active chunk window, and a specific post-processing stack order. Material UI components receive throttled UI snapshots from a `useUIState` Zustand store, with mandatory responsive design. Yuka AI integration involves prewarmed Vehicle/StateMachine pools, specific state machine definitions, and steering behavior weights for different animal types, with performance optimization including tiered update frequencies and spatial indexing.

## External Dependencies
**Database & Backend:**
- Drizzle ORM with PostgreSQL
- Express server with Vite middleware

**Asset Management:**
- Textures
- Audio files (MP3/OGG/WAV)
- 3D models (GLTF/GLB)
- Font: Inter via @fontsource

**UI Libraries:**
- Radix UI for accessible primitives
- Lucide React for icons
- Tailwind CSS + clsx

**3D Graphics:**
- @react-three/drei
- @react-three/postprocessing
- vite-plugin-glsl

**Python Tooling (Build-time only):**
- Meshy SDK: for 3D model, texture, and animation generation (Webhook-only architecture)
- CrewAI agents: for autonomous game system building (see [docs/architecture/crewai_usage.md](docs/architecture/crewai_usage.md))
- `uv` for package management
- `httpx`, `tenacity`, `rich`, `playwright` (Meshy SDK dependencies)
- `crewai[anthropic]`, `litellm` (CrewAI dependencies)
- `pytest` for testing