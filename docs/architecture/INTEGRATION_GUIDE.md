
# Agent Integration Guide

## Overview

This guide explains how to integrate CrewAI deliverables with the frontend codebase.

## Review Workflow

### 1. CrewAI Delivers Backend System

When CrewAI completes a task (e.g., `ecs_component_schemas`), you'll find:

```
shared/backend/ecs_world/
├── components/           # TypeScript component files
├── tests/               # Unit tests
├── fixtures/            # Mock data
└── README.md            # Usage documentation
```

### 2. Agent Reviews Deliverable

**Checklist**:
- [ ] All files in expected locations
- [ ] README.md explains usage clearly
- [ ] Unit tests pass (`npm test`)
- [ ] TypeScript types compile (`npm run typecheck`)
- [ ] No LSP errors in VS Code
- [ ] Mock fixtures cover all component types

**Review Command**:
```bash
# From project root
npm run validate:crewai shared/backend/ecs_world
```

### 3. Integration Steps

1. **Import components** into `client/src/ecs/components/`
2. **Run integration tests** to verify ECS→R3F sync
3. **Update prototype** (e.g., `biome_selector_diorama`) to use new components
4. **Test in browser** with user interaction
5. **Performance check** with profiler

### 4. Contract Updates

If CrewAI deliverable doesn't match contract:

**Option A - CrewAI Adjust**:
```bash
# Request CrewAI revision
process-compose process restart ecs_component_schemas
```

**Option B - Contract Update**:
```typescript
// Update shared/contracts/SpeciesContract.ts
// Document breaking change in DECISION_LOG.md
```

## Integration Patterns

### ECS Components → R3F

```typescript
// client/src/prototypes/biome_selector_diorama/useBiomeECS.ts
import { BiomeComponent } from 'shared/backend/ecs_world/components/BiomeComponent';

export function useBiomeECS() {
  const biomeEntity = world.createEntity({
    biome: BiomeComponent.create('marsh'), // Use CrewAI-delivered component
  });
}
```

### Backend Services → Frontend Hooks

```typescript
// If CrewAI delivers a service (e.g., YukaBridgeManager)
import { YukaBridgeManager } from 'shared/backend/yuka_ai/YukaBridgeManager';

export function useYukaAI(entity: Entity) {
  const bridge = useMemo(() => YukaBridgeManager.getBridge(entity), [entity]);
  // ...
}
```

## Troubleshooting

**Issue**: TypeScript import errors after CrewAI delivery

**Solution**:
```bash
# Regenerate type definitions
npm run build:types
```

**Issue**: Unit tests fail in CI

**Solution**:
```bash
# Run tests locally first
cd shared/backend/ecs_world
npm test -- --verbose
```

**Issue**: Performance regression after integration

**Solution**:
```bash
# Profile with React DevTools Profiler
npm run dev
# Navigate to prototype, record interaction, check Profiler tab
```

## References

- [PARALLEL_DEVELOPMENT.md](../PARALLEL_DEVELOPMENT.md) - Overall strategy
- [crewai_usage.md](./crewai_usage.md) - CrewAI task execution
- [shared/contracts/README.md](../../shared/contracts/README.md) - Contract specs
