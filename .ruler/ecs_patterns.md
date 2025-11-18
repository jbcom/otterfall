
# ECS (Entity Component System) Patterns with Miniplex

## Core Philosophy

- **Entities** = Unique IDs with component bags
- **Components** = Pure data (no methods)
- **Systems** = Logic that operates on component queries

## Component Definition

```typescript
// Good - Pure data, explicit types
export interface TransformComponent {
  position: Vector3;
  rotation: Quaternion;
  scale: Vector3;
}

export interface HealthComponent {
  current: number;
  max: number;
  invulnerable: boolean;
}

// Bad - Methods in components
export interface BadComponent {
  value: number;
  update(): void; // ❌ No methods!
}
```

## World Creation

```typescript
import { World } from 'miniplex';

export type Entity = {
  // Core components
  transform?: TransformComponent;
  mesh?: MeshComponent;
  
  // Gameplay components
  health?: HealthComponent;
  ai?: AIComponent;
  inventory?: InventoryComponent;
  
  // Metadata
  tags?: Set<string>;
  name?: string;
};

export const world = new World<Entity>();
```

## Entity Creation Patterns

```typescript
// Factory pattern for consistent creation
export function createOtter(position: Vector3): Entity {
  return world.add({
    name: 'Otter',
    tags: new Set(['player', 'creature']),
    transform: {
      position,
      rotation: new Quaternion(),
      scale: new Vector3(1, 1, 1),
    },
    health: {
      current: 100,
      max: 100,
      invulnerable: false,
    },
    mesh: {
      ref: null, // Will be set by rendering system
    },
  });
}
```

## Querying Entities

```typescript
// With required components
const movableEntities = world.with('transform', 'velocity');

// With excluded components
const livingEnemies = world
  .with('health', 'ai')
  .without('dead');

// Iteration
for (const entity of movableEntities) {
  entity.transform.position.add(entity.velocity);
}
```

## Archetype Pattern (Performance)

```typescript
// Pre-create archetypes for fast queries
const trees = world.archetype('transform', 'mesh', 'tree');
const enemies = world.archetype('transform', 'health', 'ai', 'enemy');

// Fast iteration (cache-friendly)
for (const enemy of enemies) {
  // All components guaranteed to exist
  updateAI(enemy.ai, enemy.transform);
}
```

## React Integration

```typescript
import { useEntities } from 'miniplex-react';

function PlayerHealthUI() {
  // Query for player entity
  const [player] = useEntities(world.with('player', 'health'));
  
  if (!player) return null;
  
  return (
    <div>
      Health: {player.health.current} / {player.health.max}
    </div>
  );
}
```

## System Update Pattern

```typescript
// Systems run in useFrame
function useHealthSystem() {
  const entities = world.with('health', 'regen');
  
  useFrame((state, delta) => {
    for (const entity of entities) {
      if (entity.health.current < entity.health.max) {
        entity.health.current = Math.min(
          entity.health.max,
          entity.health.current + entity.regen.rate * delta
        );
      }
    }
  });
}
```

## Component Addition/Removal (Runtime)

```typescript
// Add component
world.addComponent(entity, 'stunned', { duration: 2.0 });

// Remove component
world.removeComponent(entity, 'stunned');

// Check existence
if ('stunned' in entity) {
  // Entity is stunned
}
```

## Zustand + ECS Bridge

```typescript
// Sync ECS data to Zustand for UI
function useECSSync() {
  const updateUI = useGameStore(s => s.updateUI);
  
  useFrame(() => {
    const [player] = world.with('player', 'health', 'transform');
    if (!player) return;
    
    updateUI({
      health: player.health.current,
      position: player.transform.position.toArray(),
    });
  });
}
```

## Tags Pattern (Flexible Grouping)

```typescript
// Good for dynamic categorization
export function createEnemy(type: string, position: Vector3) {
  return world.add({
    tags: new Set(['enemy', type, 'hostile']),
    transform: { position, /* ... */ },
    health: { /* ... */ },
  });
}

// Query by tag
function getDamageableEntities() {
  return world.with('tags', 'health').filter(e => 
    e.tags.has('enemy') || e.tags.has('npc')
  );
}
```

## Performance Tips

1. **Batch updates** - Don't add/remove components in tight loops
2. **Use archetypes** - Pre-define common entity types
3. **Avoid deep nesting** - Keep component data flat
4. **Cache queries** - Don't recreate archetype queries every frame
5. **Minimize watchers** - Only use `useEntities` when React needs updates

## Anti-Patterns

### ❌ God Components
```typescript
// Bad - Kitchen sink component
interface EntityComponent {
  health: number;
  position: Vector3;
  inventory: Item[];
  quests: Quest[];
  // ... 50 more fields
}

// Good - Split into focused components
interface HealthComponent { current: number; max: number; }
interface TransformComponent { position: Vector3; /* ... */ }
interface InventoryComponent { items: Item[]; slots: number; }
```

### ❌ Component Mutation Outside Systems
```typescript
// Bad - Direct mutation in React component
function AttackButton() {
  const [enemy] = useEntities(world.with('enemy'));
  
  const handleClick = () => {
    enemy.health.current -= 10; // ❌ Breaks reactivity
  };
}

// Good - Use command pattern or events
function AttackButton() {
  const attackEnemy = useGameStore(s => s.attackEnemy);
  
  const handleClick = () => {
    attackEnemy(enemyId); // System handles mutation
  };
}
```

### ❌ Circular Dependencies
```typescript
// Bad - Components reference each other
interface OwnerComponent {
  owned: Entity[]; // ❌ Entities referencing entities
}

// Good - Use IDs or tags
interface OwnerComponent {
  ownedIds: string[];
}
```
