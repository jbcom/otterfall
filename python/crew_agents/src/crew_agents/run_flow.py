
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


def run_asset_integration(asset_manifest: Dict[str, Any]):
    """Run Asset Integration Flow."""
    from crew_agents.flows.asset_integration_flow import AssetIntegrationFlow
    
    flow = AssetIntegrationFlow()
    result = flow.kickoff(inputs={"asset_manifest": asset_manifest})
    return result


def run_hitl_review(content_type: str, content_url: str):
    """Run HITL Review Flow."""
    from crew_agents.flows.hitl_review_flow import HITLReviewFlow
    
    flow = HITLReviewFlow()
    result = flow.kickoff(inputs={
        "content_type": content_type,
        "content_url": content_url
    })
    return result


def run_batch_generation(species_list: list):
    """Run Batch Generation Flow."""
    from crew_agents.flows.batch_generation_flow import BatchGenerationFlow
    
    flow = BatchGenerationFlow()
    result = flow.kickoff(inputs={"species_list": species_list})
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m crew_agents.run_flow <flow_name> [args...]")
        print("\nAvailable flows:")
        print("  tdd_prototype")
        print("  meshy_asset <species> <prompt> <retexture_prompt>")
        print("  prototype_assessment <prototype1> <prototype2> ...")
        print("  asset_integration")
        print("  hitl_review <content_type> <content_url>")
        print("  batch_generation <species1> <species2> ...")
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
    
    elif flow_name == "asset_integration":
        manifest = {
            "species": sys.argv[2] if len(sys.argv) > 2 else "otter",
            "glb_url": sys.argv[3] if len(sys.argv) > 3 else "",
            "animations": []
        }
        run_asset_integration(manifest)
    
    elif flow_name == "hitl_review":
        content_type = sys.argv[2] if len(sys.argv) > 2 else "asset"
        content_url = sys.argv[3] if len(sys.argv) > 3 else ""
        run_hitl_review(content_type, content_url)
    
    elif flow_name == "batch_generation":
        species_list = sys.argv[2:] if len(sys.argv) > 2 else ["otter", "beaver", "muskrat"]
        run_batch_generation(species_list)
    
    else:
        print(f"Unknown flow: {flow_name}")
        sys.exit(1)
