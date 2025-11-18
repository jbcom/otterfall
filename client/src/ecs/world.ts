import { World } from 'miniplex';
import type { Transform, Physical, Health, AIControl, Species, Visual, Interactable, Inventory } from './components';
import type { BiomeComponent } from './components/BiomeComponent';
import type { WeatherComponent } from './components/WeatherComponent';
import type { TimeOfDayComponent } from './components/TimeOfDayComponent';
import type { MovementComponent } from './components/MovementComponent';
import type { CombatComponent } from './components/CombatComponent';
import type { AnimationComponent } from './components/AnimationComponent';

// Define the Entity type with all available components
export type Entity = Partial<{
  id: string;
  transform: Transform;
  physical: Physical;
  health: Health;
  aiControl: AIControl;
  species: Species;
  visual: Visual;
  interactable: Interactable;
  inventory: Inventory;
  biome: BiomeComponent;
  weather: WeatherComponent;
  timeOfDay: TimeOfDayComponent;
  movement: MovementComponent;
  combat: CombatComponent;
  animation: AnimationComponent;
}>;

// Create and export the main world instance
export const world = new World<Entity>();

// Entity queries can be added here as needed
// Example: export const physicalEntities = world.with('transform', 'physical');
export const queries = {};

// Type guard helpers
export const hasPhysics = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'physical'>> => 
  !!e.transform && !!e.physical;

export const hasAI = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'species' | 'aiControl'>> =>
  !!e.transform && !!e.species && !!e.aiControl;

export const isInteractable = (e: Entity): e is Entity & Required<Pick<Entity, 'transform' | 'interactable'>> =>
  !!e.transform && !!e.interactable;
