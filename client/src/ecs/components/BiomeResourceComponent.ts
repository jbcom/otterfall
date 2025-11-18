/**
 * BiomeResource Component - gatherable plants/fungi spawned by biomes
 * NOT creatures - these are environmental resources
 */

export type ResourceType =
  // Plants
  | 'berries'          // Food, common
  | 'herbs'            // Crafting material
  | 'cattails'         // Marsh-specific, food + crafting
  | 'wildflowers'      // Decorative, minor crafting
  | 'bamboo'           // Sturdy material
  
  // Fungi
  | 'mushrooms'        // Food
  
  // Other
  | 'moss'             // Crafting material
  | 'cacti'            // Desert plant
  | 'rocks';           // Mining resource

export interface BiomeResourceComponent {
  type: ResourceType;
  name: string;              // Display name
  
  // Spawning/biome info
  biomes: string[];          // Which biomes this spawns in
  visualModel: string;       // Model identifier (procedural or GLB)
  
  // Gathering mechanics
  gatherSkillRequired: number;  // Skill level required (0-100)
  gatherTime: number;           // Seconds to gather
  minQuantity: number;          // Min drops per gather
  maxQuantity: number;          // Max drops per gather
  respawnTime: number;          // Minutes until respawn
  
  // Current state (runtime)
  currentQuantity: number;      // How much is left
  isRespawning: boolean;
  respawnTimer: number;
  
  // Drops when gathered
  dropItems: Array<{
    item: string;
    quantity: number;
    chance: number;
  }>;
  
  // Who's currently harvesting
  harvesters: string[];      // Entity IDs
}

// NOTE: Actual resource definitions are in client/src/ecs/data/biomeResources.ts (BIOME_RESOURCES_DATA)
