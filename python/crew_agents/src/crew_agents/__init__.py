"""
CrewAI Agents for Rivermarsh game development.

This package provides autonomous AI crews that design and implement
game systems, following the CrewAI @CrewBase pattern with OpenRouter.

Usage:
    from crew_agents import GameDesignFlow, ImplementationFlow, AssetGenerationFlow
    
    # Run the complete design phase
    design = await GameDesignFlow().kickoff_async()
    
    # Then run implementation
    impl = await ImplementationFlow().kickoff_async(inputs=design)
    
    # Or generate assets
    assets = await AssetGenerationFlow().kickoff_async(inputs=design)
"""

from crew_agents.flows import (
    GameDesignFlow,
    ImplementationFlow,
    AssetGenerationFlow,
)

from crew_agents.crews import (
    WorldDesignCrew,
    CreatureDesignCrew,
    GameplayDesignCrew,
    ECSImplementationCrew,
    RenderingCrew,
    AssetPipelineCrew,
    QAValidationCrew,
)

__version__ = "0.2.0"

__all__ = [
    # Flows (primary interface)
    "GameDesignFlow",
    "ImplementationFlow",
    "AssetGenerationFlow",
    # Crews (for direct use if needed)
    "WorldDesignCrew",
    "CreatureDesignCrew",
    "GameplayDesignCrew",
    "ECSImplementationCrew",
    "RenderingCrew",
    "AssetPipelineCrew",
    "QAValidationCrew",
]
