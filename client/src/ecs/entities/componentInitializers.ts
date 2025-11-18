/**
 * Component initializers with sensible defaults
 * Factories call these to hydrate complete component objects
 */

import type { CombatComponent, Attack } from '../components/CombatComponent';
import type { EquipmentComponent } from '../components/EquipmentComponent';
import type { AIComponent } from '../components/AIComponent';
import type { AnimationComponent } from '../components/AnimationComponent';
import type { MovementComponent } from '../components/MovementComponent';

export function initializeCombat(options: {
  health: number;
  maxHealth: number;
  stamina?: number;
  maxStamina?: number;
  staminaRegen?: number;
  attacks: Attack[];
}): CombatComponent {
  return {
    health: options.health,
    maxHealth: options.maxHealth,
    stamina: options.stamina ?? 100,
    maxStamina: options.maxStamina ?? 100,
    staminaRegen: options.staminaRegen ?? 5,
    attacks: options.attacks,
    
    // Defense defaults
    armor: 0,
    dodgeChance: 0.05,
    
    // Combat state
    isInCombat: false,
    lastAttackTime: 0,
    currentTarget: null,
    
    // Equipment bonuses (updated by equipment system)
    damageBonus: 1.0,
    armorBonus: 0,
    staminaCostReduction: 0
  };
}

export function initializeEquipment(): EquipmentComponent {
  return {
    equipped: {},
    
    // Cached totals
    totalHealthBonus: 0,
    totalStaminaBonus: 0,
    totalDamageBonus: 1.0,
    totalArmorBonus: 0,
    totalSpeedBonus: 1.0,
    totalStaminaCostReduction: 0
  };
}

export function initializeAI(options: {
  personality: string;
  aggressionLevel: number;
  homePosition: [number, number, number];
  fleeThreshold?: number;
}): AIComponent {
  // Map species personality to AI personality
  const normalizedPersonality = normalizePersonality(options.personality);
  
  // Defaults based on personality
  const defaults = getAIDefaults(normalizedPersonality);
  
  return {
    currentState: 'idle',
    personality: normalizedPersonality,
    
    // Detection
    detectionRadius: defaults.detectionRadius,
    fieldOfView: defaults.fieldOfView,
    hearingRadius: defaults.hearingRadius,
    
    // Decision making
    fleeThreshold: options.fleeThreshold ?? defaults.fleeThreshold,
    aggressionLevel: options.aggressionLevel,
    curiosity: defaults.curiosity,
    
    // State tracking
    target: null,
    homePosition: [...options.homePosition], // Deep copy to prevent shared references
    patrolPoints: [],
    currentPatrolIndex: 0,
    
    // Timers
    lastStateChange: 0,
    stateDuration: 5,
    nextDecisionTime: 0,
    
    // Pack behavior
    packId: null,
    packRole: 'solo',
    
    // Memory
    lastThreatPosition: null,
    lastThreatTime: 0,
    safeZones: []
  };
}

export function initializeAnimation(): AnimationComponent {
  return {
    currentAnimation: 0, // Idle animation
    animationTime: 0,
    animationSpeed: 1.0,
    previousAnimation: null,
    blendProgress: 0,
    blendDuration: 0.2,
    animations: {
      idle: [0, 11, 12],
      walk: 1,
      run: 14,
      swim: 1,
      jump: 13,
      fall: 13,
      attack: [4],
      hit: 7,
      death: 8,
      eat: 31,
      drink: 31,
      sleep: 38
    },
    isLooping: true,
    isPaused: false
  };
}

export function initializeMovement(options: {
  position: [number, number, number];
  walkSpeed: number;
  runSpeed: number;
  swimSpeed: number;
  climbSpeed: number;
  jumpHeight: number;
  mass: number;
  rotation?: [number, number, number, number];
  velocity?: [number, number, number];
}): MovementComponent {
  return {
    position: [...options.position], // Deep copy to prevent shared references
    velocity: options.velocity ? [...options.velocity] : [0, 0, 0], // Honor caller or default to stationary
    rotation: options.rotation ? [...options.rotation] : [0, 0, 0, 1], // Honor caller or default
    walkSpeed: options.walkSpeed,
    runSpeed: options.runSpeed,
    swimSpeed: options.swimSpeed,
    climbSpeed: options.climbSpeed,
    jumpHeight: options.jumpHeight,
    mass: options.mass,
    currentMode: 'walk',
    isGrounded: true,
    isInWater: false,
    canClimb: options.climbSpeed > 0,
    waterDepth: 0,
    speedMultiplier: 1.0,
    drag: 0.15,
    gravity: -9.8,
    targetPosition: null,
    pathToTarget: [],
    avoidanceRadius: 0.5
  };
}

// Map species personality strings to AIComponent personality enum
function normalizePersonality(speciesPersonality: string): 'timid' | 'cautious' | 'aggressive' | 'fearless' | 'pack' | 'territorial' {
  const mapping: Record<string, 'timid' | 'cautious' | 'aggressive' | 'fearless' | 'pack' | 'territorial'> = {
    'playful': 'cautious',
    'cunning': 'cautious',
    'aggressive': 'aggressive',
    'pack_hunter': 'pack',
    'curious': 'cautious',
    'defensive': 'territorial',
    'timid': 'timid',
    'docile': 'timid',
    'fearless': 'fearless'
  };
  
  return mapping[speciesPersonality] ?? 'cautious';
}

function getAIDefaults(personality: 'timid' | 'cautious' | 'aggressive' | 'fearless' | 'pack' | 'territorial') {
  const presets = {
    timid: {
      detectionRadius: 30,
      fieldOfView: 270,
      hearingRadius: 25,
      fleeThreshold: 0.9,
      curiosity: 0.2
    },
    cautious: {
      detectionRadius: 20,
      fieldOfView: 180,
      hearingRadius: 15,
      fleeThreshold: 0.5,
      curiosity: 0.5
    },
    aggressive: {
      detectionRadius: 25,
      fieldOfView: 180,
      hearingRadius: 20,
      fleeThreshold: 0.2,
      curiosity: 0.3
    },
    fearless: {
      detectionRadius: 20,
      fieldOfView: 160,
      hearingRadius: 15,
      fleeThreshold: 0.0,
      curiosity: 0.1
    },
    pack: {
      detectionRadius: 30,
      fieldOfView: 200,
      hearingRadius: 25,
      fleeThreshold: 0.3,
      curiosity: 0.4
    },
    territorial: {
      detectionRadius: 35,
      fieldOfView: 220,
      hearingRadius: 30,
      fleeThreshold: 0.4,
      curiosity: 0.6
    }
  };
  
  return presets[personality];
}
