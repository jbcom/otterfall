import { World } from 'miniplex';
import type { BiomeComponent } from './components/BiomeComponent';
import type { WeatherComponent } from './components/WeatherComponent';
import type { TimeOfDayComponent } from './components/TimeOfDayComponent';
import type { SpeciesComponent } from './components/SpeciesComponent';
import type { CombatComponent } from './components/CombatComponent';
import type { EquipmentComponent } from './components/EquipmentComponent';
import type { BiomeResourceComponent } from './components/BiomeResourceComponent';
import type { AIComponent } from './components/AIComponent';
import type { MovementComponent } from './components/MovementComponent';
import type { AnimationComponent } from './components/AnimationComponent';

export interface Entity {
  id: string;
  type: 'predator' | 'prey' | 'resource' | 'world';
  
  // Optional components
  species?: SpeciesComponent;
  combat?: CombatComponent;
  equipment?: EquipmentComponent;
  movement?: MovementComponent;
  ai?: AIComponent;
  animation?: AnimationComponent;
  biomeResource?: BiomeResourceComponent;
  
  // World singleton components
  biome?: BiomeComponent;
  weather?: WeatherComponent;
  timeOfDay?: TimeOfDayComponent;
}

export const world = new World<Entity>();

console.log('[ECS] Miniplex world initialized');
