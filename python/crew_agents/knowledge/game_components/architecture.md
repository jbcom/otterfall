# Rivermarsh Game Architecture

## Overview

Rivermarsh is a mobile-first 3D game where the player controls an otter navigating diverse biomes.
Built with React Three Fiber + Miniplex ECS + Yuka AI.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  React Three Fiber Components (R3F)                         │
│  - Read ECS state via Miniplex React hooks                  │
│  - Render GLB models from Meshy                             │
│  - Apply shaders for water/nature effects                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                     SIMULATION LAYER                         │
│  Yuka AI EntityManager                                       │
│  - Vehicle steering behaviors (flee, seek, wander)           │
│  - State machines (idle → hunt → attack → eat)              │
│  - Goal-driven AI                                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                            │
│  Miniplex ECS World                                          │
│  - Components: Species, Combat, Movement, AI, Animation      │
│  - Systems: SpawnSystem, CombatSystem, TimeSystem           │
│  - Entities: Predators, Prey, BiomeResources, World         │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Input → ECS (PlayerController) → Yuka (Vehicle movement)
                                    → Miniplex React Hook
                                    → R3F (Render mesh at position)

AI Tick    → Yuka (State machine executes)
           → ECS Component updated
           → AnimationComponent updated
           → R3F (Play animation on GLB model)

Combat     → ECS CombatSystem (damage calculation)
           → Update health
           → Trigger flee state if health low
           → R3F (Play hit animation)
```

## Folder Structure

```
client/src/
├── ecs/
│   ├── components/           # Pure data interfaces
│   │   ├── BiomeComponent.ts
│   │   ├── WeatherComponent.ts
│   │   ├── CombatComponent.ts
│   │   └── ...
│   ├── entities/             # Entity factories
│   │   ├── createPredator.ts
│   │   ├── createPrey.ts
│   │   └── createBiomeResource.ts
│   └── world.ts              # Miniplex ECS world
├── ai/
│   └── yukaManager.ts        # Yuka EntityManager wrapper
├── components/               # R3F rendering components
│   ├── Player.tsx
│   ├── MarshlandTerrain.tsx
│   └── ...
└── lib/stores/               # Zustand state management
    ├── useGame.tsx
    └── useRivermarsh.tsx
```

## System Execution Order

Every Frame (60 FPS):
1. TimeSystem.update()        → Advance time
2. WeatherSystem.update()     → Transition weather
3. YukaEntityManager.update() → Run AI behaviors
4. CombatSystem.update()      → Process attacks
5. SpawnSystem.update()       → Spawn new entities
6. AnimationSystem.update()   → Select animations
7. R3F.render()               → Render frame

## Biomes

7 distinct biomes:
- **Marsh** - Home biome, waterlogged, reeds
- **Forest** - Dense trees, moderate difficulty
- **Desert** - Hot, resource-scarce
- **Tundra** - Cold, stamina drain
- **Savanna** - Open grasslands, many predators
- **Mountain** - Rocky, climbing required
- **Scrubland** - Dry brush, transitional

## Species

Player: River Otter

13 Predators:
- Fox, Wolf, Badger, Raccoon, Mongoose, Meerkat
- Honey Badger, Wolverine, Tasmanian Devil, Red Panda
- Wombat, Pangolin, Mink

15 Prey:
- Rabbit, Squirrel, Mouse, Fish (various), Frog
- Bird (various), Insect (various)

## Performance Targets

- 60 FPS on iPhone 13
- < 100 draw calls per frame
- < 500k vertices per frame
- < 200MB texture memory
