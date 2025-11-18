import { world } from '../world';
import { BIOME_RESOURCES_DATA, BiomeResourceType } from '../data/biomeResources';
import type { Entity } from '../world';

export interface CreateBiomeResourceOptions {
  type: BiomeResourceType;
  position: [number, number, number];
}

export function createBiomeResource(options: CreateBiomeResourceOptions): Entity {
  const resourceDef = BIOME_RESOURCES_DATA[options.type];

  const entity: Entity = {
    id: crypto.randomUUID(),
    type: 'resource',
    
    biomeResource: {
      type: options.type,
      name: resourceDef.name,
      visualModel: resourceDef.visualModel,
      biomes: resourceDef.biomes,
      gatherSkillRequired: resourceDef.gatherSkillRequired,
      gatherTime: resourceDef.gatherTime,
      minQuantity: resourceDef.minQuantity,
      maxQuantity: resourceDef.maxQuantity,
      respawnTime: resourceDef.respawnTime,
      dropItems: resourceDef.dropItems,
      currentQuantity: Math.floor(
        resourceDef.minQuantity + 
        Math.random() * (resourceDef.maxQuantity - resourceDef.minQuantity)
      ),
      isRespawning: false,
      respawnTimer: 0,
      harvesters: []
    },
    
    movement: {
      position: [...options.position],
      velocity: [0, 0, 0],
      rotation: [0, 0, 0, 1],
      walkSpeed: 0,
      runSpeed: 0,
      swimSpeed: 0,
      climbSpeed: 0,
      jumpHeight: 0,
      mass: 1,
      isGrounded: true,
      currentLocomotion: 'idle'
    }
  };

  world.add(entity);
  
  console.log(`[Entity] Created ${resourceDef.name} resource at`, options.position);
  
  return entity;
}
