# Rivermarsh CrewAI Agents

Autonomous AI development crews for Rivermarsh game development.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GAME DESIGN FLOW                            │
├─────────────┬─────────────┬──────────────┬────────────────────┤
│ World       │ Creature    │ Gameplay     │ QA Validation      │
│ Design      │ Design      │ Design       │ (gates between     │
│ Crew        │ Crew        │ Crew         │  each crew)        │
└──────┬──────┴──────┬──────┴──────┬───────┴────────────────────┘
       │             │             │
       ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   IMPLEMENTATION FLOW                           │
├─────────────┬─────────────┬──────────────┬────────────────────┤
│ ECS         │ Systems     │ Rendering    │ QA Validation      │
│ Components  │ Engineer    │ Crew         │ (code review)      │
│ Crew        │             │              │                    │
└──────┬──────┴──────┬──────┴──────┬───────┴────────────────────┘
       │             │             │
       ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ASSET GENERATION FLOW                         │
├─────────────┬─────────────┬──────────────┬────────────────────┤
│ Asset Specs │ Meshy       │ Automated    │ HITL              │
│             │ Prompts     │ QA           │ (Human Review)     │
└─────────────┴─────────────┴──────────────┴────────────────────┘
```

## Crews

### Design Crews

| Crew | Agents | Purpose |
|------|--------|---------|
| **WorldDesignCrew** | World Architect, Biome Designer, Ecosystem Specialist | Define world structure, biomes, ecosystems |
| **CreatureDesignCrew** | Creature Designer, Behavior Specialist, Stats Balancer | Design species, behaviors, balance |
| **GameplayDesignCrew** | Systems Designer, Combat Designer, Economy Designer | Core loops, combat, progression |

### Implementation Crews

| Crew | Agents | Purpose |
|------|--------|---------|
| **ECSImplementationCrew** | ECS Architect, TypeScript Engineer, Systems Engineer | Miniplex components and systems |
| **RenderingCrew** | Shader Engineer, R3F Specialist, Performance Engineer | Visual systems, shaders, optimization |

### Operations Crews

| Crew | Agents | Purpose |
|------|--------|---------|
| **AssetPipelineCrew** | Asset Director, Prompt Engineer, Asset QA | 3D asset generation via Meshy |
| **QAValidationCrew** | Design Reviewer, Code Reviewer, Integration Tester | Quality gates between phases |

## Usage

### Environment Setup

```bash
# Required environment variables
export OPENROUTER_API_KEY="your-key-here"
export MESHY_API_KEY="your-key-here"  # For asset generation
```

### Running Flows

```bash
# Run game design (World → Creatures → Gameplay)
uv run crew_agents design

# Run implementation (ECS → Rendering)
uv run crew_agents implement

# Run asset generation
uv run crew_agents assets

# Run everything
uv run crew_agents full
```

### Programmatic Usage

```python
import asyncio
from crew_agents import GameDesignFlow, ImplementationFlow, AssetGenerationFlow

async def main():
    # Run design phase
    design_flow = GameDesignFlow()
    design_result = await design_flow.kickoff_async()
    
    # Run implementation with design outputs
    impl_flow = ImplementationFlow()
    impl_flow.state.world_design = design_result.world_design
    impl_flow.state.creature_design = design_result.creature_design
    impl_flow.state.gameplay_design = design_result.gameplay_design
    impl_result = await impl_flow.kickoff_async()
    
    # Run asset generation
    asset_flow = AssetGenerationFlow()
    asset_flow.state.creature_design = design_result.creature_design
    asset_result = await asset_flow.kickoff_async()

asyncio.run(main())
```

## OpenRouter Configuration

All agents use OpenRouter with automatic model selection by default:

```python
from crew_agents.config.llm import get_llm

# Default (auto-selects best model)
llm = get_llm("openrouter/auto")

# Or specify a model
llm = get_llm("openrouter/anthropic/claude-3.5-sonnet")
llm = get_llm("openrouter/openai/gpt-4o")
```

## Flow Patterns

### Self-Evaluation Loop

Each design crew output passes through QA validation:

```
Design → QA Review → [APPROVED] → Next Phase
              │
              └────→ [REJECTED] → Retry (max 2x) → Next Phase
```

### Human-in-the-Loop (HITL)

Asset generation includes human approval gates:

```
Generate Asset → Automated QA → Create GitHub Issue → Human Approval → Integrate
```

## Directory Structure

```
src/crew_agents/
├── __init__.py           # Package exports
├── main.py               # CLI entry point
├── config/
│   ├── __init__.py
│   └── llm.py            # OpenRouter LLM configuration
├── crews/
│   ├── world_design/
│   │   ├── world_design_crew.py
│   │   └── config/
│   │       ├── agents.yaml
│   │       └── tasks.yaml
│   ├── creature_design/
│   ├── gameplay_design/
│   ├── ecs_implementation/
│   ├── rendering/
│   ├── asset_pipeline/
│   └── qa_validation/
├── flows/
│   ├── game_design_flow.py
│   ├── implementation_flow.py
│   └── asset_generation_flow.py
└── tools/                # Custom tools (future)
```

## Development

### Adding a New Crew

1. Create directory: `src/crew_agents/crews/new_crew/`
2. Add config files: `config/agents.yaml`, `config/tasks.yaml`
3. Create crew class with `@CrewBase` decorator
4. Add to `crews/__init__.py`

### Testing

```bash
# Run crew agent tests
uv run pytest tests/ -v
```

## See Also

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenRouter](https://openrouter.ai/)
- [Meshy API](https://www.meshy.ai/)
- Project guidelines: `python/.ruler/AGENTS.md`
