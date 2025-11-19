
"""Meshy Asset Pipeline Flow - Generate → Rig → Animate → Retexture → Review."""

from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel
from typing import List, Dict, Any


class MeshyAssetState(BaseModel):
    """State for Meshy Asset workflow."""
    id: str = ""
    species: str = ""
    prompt: str = ""
    retexture_prompt: str = ""
    static_task_id: str = ""
    rigged_task_id: str = ""
    animations: List[Dict[str, Any]] = []
    retexture_task_id: str = ""
    review_results: Dict[str, Any] = {}


class MeshyAssetFlow(Flow[MeshyAssetState]):
    """
    Standard sequence for generating GLB assets via Meshy API.
    
    Steps:
    1. Generate static 3D model from text
    2. Add skeleton rigging
    3. Generate animation variants (parallel)
    4. Create retextured variant
    5. Human review of all variants
    """
    
    initial_state = MeshyAssetState
    name = "meshy_asset_flow"

    @start()
    def generate_static_model(self):
        """Text-to-3D static model generation."""
        from mesh_toolkit.services.text3d_service import Text3DService
        
        service = Text3DService()
        result = service.submit_task(
            species=self.state.species,
            prompt=self.state.prompt
        )
        
        self.state.static_task_id = result.task_id
        print(f"Static model task submitted: {result.task_id}")
        return result

    @listen(generate_static_model)
    def rig_model(self, static_result):
        """Add skeleton to model."""
        from mesh_toolkit.services.rigging_service import RiggingService
        
        service = RiggingService()
        result = service.submit_task(
            model_id=static_result.model_id
        )
        
        self.state.rigged_task_id = result.task_id
        print(f"Rigging task submitted: {result.task_id}")
        return result

    @listen(rig_model)
    def animate_variants(self, rigged_result):
        """Trigger parallel animation tasks."""
        from mesh_toolkit.services.animation_service import AnimationService
        
        service = AnimationService()
        
        # Submit walk animation
        walk = service.submit_task(
            model_id=rigged_result.model_id,
            animation_id="1"  # Walk
        )
        
        # Submit attack animation
        attack = service.submit_task(
            model_id=rigged_result.model_id,
            animation_id="4"  # Attack
        )
        
        self.state.animations = [
            {"name": "walk", "task_id": walk.task_id},
            {"name": "attack", "task_id": attack.task_id}
        ]
        
        print(f"Animation tasks submitted: walk={walk.task_id}, attack={attack.task_id}")
        return {"walk": walk, "attack": attack}

    @listen(animate_variants)
    def retexture_variant(self, anim_results):
        """Create color variant."""
        from mesh_toolkit.services.retexture_service import RetextureService
        
        service = RetextureService()
        result = service.submit_task(
            model_id=self.state.static_task_id,
            prompt=self.state.retexture_prompt
        )
        
        self.state.retexture_task_id = result.task_id
        print(f"Retexture task submitted: {result.task_id}")
        return result

    @listen(retexture_variant)
    def hitl_review(self, retexture_result):
        """Present all variants for human review."""
        print("\n=== Asset Review Required ===")
        print(f"Static model: {self.state.static_task_id}")
        print(f"Walk animation: {self.state.animations[0]['task_id']}")
        print(f"Attack animation: {self.state.animations[1]['task_id']}")
        print(f"Retextured variant: {self.state.retexture_task_id}")
        
        # In production, this loads HITLReviewControls with all 4 GLBs
        review_results = {
            "static": {"approved": True, "rating": 8},
            "walk": {"approved": True, "rating": 7},
            "attack": {"approved": True, "rating": 9},
            "variant": {"approved": True, "rating": 8},
            "notes": "All variants look good, ready for integration"
        }
        
        self.state.review_results = review_results
        return review_results
