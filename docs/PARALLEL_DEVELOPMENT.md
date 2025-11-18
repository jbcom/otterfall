# Parallel Development Strategy

**Last Updated:** Current session

## Overview

CrewAI handles backend system implementations while Agent focuses on frontend prototypes and user collaboration.

## Division of Responsibility

### CrewAI (Backend Systems)
**Technology:** OpenRouter with auto-routing (Claude 3.5 Sonnet, GPT-4o-mini, Codestral)
**MCP Servers:** Code analysis, documentation, web search

**Systems to Implement:**
1. **ECS World** - Complete system implementations
2. **Daggerfall Unity Analysis** - Parse and map to natural world
3. **Yuka AI Integration** - Behavior systems and pooling
4. **Rendering Pipeline** - SDF, instancing, LOD
5. **RPG Systems** - Leveling, inventory, quests, dialogue

### Agent (Frontend & Integration)
**Focus:** User collaboration on design decisions

**Responsibilities:**
1. **Visual Prototypes** - Biome design, creature placement
2. **UI/UX** - Material UI components, control panels
3. **Integration** - Connect CrewAI systems to R3F rendering
4. **Validation** - Review and test CrewAI deliverables

## Parallel Execution Plan

### Batch 1: Foundation (Run in Parallel)
```
┌─────────────────────────┐     ┌─────────────────────────┐
│   ECS Component Schema  │     │   DFU Data Analysis     │
│                         │     │                         │
│ CrewAI Task 1          │     │ CrewAI Task 2          │
│ - Component definitions │     │ - Parse creature stats  │
│ - Type exports          │     │ - Map to natural world  │
│ - Mock fixtures         │     │ - Export data packs     │
└─────────────────────────┘     └─────────────────────────┘
```

**Deliverables:**
- `shared/backend/ecs_world/components/` - All component TypeScript definitions
- `shared/backend/dfu_analysis/data/` - Parsed DFU creature/terrain data
- Unit tests + README for each

**Agent Work (Parallel):**
- Build prototype for biome visualization
- Design creature placement UI
- Refine control panel UX

---

### Batch 2: Core Systems (Depends on Batch 1)
```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   Yuka AI Bridge     │  │   RPG: Leveling      │  │   RPG: Inventory     │
│                      │  │                      │  │                      │
│ CrewAI Task 3       │  │ CrewAI Task 4       │  │ CrewAI Task 5       │
│ - Species behaviors  │  │ - XP calculation     │  │ - Item management    │
│ - State machines     │  │ - Stat progression   │  │ - Storage system     │
│ - Performance pools  │  │ - Skill trees        │  │ - Equipment slots    │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

**Deliverables:**
- `shared/backend/yuka_ai/` - AI integration with ECS
- `shared/backend/rpg_systems/leveling/` - Leveling logic
- `shared/backend/rpg_systems/inventory/` - Inventory system
- Integration harness + tests

**Agent Work (Parallel):**
- Build inventory UI prototype
- Design leveling progression visuals
- Test AI behaviors in diorama

---

### Batch 3: Rendering (Depends on Batch 1 & 2)
```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   SDF Library        │  │   Instancing System  │  │   LOD & Pathfinding  │
│                      │  │                      │  │                      │
│ CrewAI Task 6       │  │ CrewAI Task 7       │  │ CrewAI Task 8       │
│ - Water shaders      │  │ - Grass/reeds        │  │ - Mobile LOD         │
│ - Fog/caustics       │  │ - GPU culling        │  │ - Pathfinding mesh   │
│ - Fur effects        │  │ - Billboard system   │  │ - Navigation         │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

**Deliverables:**
- `shared/backend/rendering_pipeline/sdf/` - Shader library
- `shared/backend/rendering_pipeline/instancing/` - Instance mesh system
- `shared/backend/rendering_pipeline/lod/` - LOD and pathfinding
- Performance benchmarks

**Agent Work (Parallel):**
- Integrate SDF shaders into prototypes
- Build creature spawning UI
- Test rendering performance

---

## Integration Workflow

```
┌─────────────┐
│  CrewAI     │
│  Delivers   │
│  Backend    │
└──────┬──────┘
       │
       ├─► Unit Tests (Auto CI)
       │
       ├─► Schema Validation
       │
       ├─► Headless Simulation
       │
       ▼
┌─────────────┐
│   Agent     │
│  Reviews &  │
│  Integrates │
└──────┬──────┘
       │
       ├─► R3F Adapter Test
       │
       ├─► Prototype Integration
       │
       ├─► User Validation
       │
       ▼
┌─────────────┐
│   Merge to  │
│     Main    │
└─────────────┘
```

## File Structure

```
rivermarsh/
├── shared/
│   ├── contracts/              # Type definitions (Agent creates)
│   │   ├── BiomeContract.ts
│   │   ├── SpeciesContract.ts
│   │   └── QuestContract.ts
│   └── backend/                # CrewAI implementations
│       ├── ecs_world/
│       ├── dfu_analysis/
│       ├── yuka_ai/
│       ├── rendering_pipeline/
│       └── rpg_systems/
├── client/src/
│   ├── prototypes/             # Agent: Visual prototypes
│   ├── components/             # Agent: UI components
│   ├── ecs/
│   │   ├── systems/            # CrewAI: System implementations
│   │   └── components/         # CrewAI: Component schemas
│   └── ai/                     # CrewAI: Yuka bridges
└── python/
    └── crew_agents/            # CrewAI orchestration
```

## Communication Protocol

### CrewAI → Agent
**Format:** GitHub-style issue comments in deliverable README
- **Status:** "Ready for review" | "Blocked" | "In progress"
- **Dependencies:** List of unmet requirements
- **Tests:** Link to test results
- **Notes:** Integration guidance

### Agent → CrewAI
**Format:** Contract updates in `shared/contracts/`
- **Schema changes:** Update TypeScript interfaces
- **Requirements:** Add comments to contract files
- **Priorities:** Update batch order in this doc

## Current Status

### ✅ Completed
- Parallel development strategy defined
- Contract structure created
- Batch decomposition plan

### 🔄 In Progress
- Agent: Biome selector prototype (DONE, awaiting user feedback)
- Agent: Setting up CrewAI Batch 1 tasks

### ⏳ Queued
- Batch 1: ECS schemas + DFU analysis
- Batch 2: Yuka AI + RPG systems
- Batch 3: Rendering pipeline

## Next Steps

1. **Agent:** Finalize contract definitions (BiomeContract, SpeciesContract, QuestContract)
2. **Agent:** Configure CrewAI workflow for Batch 1
3. **CrewAI:** Begin parallel execution of Batch 1 tasks
4. **Agent:** Continue prototype work with user on visual design
5. **Both:** Daily sync on integration points

## Success Metrics

- **Parallelization:** Multiple systems building simultaneously
- **Quality:** All CrewAI deliverables pass CI + Agent review
- **Speed:** Backend systems complete while Agent focuses on design
- **Integration:** Smooth handoff from CrewAI to Agent for frontend work
