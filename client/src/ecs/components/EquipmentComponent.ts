/**
 * Equipment Component - enchanted accessories that boost natural abilities
 * NO swords/shields - only items that attach to bones (collars, bracers, rings)
 */

export type EquipmentSlot = 
  | 'collar'      // Neck - health/regen bonuses
  | 'bracer_left' // Left wrist - claw attack bonus
  | 'bracer_right' // Right wrist - claw attack bonus
  | 'tail_ring'   // Tail - tail attack bonus, balance
  | 'anklet_left' // Left ankle - speed bonus
  | 'anklet_right' // Right ankle - speed bonus
  | 'earring_left' // Left ear - perception/stealth
  | 'earring_right'; // Right ear - perception/stealth

export interface EquipmentItem {
  id: string;
  name: string;
  slot: EquipmentSlot;
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  
  // Visual properties (for rendering)
  glowColor: string;      // Hex color for enchantment glow
  materialType: 'metal' | 'leather' | 'bone' | 'crystal' | 'wood';
  
  // Stat bonuses
  healthBonus: number;
  staminaBonus: number;
  damageBonus: number;    // Multiplier (1.2 = +20% damage)
  armorBonus: number;     // Flat armor addition
  speedBonus: number;     // Movement speed multiplier
  staminaCostReduction: number; // 0.0 to 1.0
  
  // Special effects
  specialEffect?: 'fire_aura' | 'ice_aura' | 'lightning_strike' | 'heal_on_kill' | 'thorns';
  
  // Meshy generation (for visual rendering as attachment)
  meshyPrompt?: string;   // Optional - some items can be simple geometry
  boneName: string;       // Which bone to attach to
}

export interface EquipmentComponent {
  equipped: Partial<Record<EquipmentSlot, EquipmentItem>>;
  
  // Cached total bonuses (recalculated when equipment changes)
  totalHealthBonus: number;
  totalStaminaBonus: number;
  totalDamageBonus: number;
  totalArmorBonus: number;
  totalSpeedBonus: number;
  totalStaminaCostReduction: number;
}

// Example equipment items
export const EXAMPLE_EQUIPMENT: EquipmentItem[] = [
  {
    id: 'iron_collar_of_vitality',
    name: 'Iron Collar of Vitality',
    slot: 'collar',
    rarity: 'uncommon',
    glowColor: '#44ff44',
    materialType: 'metal',
    healthBonus: 30,
    staminaBonus: 0,
    damageBonus: 1.0,
    armorBonus: 0.05,
    speedBonus: 1.0,
    staminaCostReduction: 0,
    boneName: 'neck'
  },
  
  {
    id: 'claw_bracers_of_power',
    name: 'Claw Bracers of Power',
    slot: 'bracer_left',
    rarity: 'rare',
    glowColor: '#ff4444',
    materialType: 'leather',
    healthBonus: 0,
    staminaBonus: 0,
    damageBonus: 1.3,
    armorBonus: 0,
    speedBonus: 1.0,
    staminaCostReduction: 0,
    specialEffect: 'fire_aura',
    boneName: 'left_hand'
  },
  
  {
    id: 'crystal_tail_ring',
    name: 'Crystal Tail Ring',
    slot: 'tail_ring',
    rarity: 'epic',
    glowColor: '#4444ff',
    materialType: 'crystal',
    healthBonus: 0,
    staminaBonus: 20,
    damageBonus: 1.15,
    armorBonus: 0,
    speedBonus: 1.0,
    staminaCostReduction: 0.2,
    boneName: 'tail_base'
  },
  
  {
    id: 'swiftness_anklets',
    name: 'Anklets of Swiftness',
    slot: 'anklet_left',
    rarity: 'uncommon',
    glowColor: '#ffff44',
    materialType: 'metal',
    healthBonus: 0,
    staminaBonus: 15,
    damageBonus: 1.0,
    armorBonus: 0,
    speedBonus: 1.25,
    staminaCostReduction: 0.1,
    boneName: 'left_foot'
  },
  
  {
    id: 'shadow_earring',
    name: 'Shadow Earring',
    slot: 'earring_left',
    rarity: 'rare',
    glowColor: '#9944ff',
    materialType: 'bone',
    healthBonus: 0,
    staminaBonus: 0,
    damageBonus: 1.0,
    armorBonus: 0,
    speedBonus: 1.0,
    staminaCostReduction: 0,
    // Note: Stealth bonus would be tracked in a separate StealthComponent
    boneName: 'left_ear'
  }
];
