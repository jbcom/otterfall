import { world } from '../world';
import { PREDATOR_SPECIES_DATA, PredatorSpecies } from '../data/predatorSpecies';
import type { Entity } from '../world';

export interface CreatePredatorOptions {
  species: PredatorSpecies;
  position: [number, number, number];
  level?: number;
}

export function createPredator(options: CreatePredatorOptions): Entity {
  const speciesDef = PREDATOR_SPECIES_DATA[options.species];
  const level = options.level ?? 1;
  
  // Create ECS entity
  const entity: Entity = {
    id: crypto.randomUUID(),
    type: 'predator',
    
    species: {
      type: options.species,
      category: 'predator',
      meshyPrompt: speciesDef.meshyPrompt,
      meshyArtStyle: speciesDef.meshyArtStyle,
      size: speciesDef.size,
      primaryColor: speciesDef.primaryColor,
      markings: speciesDef.markings,
      nativeBiome: speciesDef.nativeBiome,
      dropItems: speciesDef.dropItems
    },
    
    combat: {
      health: speciesDef.baseHealth,
      maxHealth: speciesDef.baseHealth,
      stamina: 100,
      maxStamina: 100,
      staminaRegen: 5,
      attacks: speciesDef.attacks.map((atk: any) => ({
        ...atk,
        damage: atk.damage * (1 + (level - 1) * 0.1) // 10% per level
      }))
    },
    
    equipment: {
      head: null,
      neck: null,
      body: null,
      legs: null,
      feet: null,
      leftPaw: null,
      rightPaw: null,
      tail: null
    },
    
    movement: {
      position: [...options.position],
      velocity: [0, 0, 0],
      rotation: [0, 0, 0, 1],
      walkSpeed: speciesDef.walkSpeed,
      runSpeed: speciesDef.runSpeed,
      swimSpeed: speciesDef.swimSpeed,
      climbSpeed: speciesDef.climbSpeed,
      jumpHeight: speciesDef.jumpHeight,
      mass: speciesDef.mass,
      isGrounded: true,
      currentLocomotion: 'idle'
    },
    
    ai: {
      currentState: 'idle',
      personality: speciesDef.personality,
      aggressionLevel: speciesDef.aggressionLevel,
      currentTarget: null,
      lastKnownTargetPosition: null,
      homePosition: [...options.position],
      memory: []
    },
    
    animation: {
      currentAnimation: 0,
      previousAnimation: null,
      blendWeight: 1.0,
      animationSpeed: 1.0,
      looping: true
    }
  };

  // Add to ECS world
  world.add(entity);
  
  console.log(`[Entity] Created ${speciesDef.name} predator at`, options.position);
  
  return entity;
}
