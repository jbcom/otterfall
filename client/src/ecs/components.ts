import { Vector3 } from 'three';

// Core components for all entities
export interface Transform {
  position: Vector3;
  rotation: Vector3;
  scale: Vector3;
}

export interface Physical {
  mass: number;
  velocity: Vector3;
  acceleration: Vector3;
  drag: number;
}

export interface Health {
  current: number;
  max: number;
  regeneration: number;
}

// AI and behavior components
export interface AIControl {
  state: 'idle' | 'wander' | 'chase' | 'flee' | 'attack';
  target?: string; // Entity ID
  detectionRange: number;
  seekWeight: number;
  fleeWeight: number;
}

export interface Species {
  id: string;
  type: 'predator' | 'prey';
  displayName: string;
  maxSpeed: number;
  turnRate: number;
  size: number;
}

// Visual components
export interface Visual {
  modelPath: string;
  animations: string[];
  currentAnimation?: string;
  color?: string;
}

// Interaction components
export interface Interactable {
  type: 'pickup' | 'talk' | 'examine';
  prompt: string;
  onInteract: () => void;
}

export interface Inventory {
  items: string[];
  maxItems: number;
}
