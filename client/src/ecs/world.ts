import { World } from 'miniplex';
import * as Components from './components';

// Define the Entity type using all available components
type Entity = Partial<{
  [K in keyof typeof Components]: (typeof Components)[K]
}>;

// Create and export the main world instance
export const world = new World<Entity>();

// Create entity queries for common use cases
export const queries = {
  // Physical entities that need movement updates
  physical: world.query(e => e.transform && e.physical),
  
  // AI-controlled creatures
  creatures: world.query(e => e.transform && e.species && e.aiControl),
  
  // Entities with health
  living: world.query(e => e.health),
  
  // Interactable objects/NPCs
  interactables: world.query(e => e.transform && e.interactable),
  
  // Visual entities that need rendering
  visible: world.query(e => e.transform && e.visual),
  
  // Specific creature types
  predators: world.query(e => e.species?.type === 'predator'),
  prey: world.query(e => e.species?.type === 'prey')
};

// Type guard helpers
export const hasPhysics = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'physical'>> => 
  !!e.transform && !!e.physical;

export const hasAI = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'species' | 'aiControl'>> =>
  !!e.transform && !!e.species && !!e.aiControl;

export const isInteractable = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'interactable'>> =>
  !!e.transform && !!e.interactable;
