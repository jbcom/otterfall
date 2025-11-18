import { Vector3 } from 'three';
import { World } from 'miniplex';
import * as Components from './components';
import { getSpeciesById } from './species';

type Entity = Partial<{
  [K in keyof typeof Components]: (typeof Components)[K]
}>;

export const createCreature = (
  world: World<Entity>,
  speciesId: string,
  position: Vector3
) => {
  const species = getSpeciesById(speciesId);
  if (!species) throw new Error(`Invalid species ID: ${speciesId}`);

  return world.add({
    transform: {
      position: position.clone(),
      rotation: new Vector3(),
      scale: new Vector3(species.size, species.size, species.size)
    },
    physical: {
      mass: species.size * 10,
      velocity: new Vector3(),
      acceleration: new Vector3(),
      drag: 0.1
    },
    health: {
      current: 100,
      max: 100,
      regeneration: 1
    },
    aiControl: {
      state: 'idle',
      detectionRange: species.type === 'predator' ? 15 : 10,
      seekWeight: species.type === 'predator' ? 1 : 0.5,
      fleeWeight: species.type === 'predator' ? 0.2 : 1
    },
    species,
    visual: {
      modelPath: `models/creatures/${species.id}.glb`,
      animations: ['idle', 'walk', 'run'],
      currentAnimation: 'idle'
    }
  });
};

export const createItem = (
  world: World<Entity>,
  itemId: string,
  position: Vector3
) => {
  return world.add({
    transform: {
      position: position.clone(),
      rotation: new Vector3(),
      scale: new Vector3(1, 1, 1)
    },
    visual: {
      modelPath: `models/items/${itemId}.glb`,
      animations: []
    },
    interactable: {
      type: 'pickup',
      prompt: `Pick up ${itemId}`,
      onInteract: () => console.log(`Picked up ${itemId}`)
    }
  });
};

export const createNPC = (
  world: World<Entity>,
  npcId: string,
  position: Vector3
) => {
  return world.add({
    transform: {
      position: position.clone(),
      rotation: new Vector3(),
      scale: new Vector3(1, 1, 1)
    },
    visual: {
      modelPath: `models/npcs/${npcId}.glb`,
      animations: ['idle', 'talk'],
      currentAnimation: 'idle'
    },
    interactable: {
      type: 'talk',
      prompt: `Talk to ${npcId}`,
      onInteract: () => console.log(`Talking to ${npcId}`)
    },
    inventory: {
      items: [],
      maxItems: 10
    }
  });
};
