/**
 * Movement Component - physics and locomotion for all entities
 * Handles walking, running, swimming, climbing
 */

export type LocomotionMode = 
  | 'walk'
  | 'run'
  | 'swim'
  | 'climb'
  | 'jump'
  | 'fall';

export interface MovementComponent {
  // Position and velocity
  position: [number, number, number];
  velocity: [number, number, number];
  rotation: [number, number, number, number]; // Quaternion (x, y, z, w)
  
  // Movement stats
  walkSpeed: number;        // Base speed (m/s)
  runSpeed: number;         // Sprint speed (m/s)
  swimSpeed: number;        // In-water speed (m/s)
  climbSpeed: number;       // Climbing speed (m/s)
  jumpHeight: number;       // Maximum jump height (meters)
  
  // Current state
  currentMode: LocomotionMode;
  isGrounded: boolean;
  isInWater: boolean;
  canClimb: boolean;        // Species-specific ability
  waterDepth: number;       // How deep in water (0 = surface, 1 = fully submerged)
  
  // Modifiers (from biome, weather, equipment)
  speedMultiplier: number;  // Final speed = baseSpeed * speedMultiplier
  
  // Physics
  mass: number;             // Affects knockback
  drag: number;             // Air/water resistance (0.0 to 1.0)
  gravity: number;          // Downward acceleration
  
  // Navigation
  targetPosition: [number, number, number] | null;
  pathToTarget: Array<[number, number, number]>; // A* pathfinding result
  avoidanceRadius: number;  // Personal space
}

// Movement presets by size class
export const MOVEMENT_PRESETS = {
  tiny: {
    walkSpeed: 2.0,
    runSpeed: 5.0,
    swimSpeed: 1.5,
    climbSpeed: 1.0,
    jumpHeight: 0.5,
    mass: 0.5,
    drag: 0.3,
    gravity: -9.8,
    avoidanceRadius: 0.3
  },
  
  small: {
    walkSpeed: 3.0,
    runSpeed: 7.0,
    swimSpeed: 2.5,
    climbSpeed: 1.5,
    jumpHeight: 1.0,
    mass: 5,
    drag: 0.2,
    gravity: -9.8,
    avoidanceRadius: 0.5
  },
  
  medium: {
    walkSpeed: 3.5,
    runSpeed: 8.0,
    swimSpeed: 3.0,
    climbSpeed: 1.2,
    jumpHeight: 1.2,
    mass: 20,
    drag: 0.15,
    gravity: -9.8,
    avoidanceRadius: 0.7
  },
  
  large: {
    walkSpeed: 4.0,
    runSpeed: 10.0,
    swimSpeed: 3.5,
    climbSpeed: 0.8,
    jumpHeight: 1.5,
    mass: 50,
    drag: 0.1,
    gravity: -9.8,
    avoidanceRadius: 1.0
  }
};
