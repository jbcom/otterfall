
/**
 * Integration layer between Meshy asset generation and ECS world
 * Converts ECS species definitions → Meshy API calls → ECS-ready assets
 */

import type { PredatorSpecies, PreySpecies } from '../../client/src/ecs/data/predatorSpecies';
import type { AnimationComponent } from '../../client/src/ecs/components/AnimationComponent';

export interface MeshyAssetManifest {
  species: string;
  text3d_task_id: string;
  rigging_task_id: string;
  animation_task_ids: Record<string, string>; // 'walk' -> task_id
  retexture_task_id?: string;
  glb_paths: {
    base: string;      // public/models/{species}/base.glb
    rigged: string;    // public/models/{species}/rigged.glb
    animated: string;  // public/models/{species}/animated.glb
    final: string;     // public/models/{species}/final.glb
  };
  animations: AnimationMapping;
}

export interface AnimationMapping {
  idle: number[];
  walk: number;
  run: number;
  attack: number[];
  // ... maps ECS AnimationComponent states to Meshy animation IDs
}

export class MeshyECSBridge {
  /**
   * Generate all assets for a species from ECS definition
   */
  async generateSpeciesAssets(
    species: PredatorSpecies | PreySpecies,
    webhookBaseUrl: string
  ): Promise<MeshyAssetManifest> {
    // 1. Read species.meshyPrompt from ECS data
    const prompt = species.meshyPrompt;
    
    // 2. Submit to Meshy pipeline (uses your existing services)
    // 3. Wait for webhooks
    // 4. Return manifest linking GLB paths to ECS entity IDs
    
    throw new Error('Implementation needed');
  }

  /**
   * Load generated assets into ECS world as renderable entities
   */
  async hydrateECSWithAssets(
    manifest: MeshyAssetManifest,
    world: any // Miniplex World
  ): Promise<void> {
    // 1. Read GLB from manifest.glb_paths.final
    // 2. Create ECS entity with:
    //    - SpeciesComponent (from manifest.species)
    //    - AnimationComponent (from manifest.animations)
    //    - MeshComponent (GLB reference for R3F)
    // 3. Store in world
    
    throw new Error('Implementation needed');
  }

  /**
   * Map species personality to Meshy animation selections
   */
  selectAnimationsForSpecies(
    species: PredatorSpecies | PreySpecies
  ): AnimationMapping {
    // Example: aggressive species get more attack animations
    // timid species get flee animations
    
    const baseMapping: AnimationMapping = {
      idle: [0, 11, 12],
      walk: 1,
      run: 14,
      attack: [4],
    };

    if (species.personality === 'aggressive') {
      return {
        ...baseMapping,
        attack: [4, 17, 18], // Multiple attack variants
      };
    }

    if (species.personality === 'timid') {
      return {
        ...baseMapping,
        idle: [2], // Alert idle (meerkat lookout pose)
      };
    }

    return baseMapping;
  }
}
