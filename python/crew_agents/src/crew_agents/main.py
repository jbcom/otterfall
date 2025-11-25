"""
Main entry point for CrewAI flows.

Run with:
    uv run crew_agents design    # Run game design flow
    uv run crew_agents implement # Run implementation flow
    uv run crew_agents assets    # Run asset generation flow
    uv run crew_agents full      # Run complete pipeline
"""

import asyncio
import sys
from typing import Optional

from crew_agents.flows import (
    AssetGenerationFlow,
    GameDesignFlow,
    ImplementationFlow,
)


async def run_design_flow():
    """Run the game design flow."""
    print("=" * 60)
    print("🎮 RIVERMARSH GAME DESIGN FLOW")
    print("=" * 60)
    print()

    flow = GameDesignFlow()
    result = await flow.kickoff_async()

    print()
    print("=" * 60)
    print("📄 DESIGN OUTPUTS")
    print("=" * 60)

    # Save outputs to files
    if result.world_design:
        with open("output/world_design.md", "w") as f:
            f.write(result.world_design)
        print("✅ World design saved to output/world_design.md")

    if result.creature_design:
        with open("output/creature_design.md", "w") as f:
            f.write(result.creature_design)
        print("✅ Creature design saved to output/creature_design.md")

    if result.gameplay_design:
        with open("output/gameplay_design.md", "w") as f:
            f.write(result.gameplay_design)
        print("✅ Gameplay design saved to output/gameplay_design.md")

    return result


async def run_implementation_flow(design_state: Optional[dict] = None):
    """Run the implementation flow."""
    print("=" * 60)
    print("🏗️ RIVERMARSH IMPLEMENTATION FLOW")
    print("=" * 60)
    print()

    flow = ImplementationFlow()

    # Load design state if not provided
    if design_state:
        flow.state.world_design = design_state.get("world_design", "")
        flow.state.creature_design = design_state.get("creature_design", "")
        flow.state.gameplay_design = design_state.get("gameplay_design", "")
    else:
        # Try to load from files
        try:
            with open("output/world_design.md", "r") as f:
                flow.state.world_design = f.read()
            with open("output/creature_design.md", "r") as f:
                flow.state.creature_design = f.read()
            with open("output/gameplay_design.md", "r") as f:
                flow.state.gameplay_design = f.read()
            print("📂 Loaded design documents from output/")
        except FileNotFoundError:
            print("⚠️ No design documents found. Run 'design' flow first.")
            return None

    result = await flow.kickoff_async()

    # Save outputs
    if result.ecs_components:
        with open("output/ecs_components.ts", "w") as f:
            f.write(result.ecs_components)
        print("✅ ECS components saved to output/ecs_components.ts")

    if result.ecs_systems:
        with open("output/ecs_systems.ts", "w") as f:
            f.write(result.ecs_systems)
        print("✅ ECS systems saved to output/ecs_systems.ts")

    if result.rendering_code:
        with open("output/rendering.tsx", "w") as f:
            f.write(result.rendering_code)
        print("✅ Rendering code saved to output/rendering.tsx")

    return result


async def run_asset_flow(design_state: Optional[dict] = None, species: str = None):
    """Run the asset generation flow."""
    print("=" * 60)
    print("🎨 RIVERMARSH ASSET GENERATION FLOW")
    print("=" * 60)
    print()

    flow = AssetGenerationFlow()

    # Load design state
    if design_state:
        flow.state.creature_design = design_state.get("creature_design", "")
        flow.state.world_design = design_state.get("world_design", "")
    else:
        try:
            with open("output/creature_design.md", "r") as f:
                flow.state.creature_design = f.read()
            with open("output/world_design.md", "r") as f:
                flow.state.world_design = f.read()
            print("📂 Loaded design documents from output/")
        except FileNotFoundError:
            print("⚠️ No design documents found. Run 'design' flow first.")
            return None

    result = await flow.kickoff_async()
    return result


async def run_full_pipeline():
    """Run the complete pipeline: design → implement → assets."""
    print("=" * 60)
    print("🚀 RIVERMARSH FULL DEVELOPMENT PIPELINE")
    print("=" * 60)
    print()

    # Phase 1: Design
    print("\n📐 PHASE 1: DESIGN\n")
    design_result = await run_design_flow()

    if not design_result:
        print("❌ Design phase failed")
        return

    design_state = {
        "world_design": design_result.world_design,
        "creature_design": design_result.creature_design,
        "gameplay_design": design_result.gameplay_design,
    }

    # Phase 2: Implementation
    print("\n🏗️ PHASE 2: IMPLEMENTATION\n")
    impl_result = await run_implementation_flow(design_state)

    # Phase 3: Assets
    print("\n🎨 PHASE 3: ASSETS\n")
    asset_result = await run_asset_flow(design_state)

    print()
    print("=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)

    return {
        "design": design_result,
        "implementation": impl_result,
        "assets": asset_result,
    }


def main():
    """CLI entry point."""
    import os

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    if command == "design":
        asyncio.run(run_design_flow())
    elif command == "implement":
        asyncio.run(run_implementation_flow())
    elif command == "assets":
        species = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(run_asset_flow(species=species))
    elif command == "full":
        asyncio.run(run_full_pipeline())
    else:
        print("""
Rivermarsh CrewAI Development Pipeline

Usage:
    uv run crew_agents <command>

Commands:
    design      Run game design flow (World → Creatures → Gameplay)
    implement   Run implementation flow (ECS → Rendering)
    assets      Run asset generation flow (Meshy 3D models)
    full        Run complete pipeline

Environment:
    OPENROUTER_API_KEY  Required for LLM access
    MESHY_API_KEY       Required for asset generation

Examples:
    uv run crew_agents design
    uv run crew_agents assets otter
    uv run crew_agents full
        """)


if __name__ == "__main__":
    main()
