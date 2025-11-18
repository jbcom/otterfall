/**
 * AI Component - behavior logic for prey and NPC predators
 * Player-controlled predators don't have this component
 */

export type AIState = 
  | 'idle'          // Standing still, looking around
  | 'wander'        // Random movement
  | 'flee'          // Running from predator
  | 'hunt'          // Chasing prey
  | 'attack'        // In combat range
  | 'eat'           // Consuming kill
  | 'sleep'         // Resting (time-based)
  | 'drink'         // At water source
  | 'alert';        // Detected threat, deciding action

export type AIPersonality =
  | 'timid'         // Flees easily, wide detection radius
  | 'cautious'      // Balanced flee/fight
  | 'aggressive'    // Prefers fighting
  | 'fearless'      // Never flees (honey badger)
  | 'pack'          // Coordinates with others
  | 'territorial';  // Defends area

export interface AIComponent {
  currentState: AIState;
  personality: AIPersonality;
  
  // Detection
  detectionRadius: number;    // How far they can sense threats/prey
  fieldOfView: number;        // Degrees (180 = can't see behind)
  hearingRadius: number;      // Detect sounds (footsteps, combat)
  
  // Decision making
  fleeThreshold: number;      // Health % when they flee (0.3 = 30% HP)
  aggressionLevel: number;    // 0.0 to 1.0 (1.0 = always attacks)
  curiosity: number;          // 0.0 to 1.0 (investigates sounds/movement)
  
  // State tracking
  target: string | null;      // Entity ID of current target
  homePosition: [number, number, number] | null; // Return here when idle
  patrolPoints: Array<[number, number, number]>; // Patrol route
  currentPatrolIndex: number;
  
  // Timers
  lastStateChange: number;    // Timestamp
  stateDuration: number;      // How long to stay in this state
  nextDecisionTime: number;   // When to re-evaluate
  
  // Pack behavior (for wolves, meerkats)
  packId: string | null;      // Which pack they belong to
  packRole: 'leader' | 'member' | 'scout' | 'solo';
  
  // Memory (simple, not full spatial memory)
  lastThreatPosition: [number, number, number] | null;
  lastThreatTime: number;
  safeZones: Array<[number, number, number]>; // Known safe spots
}

// AI presets by personality type
export const AI_PERSONALITY_PRESETS: Record<AIPersonality, Partial<AIComponent>> = {
  timid: {
    detectionRadius: 30,
    fieldOfView: 270, // Wide vision
    hearingRadius: 25,
    fleeThreshold: 0.9, // Flees at 90% health
    aggressionLevel: 0.1,
    curiosity: 0.2
  },
  
  cautious: {
    detectionRadius: 20,
    fieldOfView: 180,
    hearingRadius: 15,
    fleeThreshold: 0.5, // Flees at 50% health
    aggressionLevel: 0.4,
    curiosity: 0.5
  },
  
  aggressive: {
    detectionRadius: 25,
    fieldOfView: 200,
    hearingRadius: 20,
    fleeThreshold: 0.2, // Only flees when near death
    aggressionLevel: 0.8,
    curiosity: 0.7
  },
  
  fearless: {
    detectionRadius: 20,
    fieldOfView: 180,
    hearingRadius: 15,
    fleeThreshold: 0.0, // Never flees
    aggressionLevel: 1.0,
    curiosity: 0.3
  },
  
  pack: {
    detectionRadius: 22,
    fieldOfView: 200,
    hearingRadius: 30, // Hears packmates
    fleeThreshold: 0.3,
    aggressionLevel: 0.7,
    curiosity: 0.6
  },
  
  territorial: {
    detectionRadius: 25,
    fieldOfView: 220,
    hearingRadius: 20,
    fleeThreshold: 0.4,
    aggressionLevel: 0.9, // Very aggressive in territory
    curiosity: 0.4
  }
};

// AI behavior tree node types (for complex decision making)
export type BehaviorTreeNode =
  | { type: 'sequence'; children: BehaviorTreeNode[] }
  | { type: 'selector'; children: BehaviorTreeNode[] }
  | { type: 'condition'; check: string } // 'isHealthLow', 'seesEnemy', etc.
  | { type: 'action'; name: string };    // 'flee', 'attack', 'wander'

// Example behavior tree for prey (rabbit)
export const PREY_BEHAVIOR_TREE: BehaviorTreeNode = {
  type: 'selector',
  children: [
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'detectsPredator' },
        { type: 'action', name: 'flee' }
      ]
    },
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'isHungry' },
        { type: 'action', name: 'forage' }
      ]
    },
    { type: 'action', name: 'wander' }
  ]
};

// Example behavior tree for predator (wolf)
export const PREDATOR_BEHAVIOR_TREE: BehaviorTreeNode = {
  type: 'selector',
  children: [
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'isHealthLow' },
        { type: 'action', name: 'flee' }
      ]
    },
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'seesPrey' },
        { type: 'condition', check: 'inHuntingRange' },
        { type: 'action', name: 'hunt' }
      ]
    },
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'hasKill' },
        { type: 'action', name: 'eat' }
      ]
    },
    {
      type: 'sequence',
      children: [
        { type: 'condition', check: 'hasPatrolRoute' },
        { type: 'action', name: 'patrol' }
      ]
    },
    { type: 'action', name: 'idle' }
  ]
};
