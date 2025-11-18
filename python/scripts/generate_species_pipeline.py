
#!/usr/bin/env python3
"""
Reads client/src/ecs/data/predatorSpecies.ts
Generates all Meshy assets
Writes manifest to shared/backend/asset_pipeline/manifests/{species}.json
"""

import json
import asyncio
from pathlib import Path
from mesh_toolkit.services.text3d_service import Text3DService
from mesh_toolkit.services.rigging_service import RiggingService
from mesh_toolkit.services.animation_service import AnimationService
from mesh_toolkit.persistence.repository import TaskRepository

async def main():
    # 1. Parse TypeScript species definitions
    species_file = Path("client/src/ecs/data/predatorSpecies.ts")
    species_data = parse_typescript_species(species_file)
    
    # 2. For each species, run full pipeline
    for species_name, spec in species_data.items():
        print(f"Generating {species_name}...")
        
        # 3. Text-to-3D
        text3d_task = await text3d_service.submit_task(
            species=species_name,
            prompt=spec['meshyPrompt'],
            callback_url=f"{webhook_url}/text3d/{species_name}"
        )
        
        # 4. Wait for webhook, then rigging
        # 5. Wait for webhook, then animation
        # 6. Write manifest to shared/backend/asset_pipeline/manifests/{species_name}.json
        
    print("All species generated!")

if __name__ == "__main__":
    asyncio.run(main())
