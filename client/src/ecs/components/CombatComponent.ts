/**
 * Combat Component - natural weapon attacks for mammals
 * NO swords or gripping - only bite, claw, tail attacks
 */

export type AttackType = 
  | 'bite'        // Close range, high damage
  | 'claw_swipe'  // Medium range, fast
  | 'tail_whip'   // Long range, knockback
  | 'headbutt'    // Close range, stun
  | 'pounce'      // Leap attack
  | 'roll_crush'; // Pangolin special

export interface Attack {
  type: AttackType;
  damage: number;         // Base damage
  range: number;          // Attack reach in meters
  staminaCost: number;    // Stamina consumed per attack
  cooldown: number;       // Seconds before can use again
  knockback: number;      // How far it pushes enemy back
  stunDuration: number;   // Seconds enemy is stunned (0 if none)
  
  // Animation reference (from Meshy library)
  animationId: number;    // Meshy animation library ID
}

export interface CombatComponent {
  // Natural attacks (every predator has these)
  attacks: Attack[];
  
  // Combat stats
  health: number;
  maxHealth: number;
  stamina: number;
  maxStamina: number;
  staminaRegen: number;   // Per second
  
  // Defense
  armor: number;          // Damage reduction (0 to 1, where 0.3 = 30% reduction)
  dodgeChance: number;    // 0.0 to 1.0
  
  // Current state
  isInCombat: boolean;
  lastAttackTime: number; // Timestamp
  currentTarget: string | null; // Entity ID
  
  // Enchanted equipment bonuses (applied from EquipmentComponent)
  damageBonus: number;    // Multiplier
  armorBonus: number;     // Additional armor
  staminaCostReduction: number; // 0.0 to 1.0
}

// Default attack sets by species archetype
export const ATTACK_PRESETS = {
  // Tank archetype (high damage, slow)
  tank: [
    {
      type: 'bite' as const,
      damage: 40,
      range: 1.5,
      staminaCost: 25,
      cooldown: 2.0,
      knockback: 2,
      stunDuration: 0.5,
      animationId: 4 // Attack animation from Meshy library
    },
    {
      type: 'headbutt' as const,
      damage: 30,
      range: 1.2,
      staminaCost: 30,
      cooldown: 3.0,
      knockback: 4,
      stunDuration: 1.5,
      animationId: 17 // Skill_01
    }
  ],
  
  // Agile archetype (fast, low damage)
  agile: [
    {
      type: 'claw_swipe' as const,
      damage: 20,
      range: 1.8,
      staminaCost: 15,
      cooldown: 1.0,
      knockback: 1,
      stunDuration: 0,
      animationId: 4 // Attack
    },
    {
      type: 'pounce' as const,
      damage: 35,
      range: 4.0,
      staminaCost: 40,
      cooldown: 4.0,
      knockback: 3,
      stunDuration: 0.5,
      animationId: 13 // Jump_Run
    }
  ],
  
  // Balanced archetype
  balanced: [
    {
      type: 'bite' as const,
      damage: 28,
      range: 1.5,
      staminaCost: 20,
      cooldown: 1.5,
      knockback: 1.5,
      stunDuration: 0,
      animationId: 4
    },
    {
      type: 'claw_swipe' as const,
      damage: 22,
      range: 1.8,
      staminaCost: 18,
      cooldown: 1.2,
      knockback: 1,
      stunDuration: 0,
      animationId: 4
    },
    {
      type: 'tail_whip' as const,
      damage: 25,
      range: 2.5,
      staminaCost: 25,
      cooldown: 2.5,
      knockback: 3,
      stunDuration: 0,
      animationId: 18 // Skill_02
    }
  ]
};

// Combat stats by species archetype
export const COMBAT_STAT_PRESETS = {
  tank: {
    maxHealth: 150,
    maxStamina: 80,
    staminaRegen: 8,
    armor: 0.3,
    dodgeChance: 0.1
  },
  
  agile: {
    maxHealth: 80,
    maxStamina: 120,
    staminaRegen: 15,
    armor: 0.05,
    dodgeChance: 0.35
  },
  
  balanced: {
    maxHealth: 100,
    maxStamina: 100,
    staminaRegen: 10,
    armor: 0.15,
    dodgeChance: 0.2
  }
};
