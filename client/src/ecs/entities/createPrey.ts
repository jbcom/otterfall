import { world } from '../world';
import { PREY_SPECIES_DATA, PreySpecies } from '../data/preySpecies';
import type { Entity } from '../world';
import { initializeCombat, initializeEquipment, initializeAI, initializeAnimation, initializeMovement } from './componentInitializers';
import { normalizeAttack } from '../data/attackHelpers';

export interface CreatePreyOptions {
  species: PreySpecies;
  position: [number, number, number];
  level?: number;
}

export function createPrey(options: CreatePreyOptions): Entity {
  const speciesDef = PREY_SPECIES_DATA[options.species];
  const level = options.level ?? 1;
  
  // Normalize and scale attacks by level
  const scaledAttacks = speciesDef.attacks.map(atk => {
    const normalized = normalizeAttack(atk as any);
    return {
      ...normalized,
      damage: normalized.damage * (1 + (level - 1) * 0.1)
    };
  });
  
  // Create ECS entity with proper component initialization
  const entity: Entity = {
    id: crypto.randomUUID(),
    type: 'prey',
    
    species: {
      type: options.species,
      category: 'prey',
      meshyPrompt: speciesDef.meshyPrompt,
      meshyArtStyle: speciesDef.meshyArtStyle,
      size: speciesDef.size,
      primaryColor: speciesDef.primaryColor,
      markings: [...speciesDef.markings],
      nativeBiome: [...speciesDef.nativeBiome],
      dropItems: speciesDef.dropItems.map(item => ({ ...item }))
    },
    
    combat: initializeCombat({
      health: speciesDef.baseHealth,
      maxHealth: speciesDef.baseHealth,
      attacks: scaledAttacks
    }),
    
    equipment: initializeEquipment(),
    
    movement: initializeMovement({
      position: options.position,
      walkSpeed: speciesDef.walkSpeed,
      runSpeed: speciesDef.runSpeed,
      swimSpeed: speciesDef.swimSpeed,
      climbSpeed: speciesDef.climbSpeed,
      jumpHeight: speciesDef.jumpHeight,
      mass: speciesDef.mass
    }),
    
    ai: initializeAI({
      personality: speciesDef.personality,
      aggressionLevel: 0.1,
      homePosition: options.position,
      fleeThreshold: speciesDef.fleeThreshold
    }),
    
    animation: initializeAnimation()
  };

  // Add to ECS world
  world.add(entity);
  
  console.log(`[Entity] Created ${speciesDef.name} prey at`, options.position);
  
  return entity;
}
