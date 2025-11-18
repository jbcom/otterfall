
# Reusable CrewAI Workflow Patterns

## Overview

The `crewbase.yaml` defines **reusable workflow patterns** using YAML anchors (`&name`) and aliases (`*name`). This ensures consistent TDD practices across all prototype development.

## Available Patterns

### 1. TDD Prototype Workflow (`&tdd_prototype_workflow`)

**4-phase standard pattern for ANY prototype:**

```yaml
design_phase → implementation_phase → validation_phase → documentation_phase
```

**Usage:**
```yaml
tasks:
  design_my_new_feature:
    <<: *tdd_prototype_workflow.design_phase
    description: |
      Design specs for my feature...
    # Override defaults as needed
    agent: rendering_engineer  # Already set by anchor
```

**Phases:**

1. **Design Phase**
   - Agent: `rendering_engineer`
   - Requires: `context: true`
   - HITL: `human_input: true` (approval before implementation)
   - Outputs: Technical design, dependency graph, acceptance criteria

2. **Implementation Phase**
   - Agent: `rendering_engineer`
   - Requires: `context_from_design: true`
   - Outputs: Component files, shaders, integration points

3. **Validation Phase**
   - Agent: `qa_validator`
   - Requires: `context_from_implementation: true`
   - HITL: `human_input: true` (approval before merge)
   - Outputs: Validation report, performance metrics, approval recommendation

4. **Documentation Phase**
   - Agent: `technical_writer`
   - Requires: `context_from_all: true`
   - Outputs: Updated ConPort, integration guide, handoff notes

### 2. Meshy Asset Workflow (`&meshy_asset_workflow`)

**Standard sequence for generating any species GLB assets:**

```yaml
api_sequence:
  - text3d_static      # Sculptured model
  - rigging            # Add skeleton
  - animation_default  # Walk/idle
  - animation_custom   # Attack/custom
  - retexture_variant  # Color variant
```

**Usage:**
```yaml
tasks:
  generate_beaver_assets:
    description: |
      Generate beaver GLB variants using Meshy.
      
      Follows standard workflow (see x-meshy-asset-workflow):
      - Static sculptured beaver
      - Rigged beaver
      - Animated (walk, attack)
      - Retextured (brown variant)
```

**Outputs:**
```
client/public/models/beaver/
├── static.glb
├── walk.glb
├── attack.glb
├── variant.glb
└── manifest.json
```

**Webhook Config:**
- Base URL: `http://0.0.0.0:8000/webhooks/meshy`
- Endpoints: `/static`, `/rigged`, `/animated_default`, `/animated_custom`, `/retextured`

## Creating New Workflows

### Example: Multi-Creature Diorama Workflow

```yaml
# In crewbase.yaml, add new anchor:
x-multi-creature-diorama-workflow: &multi_creature_diorama
  asset_generation_phase:
    agent: integration_specialist
    tasks:
      - Generate all creature GLBs
      - Download and cache
      - Update manifests
  
  scene_composition_phase:
    agent: rendering_engineer
    tasks:
      - Position creatures in diorama
      - Add environmental props
      - Configure lighting/camera
  
  behavior_programming_phase:
    agent: rendering_engineer  # or ai_specialist for Yuka integration
    tasks:
      - Attach AI state machines
      - Configure animations
      - Test interactions
  
  hitl_review_phase:
    agent: qa_validator
    human_input: true
    tasks:
      - Present diorama with all creatures
      - Collect ratings (1-10) for each
      - Record notes on behavior/appearance

# Then use it:
tasks:
  create_predator_prey_diorama:
    <<: *multi_creature_diorama.asset_generation_phase
    description: |
      Generate otter (predator) and fish (prey) for ecosystem demo.
```

## Best Practices

1. **Always anchor at top of file** (before `agents:` section)
2. **Use descriptive anchor names** (`&tdd_prototype_workflow`, not `&workflow1`)
3. **Override only what's necessary** - anchors provide sensible defaults
4. **Document in task description** which workflow is being used
5. **Validate YAML** before committing:
   ```bash
   yamllint python/crew_agents/crewbase.yaml
   ```

## When to Create New Workflows

Create a new reusable workflow when:
- ✅ Pattern repeats 3+ times across different features
- ✅ Sequence is well-understood and stable
- ✅ Team agrees this is "the right way" to do X

DON'T create workflows for:
- ❌ One-off tasks
- ❌ Experimental/unproven approaches
- ❌ Highly variable sequences

## References

- [YAML Anchors & Aliases Spec](https://yaml.org/spec/1.2.2/#3222-anchors-and-aliases)
- CrewAI DSL docs: `crewAI/docs/en/mcp/dsl-integration.mdx`
- Project workflow patterns: `python/crew_agents/.ruler/workflow_configuration.md`
