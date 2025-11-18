/**
 * Biome Component - defines environmental properties of world chunks
 * NOT hardcoded meshes - this drives procedural rendering
 */

export type BiomeType = 
  | 'marsh'      // River otters, mink - waterlogged, reeds, cattails
  | 'forest'     // Fox, badger, raccoon - dense trees, undergrowth
  | 'desert'     // Meerkat, honey badger - sand, cacti, sparse vegetation
  | 'tundra'     // Arctic fox (variant) - snow, ice, moss
  | 'savanna'    // Mongoose, pangolin - grasslands, scattered trees
  | 'mountain'   // Red panda - rocky terrain, bamboo, steep slopes
  | 'scrubland'; // Wombat, Tasmanian devil - dry brush, burrows

export interface BiomeComponent {
  type: BiomeType;
  
  // Environmental properties
  temperature: number;      // -40 to 50°C
  moisture: number;         // 0.0 to 1.0 (dry to wet)
  terrainRoughness: number; // 0.0 to 1.0 (flat to mountainous)
  elevation: number;        // meters above sea level
  
  // Gameplay modifiers
  staminaDrainMod: number;  // 1.0 = normal, 1.5 = desert drains 50% faster
  movementSpeedMod: number; // 0.7 = snow slows you, 1.2 = downhill boost
  visibility: number;       // 0.5 = foggy/dense forest, 1.0 = clear
  stealthBonus: number;     // Forest gives +0.3 stealth, open savanna -0.2
  
  // Spawning rules
  preySpawnRate: number;       // 0.0 to 1.0
  stockSpawnRate: number;      // Resources like berries, fish
  predatorPatrolChance: number; // Hostile NPCs
  
  // Resource spawning (BiomeResourceComponent types)
  resources: string[];      // ['cattails', 'water_lily', 'reeds', 'berries']
  
  // Procedural rendering hints (not hardcoded)
  groundCover: string[];    // ['reeds', 'cattails', 'moss', 'mud']
  plantTypes: string[];     // ['willow', 'cypress'] - decorative, not gatherable
  colorPalette: {           // SDF shader reads this
    primary: string;        // Dominant ground color
    secondary: string;      // Accent color
    foliage: string;        // Plant tint
  };
}

