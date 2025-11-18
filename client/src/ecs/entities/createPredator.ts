import { world } from '../world';
import { PREDATOR_SPECIES_DATA, PredatorSpecies } from '../data/predatorSpecies';
import type { Entity } from '../world';
import { initializeCombat, initializeEquipment, initializeAI, initializeAnimation, initializeMovement } from './componentInitializers';
import { normalizeAttack } from '../data/attackHelpers';

export interface CreatePredatorOptions {
  species: PredatorSpecies;
  position: [number, number, number];
  level?: number;
}

export function createPredator(options: CreatePredatorOptions): Entity {
  const speciesDef = PREDATOR_SPECIES_DATA[options.species];
  const level = options.level ?? 1;
  
  // Normalize and scale attacks by level
  const scaledAttacks = speciesDef.attacks.map(atk => {
    const normalized = normalizeAttack(atk as any);
    return {
      ...normalized,
      damage: normalized.damage * (1 + (level - 1) * 0.1) // 10% per level
    };
  });
  
  // Create ECS entity with proper component initialization
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
      markings: [...speciesDef.markings], // Convert readonly to mutable
      nativeBiome: [...speciesDef.nativeBiome],
      dropItems: speciesDef.dropItems.map(item => ({ ...item })) // Deep copy
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
      aggressionLevel: speciesDef.aggressionLevel,
      homePosition: options.position
    }),
    
    animation: initializeAnimation()
  };

  // Add to ECS world
  world.add(entity);
  
  console.log(`[Entity] Created ${speciesDef.name} predator at`, options.position);
  
  return entity;
}
