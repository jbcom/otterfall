# Cross-Cutting Technical Standards

These rules apply across all components of the Rivermarsh project.

## TypeScript Standards

### Strict Mode Requirements
```typescript
// tsconfig.json must have:
"strict": true,
"noUncheckedIndexedAccess": true,
"noImplicitReturns": true
```

### No `any` Types
```typescript
// ❌ Bad
function processData(data: any) { }

// ✅ Good
function processData<T extends Record<string, unknown>>(data: T) { }
```

### Type Exports
Every module must export its public types:
```typescript
export type { Entity, Component, System };
```

## State Management

### Zustand Store Pattern
```typescript
import { create } from 'zustand';

export const useStore = create<State>((set, get) => ({
  // State
  value: 0,

  // Actions
  increment: () => set(state => ({ value: state.value + 1 })),
}));
```

### ECS Component Queries
```typescript
// Use Miniplex queries, not manual filtering
const movingEntities = world.with('transform', 'velocity');
```

## Performance Standards

### Mobile Budget (60 FPS target)
- **Draw Calls**: < 100 per frame
- **Vertices**: < 500k per frame
- **Texture Memory**: < 200MB total
- **Shader Instructions**: < 200 per pixel

### Profiling Required
Before optimizing, measure with:
```typescript
import { Perf } from 'r3f-perf';
// Add <Perf /> to scene during development
```

## Error Handling

### Always Handle Async Errors
```typescript
// ❌ Bad
async function loadAsset() {
  const data = await fetch(url);
}

// ✅ Good
async function loadAsset(): Promise<Result<Asset, Error>> {
  try {
    const data = await fetch(url);
    return { ok: true, value: data };
  } catch (error) {
    return { ok: false, error };
  }
}
```

## File Organization

### Import Order
1. External dependencies
2. Internal absolute imports (`@/...`)
3. Relative imports (`./`, `../`)
4. Type imports (at end with `import type`)

```typescript
import React from 'react';
import { Canvas } from '@react-three/fiber';
import { useGame } from '@/lib/stores/useGame';
import { Player } from './Player';
import type { Entity } from '@/ecs/world';