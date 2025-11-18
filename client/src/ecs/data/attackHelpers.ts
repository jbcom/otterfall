import type { Attack, AttackType } from '../components/CombatComponent';

/**
 * Normalize attack data - adds missing required fields with sensible defaults
 * STRICT MODE: Throws error on unknown attack types to catch data errors early
 */
export function normalizeAttack(attack: Partial<Attack> & { name: string; damage: number; staminaCost: number; cooldown: number; range: number }): Attack {
  // Infer attack type from name if not provided, with strict validation
  const inferredType: AttackType = attack.type || inferAttackType(attack.name);
  
  return {
    type: inferredType,
    damage: attack.damage,
    range: attack.range,
    staminaCost: attack.staminaCost,
    cooldown: attack.cooldown,
    knockback: attack.knockback ?? getDefaultKnockback(inferredType),
    stunDuration: attack.stunDuration ?? getDefaultStunDuration(inferredType),
    animationId: attack.animationId ?? getDefaultAnimationId(inferredType)
  };
}

/**
 * Infer attack type from name with STRICT validation
 * Throws error if attack name doesn't match known patterns
 */
function inferAttackType(name: string): AttackType {
  const nameLower = name.toLowerCase();
  
  // Explicit type mapping - ordered by specificity
  if (nameLower.includes('bite')) return 'bite';
  if (nameLower.includes('claw') || nameLower.includes('swipe') || nameLower.includes('scratch')) return 'claw_swipe';
  if (nameLower.includes('tail') || nameLower.includes('whip') || nameLower.includes('slap')) return 'tail_whip';
  if (nameLower.includes('head') || nameLower.includes('butt')) return 'headbutt';
  if (nameLower.includes('pounce') || nameLower.includes('lunge') || nameLower.includes('leap')) return 'pounce';
  if (nameLower.includes('roll') || nameLower.includes('crush')) return 'roll_crush';
  if (nameLower.includes('kick') || nameLower.includes('stomp')) return 'bite'; // Prey defense attacks
  if (nameLower.includes('antler') || nameLower.includes('horn') || nameLower.includes('gore')) return 'headbutt';
  if (nameLower.includes('charge') || nameLower.includes('ram')) return 'pounce';
  
  // STRICT: Throw error on unknown attack types to surface data issues
  throw new Error(`Unknown attack type for attack "${name}". Please add explicit type or update inferAttackType() mapping.`);
}

function getDefaultKnockback(type: AttackType): number {
  const knockbackMap: Record<AttackType, number> = {
    'bite': 1,
    'claw_swipe': 0.5,
    'tail_whip': 2,
    'headbutt': 3,
    'pounce': 2.5,
    'roll_crush': 4
  };
  return knockbackMap[type] ?? 1;
}

function getDefaultStunDuration(type: AttackType): number {
  const stunMap: Record<AttackType, number> = {
    'bite': 0,
    'claw_swipe': 0,
    'tail_whip': 0,
    'headbutt': 1.5,
    'pounce': 0.5,
    'roll_crush': 1.0
  };
  return stunMap[type] ?? 0;
}

function getDefaultAnimationId(type: AttackType): number {
  const animationMap: Record<AttackType, number> = {
    'bite': 4,        // Attack animation
    'claw_swipe': 4,
    'tail_whip': 17,  // Skill_01
    'headbutt': 17,
    'pounce': 18,     // Skill_02
    'roll_crush': 17
  };
  return animationMap[type] ?? 4;
}
