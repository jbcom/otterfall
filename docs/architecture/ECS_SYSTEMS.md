
# ECS Systems Architecture

## Component Lifecycle

### Creation
```typescript
// Entity factory pattern
export function createPredator(spec: PredatorSpec): Entity {
  return world.createEntity({
    species: SpeciesComponent.create(spec),
    movement: MovementComponent.create(spec.baseSpeed),
    combat: CombatComponent.create(spec.health),
    ai: AIComponent.create('predator'),
  });
}
```

### Updates
Systems query entities and update components:

```typescript
// client/src/ecs/systems/MovementSystem.ts
export function MovementSystem(world: World, deltaTime: number) {
  for (const entity of world.with('movement', 'transform')) {
    const { movement, transform } = entity;
    transform.position.add(movement.velocity.multiplyScalar(deltaTime));
  }
}
```

### Destruction
```typescript
world.destroyEntity(entity);
```

## System Execution Order

**Mandatory sequence** (from [.ruler/AGENTS.md](rag://rag_source_14)):

1. **TimeSystem** - Advance world clock
2. **WeatherSystem** - Update atmospheric conditions
3. **SpawnSystem** - Create new entities in active chunks
4. **AISystem** - Update creature behaviors
5. **MovementSystem** - Apply velocity to positions
6. **CombatSystem** - Process attacks and damage
7. **AnimationSystem** - Update animation states
8. **YukaSyncSystem** - Sync Yuka entities with R3F meshes

## Component Integration Patterns

### ECS → R3F Rendering

```typescript
// client/src/components/OtterNPC.tsx
export function OtterNPC({ entity }: { entity: Entity }) {
  const transform = useComponentValue(entity, 'transform');
  const animation = useComponentValue(entity, 'animation');

  return (
    <group position={transform.position}>
      <AnimatedModel clip={animation.currentClip} />
    </group>
  );
}
```

### ECS → Material UI

```typescript
// client/src/stores/useUIState.ts
export const useUIState = create((set) => ({
  health: 100,
  updateFromECS: (playerEntity: Entity) => {
    const combat = playerEntity.combat;
    set({ health: combat.health });
  },
}));
```

## References

- [rendering_pipeline.md](../../client/.ruler/rendering_pipeline.md) - Render integration
- [ARCHITECTURE.md](../../client/src/ecs/ARCHITECTURE.md) - ECS implementation details
- [BiomeComponent.ts](../../client/src/ecs/components/BiomeComponent.ts) - Example component