// Biome archetypes - starting templates for world generation
export const BIOME_ARCHETYPES: Record<BiomeType, Omit<BiomeComponent, 'type'>> = {
  marsh: {
    temperature: 15,
    moisture: 0.9,
    terrainRoughness: 0.2,
    elevation: 5,
    staminaDrainMod: 1.1, // Wading through water is tiring
    movementSpeedMod: 0.85, // Mud slows you down
    visibility: 0.7, // Reeds block sight
    stealthBonus: 0.2, // Easy to hide
    preySpawnRate: 0.7,
    stockSpawnRate: 0.8, // Fish spawn rate
    predatorPatrolChance: 0.3,
    resources: ['cattails', 'water_lily', 'reeds', 'moss'],
    groundCover: ['mud', 'shallow_water'],
    plantTypes: ['willow', 'cypress'], // Decorative trees
    colorPalette: {
      primary: '#4a5f4d',
      secondary: '#6b8e6f',
      foliage: '#7fa87f'
    }
  },
  
  forest: {
    temperature: 12,
    moisture: 0.6,
    terrainRoughness: 0.4,
    elevation: 150,
    staminaDrainMod: 1.0,
    movementSpeedMod: 0.9, // Undergrowth slows
    visibility: 0.5, // Dense canopy
    stealthBonus: 0.3, // Best for ambushes
    preySpawnRate: 0.8,
    stockSpawnRate: 0.6,
    predatorPatrolChance: 0.5,
    resources: ['mushroom_common', 'mushroom_rare', 'berries', 'herbs', 'moss'],
    groundCover: ['leaf_litter', 'ferns', 'roots'],
    plantTypes: ['oak', 'pine'], // Large trees
    colorPalette: {
      primary: '#3d4a2f',
      secondary: '#5a6b47',
      foliage: '#6b8257'
    }
  },
  
  desert: {
    temperature: 35,
    moisture: 0.1,
    terrainRoughness: 0.3,
    elevation: 300,
    staminaDrainMod: 1.5, // Heat exhaustion
    movementSpeedMod: 0.95, // Sand slows slightly
    visibility: 1.0, // Wide open spaces
    stealthBonus: -0.2, // Nowhere to hide
    preySpawnRate: 0.3,
    stockSpawnRate: 0.2,
    predatorPatrolChance: 0.4,
    resources: ['herbs'], // Sparse resources
    groundCover: ['sand', 'rock', 'dry_grass'],
    plantTypes: ['cactus', 'dead_tree'], // Decorative
    colorPalette: {
      primary: '#d4a574',
      secondary: '#c9954a',
      foliage: '#8b7355'
    }
  },
  
  tundra: {
    temperature: -15,
    moisture: 0.3,
    terrainRoughness: 0.2,
    elevation: 50,
    staminaDrainMod: 1.3, // Cold drains energy
    movementSpeedMod: 0.7, // Snow is slow
    visibility: 0.9,
    stealthBonus: 0.1, // White on white blends
    preySpawnRate: 0.4,
    stockSpawnRate: 0.3,
    predatorPatrolChance: 0.3,
    resources: ['moss', 'herbs'], // Minimal vegetation
    groundCover: ['snow', 'ice', 'permafrost'],
    plantTypes: ['dwarf_shrub'], // Tiny plants
    colorPalette: {
      primary: '#e8f4f8',
      secondary: '#c9dfe8',
      foliage: '#a8b8c0'
    }
  },
  
  savanna: {
    temperature: 28,
    moisture: 0.4,
    terrainRoughness: 0.1,
    elevation: 200,
    staminaDrainMod: 1.2,
    movementSpeedMod: 1.1, // Open grassland = fast
    visibility: 0.9,
    stealthBonus: -0.1, // Tall grass helps a bit
    preySpawnRate: 0.9, // Lots of prey
    stockSpawnRate: 0.5,
    predatorPatrolChance: 0.6, // Competitive hunting grounds
    resources: ['berries', 'herbs', 'flowers'],
    groundCover: ['tall_grass', 'dirt', 'rock'],
    plantTypes: ['acacia', 'baobab'], // Iconic trees
    colorPalette: {
      primary: '#d4b896',
      secondary: '#c9a876',
      foliage: '#9b8a5a'
    }
  },
  
  mountain: {
    temperature: 5,
    moisture: 0.5,
    terrainRoughness: 0.9,
    elevation: 2000,
    staminaDrainMod: 1.4, // Thin air
    movementSpeedMod: 0.8, // Climbing is slow
    visibility: 0.8,
    stealthBonus: 0.1, // Rocks provide cover
    preySpawnRate: 0.5,
    stockSpawnRate: 0.4,
    predatorPatrolChance: 0.4,
    resources: ['herbs', 'mushroom_rare', 'flowers'],
    groundCover: ['rock', 'scree', 'alpine_grass', 'snow_patch'],
    plantTypes: ['bamboo', 'rhododendron', 'conifer'],
    colorPalette: {
      primary: '#8a9299',
      secondary: '#6f7a82',
      foliage: '#5a6b57'
    }
  },
  
  scrubland: {
    temperature: 22,
    moisture: 0.3,
    terrainRoughness: 0.4,
    elevation: 100,
    staminaDrainMod: 1.1,
    movementSpeedMod: 0.9, // Thorny bushes slow
    visibility: 0.6,
    stealthBonus: 0.15,
    preySpawnRate: 0.6,
    stockSpawnRate: 0.5,
    predatorPatrolChance: 0.5,
    resources: ['berries', 'herbs', 'mushroom_common'],
    groundCover: ['dry_dirt', 'sparse_grass', 'rock'],
    plantTypes: ['eucalyptus', 'thorn_bush', 'dry_shrub'],
    colorPalette: {
      primary: '#b89968',
      secondary: '#a68a5a',
      foliage: '#8a7a4d'
    }
  }
};
