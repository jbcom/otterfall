
# Client-Side Development Standards

## Directory Structure (MANDATORY)

```
client/src/
├── components/        # React components (UI + 3D)
├── ecs/              # Entity Component System
│   ├── components/   # ECS component definitions
│   ├── entities/     # Entity factory functions
│   └── data/         # Static data (species, biomes, etc.)
├── stores/           # Zustand state management
├── lib/              # Utilities and helpers
├── prototypes/       # Experimental features (isolated)
└── pages/            # Route pages
```

## React Three Fiber Integration

### Component Guidelines
- Keep R3F components pure (no side effects in render)
- Use `useFrame` for animation, not `requestAnimationFrame`
- Prefer declarative over imperative Three.js calls

See [rendering_pipeline.md](./rendering_pipeline.md) for detailed render pass order.

## ECS Integration

Every game entity must:
1. Be created through factory functions in `ecs/entities/`
2. Have all required components defined in `ecs/components/`
3. Be queryable through Miniplex world

Example:
```typescript
import { createPrey } from '@/ecs/entities/createPrey';

const rabbit = createPrey(world, {
  species: 'rabbit',
  position: [0, 0, 0],
});
```

## Mobile Optimization

### Touch Controls Required
- Virtual joysticks for movement
- Tap zones for actions
- Responsive UI scaling

### Gyroscope Camera
- Smooth interpolation (lerp factor: 0.1)
- Dead zone for small movements
- Fallback to touch swipe

### Performance Testing
Test on actual devices or Chrome DevTools mobile emulation:
- iPhone 12 (mid-tier target)
- Pixel 5 (Android target)
- Throttle CPU 4x slowdown
