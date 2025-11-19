
"""Utility to run CrewAI flows from command line."""

import sys
from typing import Any, Dict


def run_tdd_prototype(requirements: Dict[str, Any]):
    """Run TDD Prototype Flow."""
    from crew_agents.flows.tdd_prototype_flow import TDDPrototypeFlow
    
    flow = TDDPrototypeFlow()
    result = flow.kickoff(inputs={"requirements": requirements})
    return result


def run_meshy_asset(species: str, prompt: str, retexture_prompt: str):
    """Run Meshy Asset Flow."""
    from crew_agents.flows.meshy_asset_flow import MeshyAssetFlow
    
    flow = MeshyAssetFlow()
    result = flow.kickoff(inputs={
        "species": species,
        "prompt": prompt,
        "retexture_prompt": retexture_prompt
    })
    return result


def run_prototype_assessment(prototypes: list):
    """Run Prototype to Production Flow."""
    from crew_agents.flows.prototype_to_production_flow import PrototypeToProductionFlow
    
    flow = PrototypeToProductionFlow()
    result = flow.kickoff(inputs={"prototypes": prototypes})
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m crew_agents.run_flow <flow_name> [args...]")
        print("\nAvailable flows:")
        print("  tdd_prototype")
        print("  meshy_asset <species> <prompt> <retexture_prompt>")
        print("  prototype_assessment <prototype1> <prototype2> ...")
        sys.exit(1)
    
    flow_name = sys.argv[1]
    
    if flow_name == "tdd_prototype":
        requirements = {"feature": "biome_selector"}
        run_tdd_prototype(requirements)
    
    elif flow_name == "meshy_asset":
        species = sys.argv[2] if len(sys.argv) > 2 else "otter"
        prompt = sys.argv[3] if len(sys.argv) > 3 else "A realistic otter"
        retexture = sys.argv[4] if len(sys.argv) > 4 else "grey fur variant"
        run_meshy_asset(species, prompt, retexture)
    
    elif flow_name == "prototype_assessment":
        prototypes = sys.argv[2:] if len(sys.argv) > 2 else ["biome_selector_diorama"]
        run_prototype_assessment(prototypes)
    
    else:
        print(f"Unknown flow: {flow_name}")
        sys.exit(1)
