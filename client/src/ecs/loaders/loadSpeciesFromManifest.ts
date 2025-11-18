
import { world } from '../world';
import type { MeshyAssetManifest } from '../../../shared/backend/asset_pipeline/MeshyECSBridge';
import { createPredator } from '../entities/createPredator';

export async function loadAllSpeciesAssets() {
  // 1. Read all manifests from shared/backend/asset_pipeline/manifests/*.json
  const manifestFiles = await fetch('/api/manifests').then(r => r.json());
  
  // 2. For each manifest:
  for (const manifest of manifestFiles as MeshyAssetManifest[]) {
    // 3. Load GLB into Three.js
    const gltf = await loadGLTF(manifest.glb_paths.final);
    
    // 4. Create ECS entity
    const entity = createPredator(world, {
      species: manifest.species,
      position: [0, 0, 0],
      // GLB mesh attached by rendering system
    });
    
    // 5. Store GLB reference for R3F
    entity.mesh = { ref: gltf.scene };
    entity.animation.animations = manifest.animations;
  }
}
