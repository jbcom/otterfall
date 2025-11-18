# Rivermarsh ECS Architecture & Integration Plan

## Overview
This document defines how our entire game fits together: **Miniplex ECS** (data) + **Yuka AI** (simulation) + **React Three Fiber** (rendering).

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  React Three Fiber Components (R3F)                         │
│  - Read ECS state via Miniplex React hooks                  │
│  - Render GLB models from Meshy                             │
│  - Apply SDF shaders for fur/water/nature                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                     SIMULATION LAYER                         │
│  Yuka AI EntityManager                                       │
│  - Vehicle steering behaviors (flee, seek, wander)           │
│  - State machines (idle → hunt → attack → eat)              │
│  - Goal-driven AI (gather food, rest, patrol)               │
│  - Pathfinding (NavMesh for complex terrain)                │
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
           → ECS Component updated (AIComponent.currentState = 'flee')
           → AnimationComponent.currentAnimation = FLEE_ANIM_ID
           → R3F (Play animation on GLB model)

Combat     → ECS CombatSystem (damage calculation)
           → Update CombatComponent.health
           → If health < fleeThreshold → Yuka.StateMachine.changeTo('flee')
           → AnimationComponent = HIT_ANIM
           → R3F (Play hit animation + blood particle effect)
```

## Component-to-Yuka Mapping

### Our ECS Components → Yuka Concepts

| ECS Component | Yuka Class | Integration |
|---------------|------------|-------------|
| `MovementComponent` | `Vehicle` | Yuka Vehicle drives position/velocity, we sync back to ECS |
| `AIComponent` | `StateMachine` + `Goal` | Yuka handles state transitions, we read current state |
| `CombatComponent.target` | `Vehicle.target` | Share target reference between systems |
| `AnimationComponent` | None (we manage) | Read Yuka state, map to Meshy animation ID |
| `SpeciesComponent` | `Vehicle` properties | Configure maxSpeed, mass based on species |

### Bridge Pattern

```typescript
// Each ECS entity with AI gets a paired Yuka Vehicle
interface YukaBridge {
  ecsEntityId: string;           // Miniplex entity ID
  yukaVehicle: YUKA.Vehicle;     // Yuka AI entity
  stateMachine: YUKA.StateMachine;
}

// Systems update both in sync
function syncECStoYuka(entity, bridge) {
  // Read ECS data → write to Yuka
  bridge.yukaVehicle.position.copy(entity.movement.position);
  bridge.yukaVehicle.maxSpeed = entity.movement.runSpeed;
}

function syncYukaToECS(bridge, entity) {
  // Read Yuka simulation → write to ECS
  entity.movement.position = bridge.yukaVehicle.position.toArray();
  entity.movement.velocity = bridge.yukaVehicle.velocity.toArray();
  entity.ai.currentState = bridge.stateMachine.currentState.name;
}
```

## Test-Driven Development (TDD) Plan

### Phase 1: ECS Data Tests (No Rendering)

**Goal**: Validate game rules work in pure data

```typescript
// tests/ecs/combat.test.ts
describe('Combat System', () => {
  it('otter bite vs rabbit should kill in 4 hits', () => {
    const otter = createPredator('otter');
    const rabbit = createPrey('rabbit');
    
    for (let i = 0; i < 4; i++) {
      applyCombat(otter.combat.attacks[0], rabbit.combat);
    }
    
    expect(rabbit.combat.health).toBeLessThanOrEqual(0);
  });
  
  it('prey flees when health < 90%', () => {
    const rabbit = createPrey('rabbit');
    rabbit.combat.health = 89; // Below flee threshold
    
    updateAI(rabbit, deltaTime);
    
    expect(rabbit.ai.currentState).toBe('flee');
  });
});
```

### Phase 2: Yuka AI Integration Tests

**Goal**: Ensure Yuka behaviors work correctly

```typescript
// tests/integration/yuka-ai.test.ts
describe('Yuka AI Integration', () => {
  it('prey vehicle flees from predator', () => {
    const yukaPrey = new YUKA.Vehicle();
    const fleeBehavior = new YUKA.FleeBehavior(predatorPos, 10);
    yukaPrey.steering.add(fleeBehavior);
    
    entityManager.add(yukaPrey);
    entityManager.update(1.0); // 1 second
    
    const distanceAfter = yukaPrey.position.distanceTo(predatorPos);
    expect(distanceAfter).toBeGreaterThan(initialDistance);
  });
  
  it('pack wolves coordinate via OffsetPursuit', () => {
    const leader = createWolf();
    const follower1 = createWolf();
    const follower2 = createWolf();
    
    // Formation: leader in front, two flanking behind
    follower1.steering.add(new YUKA.OffsetPursuitBehavior(leader, offset1));
    follower2.steering.add(new YUKA.OffsetPursuitBehavior(leader, offset2));
    
    simulateSeconds(5);
    
    // Verify formation maintained
    expect(follower1.position.distanceTo(leader.position + offset1)).toBeLessThan(1.0);
  });
});
```

### Phase 3: Game Balance Tests

**Goal**: Tune numbers until it feels right

```typescript
// tests/balance/ecosystem.test.ts
describe('Ecosystem Balance', () => {
  it('predators can catch 70% of prey encounters', () => {
    const results = [];
    for (let i = 0; i < 100; i++) {
      const fox = createPredator('fox');
      const rabbit = createPrey('rabbit');
      const caught = simulateChase(fox, rabbit, maxDuration: 30);
      results.push(caught);
    }
    
    const successRate = results.filter(Boolean).length / 100;
    expect(successRate).toBeGreaterThan(0.65);
    expect(successRate).toBeLessThan(0.75);
  });
  
  it('marsh biome sustains 2-3 otters per km²', () => {
    const marsh = createBiome('marsh', size: 1000x1000);
    spawnPredators(marsh, species: 'otter', count: 3);
    
    simulateDays(30);
    
    // All otters should survive if resources are balanced
    const survivors = marsh.entities.filter(e => 
      e.species.type === 'otter' && e.combat.health > 0
    );
    expect(survivors.length).toBeGreaterThanOrEqual(2);
  });
});
```

### Phase 4: Rendering Tests

**Goal**: Ensure visuals match data

```typescript
// tests/rendering/sync.test.ts
describe('ECS to R3F Sync', () => {
  it('GLB model position matches ECS entity position', () => {
    const entity = createOtter();
    entity.movement.position = [10, 0, 5];
    
    renderFrame();
    
    const mesh = getRenderedMesh(entity.id);
    expect(mesh.position.toArray()).toEqual([10, 0, 5]);
  });
  
  it('animation plays when state changes', () => {
    const entity = createRabbit();
    entity.ai.currentState = 'flee';
    
    updateAnimation(entity);
    renderFrame();
    
    expect(entity.animation.currentAnimation).toBe(FLEE_ANIM_ID);
    const mesh = getRenderedMesh(entity.id);
    expect(mesh.mixer.clipAction(FLEE_ANIM_ID).isRunning()).toBe(true);
  });
});
```

## System Execution Order

```
Every Frame (60 FPS):
  1. TimeSystem.update()        → Advance time, update sun position
  2. WeatherSystem.update()     → Transition weather, apply modifiers
  3. YukaEntityManager.update() → Run all AI/steering behaviors
  4. CombatSystem.update()      → Process attacks, apply damage
  5. SpawnSystem.update()       → Spawn new entities based on biome rules
  6. AnimationSystem.update()   → Select animations based on state
  7. SyncToR3F()                → Update all mesh positions/rotations
  8. R3F.render()               → Three.js renders frame
