/**
 * Animation Component - manages Meshy animation library playback
 * References the 600+ animations from Meshy API
 */

export interface AnimationComponent {
  // Current animation state
  currentAnimation: number | null; // Meshy animation library ID
  animationTime: number;            // Current playback time
  animationSpeed: number;           // Playback speed multiplier
  
  // Blending
  previousAnimation: number | null;
  blendProgress: number;            // 0.0 to 1.0 for smooth transitions
  blendDuration: number;            // How long transitions take (seconds)
  
  // Animation sets by state (mapped from Meshy library)
  animations: {
    idle: number[];           // Random idle variations
    walk: number;
    run: number;
    swim: number;
    jump: number;
    fall: number;
    attack: number[];         // Different attack animations
    hit: number;              // Taking damage
    death: number;
    eat: number;
    drink: number;
    sleep: number;
  };
  
  // State
  isLooping: boolean;
  isPaused: boolean;
}

// Default animation mapping from Meshy library
// Based on https://docs.meshy.ai/en/api/animation-library
export const DEFAULT_ANIMATION_MAP = {
  idle: [0, 11, 12], // Idle, Idle_02, Idle_03
  walk: 1,           // Walking_Woman (works for all bipeds)
  run: 14,           // Run_02
  swim: 1,           // Use walk animation but slower
  jump: 13,          // Jump_Run
  fall: 13,          // Jump_Run (reuse)
  attack: [4],       // Attack
  hit: 7,            // BeHit_FlyUp
  death: 8,          // Dead
  eat: 31,           // Catching_Breath (repurpose)
  drink: 31,         // Catching_Breath (repurpose)
  sleep: 38          // Dozing_Elderly
};

// Species-specific animation overrides
export const SPECIES_ANIMATION_OVERRIDES: Record<string, Partial<typeof DEFAULT_ANIMATION_MAP>> = {
  otter: {
    swim: 30,        // Casual_Walk (modified for swimming)
    eat: 31          // Catching_Breath
  },
  
  pangolin: {
    attack: [4, 17], // Attack + Skill_01 (rolling attack)
    idle: [12]       // More defensive idle
  },
  
  mongoose: {
    attack: [4, 18], // Attack + Skill_02 (quick strikes)
    run: 15          // Run_03 (faster)
  },
  
  meerkat: {
    idle: [2],       // Alert (lookout pose)
    walk: 30         // Casual_Walk
  },
  
  wolf: {
    run: 16,         // RunFast
    attack: [4, 9]   // Attack + ForwardLeft_Run_Fight
  }
};

// Animation transition rules
export interface AnimationTransition {
  from: string;
  to: string;
  blendDuration: number;
  canInterrupt: boolean;
}

export const ANIMATION_TRANSITIONS: AnimationTransition[] = [
  // Natural transitions (smooth)
  { from: 'idle', to: 'walk', blendDuration: 0.2, canInterrupt: true },
  { from: 'walk', to: 'run', blendDuration: 0.15, canInterrupt: true },
  { from: 'run', to: 'walk', blendDuration: 0.2, canInterrupt: true },
  { from: 'walk', to: 'idle', blendDuration: 0.3, canInterrupt: true },
  
  // Combat transitions (fast)
  { from: 'idle', to: 'attack', blendDuration: 0.1, canInterrupt: false },
  { from: 'walk', to: 'attack', blendDuration: 0.1, canInterrupt: false },
  { from: 'attack', to: 'idle', blendDuration: 0.2, canInterrupt: true },
  
  // Damage (instant)
  { from: 'any', to: 'hit', blendDuration: 0.05, canInterrupt: true },
  { from: 'any', to: 'death', blendDuration: 0.1, canInterrupt: false },
  
  // Environmental
  { from: 'walk', to: 'swim', blendDuration: 0.3, canInterrupt: true },
  { from: 'swim', to: 'walk', blendDuration: 0.3, canInterrupt: true }
];
