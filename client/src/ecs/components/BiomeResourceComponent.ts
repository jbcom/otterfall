/**
 * BiomeResource Component - gatherable plants/fungi spawned by biomes
 * NOT creatures - these are environmental resources
 */

export type ResourceType =
  // Plants
  | 'berries'          // Food, common
  | 'herbs'            // Crafting material
  | 'cattails'         // Marsh-specific, food + crafting
  | 'water_lily'       // Marsh decoration, minor food
  
  // Fungi
  | 'mushroom_common'  // Food
  | 'mushroom_rare'    // Crafting, medicinal
  
  // Other
  | 'reeds'            // Crafting material
  | 'moss'             // Crafting material
  | 'flowers';         // Decorative, minor crafting

export interface BiomeResourceComponent {
  type: ResourceType;
  
  // Visual (simple procedural geometry, no Meshy needed)
  renderType: 'cluster' | 'single' | 'patch';
  color: string;
  size: number; // 0.1 to 1.0 scale
  
  // Gameplay
  gatherable: boolean;    // Can player collect it?
  respawnTime: number;    // Minutes until it respawns
  
  // Drops when gathered
  dropItems: Array<{
    item: string;
    quantity: number;
    chance: number;
  }>;
  
  // Spawning rules
  spawnDensity: number;   // How many per chunk
  minGroupSize: number;   // Minimum cluster size
  maxGroupSize: number;   // Maximum cluster size
}

// Resource definitions by type
export const BIOME_RESOURCE_DEFINITIONS: Record<ResourceType, Omit<BiomeResourceComponent, 'type'>> = {
  berries: {
    renderType: 'cluster',
    color: '#8b4789',
    size: 0.3,
    gatherable: true,
    respawnTime: 5,
    dropItems: [
      { item: 'berry', quantity: 3, chance: 1.0 }
    ],
    spawnDensity: 0.6,
    minGroupSize: 1,
    maxGroupSize: 3
  },
  
  herbs: {
    renderType: 'patch',
    color: '#6b9b6f',
    size: 0.2,
    gatherable: true,
    respawnTime: 8,
    dropItems: [
      { item: 'herb', quantity: 2, chance: 1.0 }
    ],
    spawnDensity: 0.4,
    minGroupSize: 2,
    maxGroupSize: 5
  },
  
  cattails: {
    renderType: 'single',
    color: '#8b7355',
    size: 0.8,
    gatherable: true,
    respawnTime: 10,
    dropItems: [
      { item: 'cattail_fluff', quantity: 1, chance: 0.8 },
      { item: 'cattail_root', quantity: 1, chance: 0.5 }
    ],
    spawnDensity: 0.9, // Very common in marsh
    minGroupSize: 3,
    maxGroupSize: 12
  },
  
  water_lily: {
    renderType: 'single',
    color: '#ffffff',
    size: 0.4,
    gatherable: true,
    respawnTime: 12,
    dropItems: [
      { item: 'lily_petal', quantity: 1, chance: 0.6 }
    ],
    spawnDensity: 0.3,
    minGroupSize: 1,
    maxGroupSize: 4
  },
  
  mushroom_common: {
    renderType: 'cluster',
    color: '#c9a876',
    size: 0.15,
    gatherable: true,
    respawnTime: 6,
    dropItems: [
      { item: 'mushroom', quantity: 2, chance: 1.0 }
    ],
    spawnDensity: 0.5,
    minGroupSize: 2,
    maxGroupSize: 6
  },
  
  mushroom_rare: {
    renderType: 'single',
    color: '#9b4a9b',
    size: 0.2,
    gatherable: true,
    respawnTime: 20,
    dropItems: [
      { item: 'rare_mushroom', quantity: 1, chance: 1.0 }
    ],
    spawnDensity: 0.1,
    minGroupSize: 1,
    maxGroupSize: 2
  },
  
  reeds: {
    renderType: 'patch',
    color: '#7a8a5a',
    size: 0.6,
    gatherable: true,
    respawnTime: 7,
    dropItems: [
      { item: 'reed', quantity: 3, chance: 1.0 }
    ],
    spawnDensity: 0.8,
    minGroupSize: 5,
    maxGroupSize: 15
  },
  
  moss: {
    renderType: 'patch',
    color: '#4a6a4a',
    size: 0.1,
    gatherable: true,
    respawnTime: 15,
    dropItems: [
      { item: 'moss', quantity: 1, chance: 1.0 }
    ],
    spawnDensity: 0.7,
    minGroupSize: 1,
    maxGroupSize: 1
  },
  
  flowers: {
    renderType: 'cluster',
    color: '#ffaa44',
    size: 0.25,
    gatherable: true,
    respawnTime: 10,
    dropItems: [
      { item: 'flower', quantity: 1, chance: 0.7 }
    ],
    spawnDensity: 0.4,
    minGroupSize: 1,
    maxGroupSize: 5
  }
};