```

## Meshy Pre-Build Process

```
Pre-Build Script (runs BEFORE game starts):
  1. Read all SPECIES_DEFINITIONS
  2. For each species:
     a. Check if public/assets/models/{species}/ exists
     b. If not:
        - POST to Meshy API (preview mode, sculpture style)
        - Save task ID to {species}/meshy-task.json
        - Poll until SUCCEEDED
        - Download GLB
        - POST to Meshy API (auto-rig)
        - Save rigged GLB to {species}/model.glb
        - Save animation mappings to {species}/animations.json
     c. If exists:
        - Log "Model already generated, skipping"
  3. Exit with success

Runtime (game loads):
  1. Load all GLB models from public/assets/models/{species}/
  2. Load animation mappings
  3. Create entity instances
  4. Sync with Yuka
  5. Start game
```

## Folder Structure (Final)

```
client/src/
├── ecs/
│   ├── components/           # Data definitions
│   │   ├── BiomeComponent.ts
│   │   ├── WeatherComponent.ts
│   │   ├── TimeOfDayComponent.ts
│   │   ├── SpeciesComponent.ts
│   │   ├── CombatComponent.ts
│   │   ├── MovementComponent.ts
│   │   ├── AIComponent.ts
│   │   ├── AnimationComponent.ts
│   │   └── BiomeResourceComponent.ts
│   ├── systems/             # Game logic
│   │   ├── TimeSystem.ts
│   │   ├── WeatherSystem.ts
│   │   ├── SpawnSystem.ts
│   │   ├── CombatSystem.ts
│   │   ├── AnimationSystem.ts
│   │   └── YukaSyncSystem.ts
│   ├── entities/            # Entity factories
│   │   ├── createPredator.ts
│   │   ├── createPrey.ts
│   │   └── createBiomeResource.ts
│   └── world.ts             # Miniplex ECS world instance
├── ai/
│   ├── behaviors/           # Yuka steering behaviors
│   ├── states/              # Yuka state machines
│   └── yukaManager.ts       # EntityManager wrapper
├── rendering/
│   ├── creatures/           # R3F components for GLB models
│   ├── environment/         # SDF shaders for nature
│   └── effects/             # Post-processing
└── scripts/
    └── generateMeshyModels.ts  # Pre-build script
```

## Success Criteria (How We Know It Works)

1. **Data Layer**: All tests pass, combat balance feels right
2. **AI Layer**: Prey flee realistically, predators hunt effectively, packs coordinate
3. **Rendering**: 60 FPS on iPhone 13, animations smooth, no visual glitches
4. **Integration**: ECS → Yuka → R3F stays in sync, no desync bugs
5. **Content**: 13 predators, 15 prey species all generated and animated

## Next Steps

1. ✅ Components defined (DONE)
2. Install Yuka: `npm install yuka`
3. Write entity factories (createPredator, createPrey)
4. Implement core systems (Time, Weather, Spawn)
5. Build Yuka integration (YukaSyncSystem)
6. Write TDD tests for combat balance
7. Run pre-build script to generate all Meshy models
8. Build R3F rendering layer
9. Integrate and test full pipeline
10. Balance and polish

---

**Philosophy**: Design → Test → Build → Render (in that order)
