# Backend System Contracts

**Purpose:** Type definitions and interfaces that CrewAI must implement for each backend system.

## Contract Requirements

Each CrewAI-delivered system MUST include:

1. **README Spec** - Architecture, usage, API documentation
2. **Typed Exports** - TypeScript/Python packages with full type coverage
3. **Mock Data Fixtures** - Sample data for testing frontend integration
4. **Unit Tests** - Full coverage with passing CI
5. **Integration Harness** - CLI or programmatic interface for validation
6. **Changelog** - Semantic versioning and migration notes

## Parallel Development Batches

### Batch 1 (Independent, Run in Parallel)
- **ECS Component Schemas** → `shared/backend/ecs_world/components/`
- **DFU Data Analysis** → `shared/backend/dfu_analysis/parsers/`

### Batch 2 (Depends on Batch 1)
- **Yuka AI Integration** → `shared/backend/yuka_ai/bridges/`
- **RPG Systems** → `shared/backend/rpg_systems/{leveling,inventory,quests}/`

### Batch 3 (Depends on Batch 1 & 2)
- **Rendering Pipeline** → `shared/backend/rendering_pipeline/{sdf,instancing,lod}/`

## Integration Points

**Agent Responsibility:**
- `client/src/prototypes/` - Visual prototypes and UI
- `client/src/components/` - Material UI components
- Integration testing of CrewAI systems

**CrewAI Responsibility:**
- `shared/backend/<system>/` - Backend implementation
- `client/src/ecs/systems/` - ECS system implementations
- Unit tests and documentation

## File Structure

```
shared/
├── contracts/           # Type definitions (this folder)
│   ├── BiomeContract.ts
│   ├── SpeciesContract.ts
│   └── QuestContract.ts
└── backend/
    ├── ecs_world/       # CrewAI: ECS implementation
    ├── dfu_analysis/    # CrewAI: Daggerfall Unity parser
    ├── yuka_ai/         # CrewAI: AI integration
    ├── rendering_pipeline/ # CrewAI: SDF/instancing
    └── rpg_systems/     # CrewAI: Leveling/inventory/quests

client/src/
├── prototypes/          # Agent: Visual prototypes
├── components/          # Agent: UI components
├── ecs/
│   ├── systems/         # CrewAI: System implementations
│   └── components/      # CrewAI: Component schemas
└── ai/                  # CrewAI: Yuka bridges
```

## Validation Checkpoints

Before Agent integrates CrewAI work:

1. **Schema Review** - Type compatibility with existing code
2. **Headless Simulation** - Run without R3F to verify logic
3. **R3F Adapter Test** - Ensure rendering integration works
4. **CI Passing** - All unit/integration tests green
5. **Manual Spot Check** - Agent reviews code quality
