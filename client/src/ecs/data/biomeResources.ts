/**
 * Biome resource data
 * Gatherables found in different biomes
 */

export const BIOME_RESOURCES_DATA = {
  cattails: {
    name: 'Cattails',
    visualModel: 'tall_reed',
    biomes: ['marsh'],
    gatherSkillRequired: 0,
    gatherTime: 2,
    minQuantity: 2,
    maxQuantity: 4,
    respawnTime: 300,
    dropItems: [
      { item: 'cattail_fluff', quantity: 2, chance: 1.0 },
      { item: 'cattail_root', quantity: 1, chance: 0.7 }
    ]
  },
  mushrooms: {
    name: 'Mushrooms',
    visualModel: 'mushroom_cluster',
    biomes: ['forest'],
    gatherSkillRequired: 0,
    gatherTime: 1.5,
    minQuantity: 1,
    maxQuantity: 3,
    respawnTime: 600,
    dropItems: [
      { item: 'edible_mushroom', quantity: 1, chance: 1.0 }
    ]
  },
  berries: {
    name: 'Berry Bush',
    visualModel: 'berry_bush',
    biomes: ['forest', 'scrubland'],
    gatherSkillRequired: 0,
    gatherTime: 2,
    minQuantity: 3,
    maxQuantity: 6,
    respawnTime: 400,
    dropItems: [
      { item: 'berries', quantity: 3, chance: 1.0 }
    ]
  },
  wildflowers: {
    name: 'Wildflowers',
    visualModel: 'flower_patch',
    biomes: ['scrubland', 'savanna'],
    gatherSkillRequired: 0,
    gatherTime: 1,
    minQuantity: 2,
    maxQuantity: 5,
    respawnTime: 200,
    dropItems: [
      { item: 'wildflower', quantity: 2, chance: 1.0 },
      { item: 'pollen', quantity: 1, chance: 0.5 }
    ]
  },
  cacti: {
    name: 'Cactus',
    visualModel: 'cactus',
    biomes: ['desert'],
    gatherSkillRequired: 1,
    gatherTime: 3,
    minQuantity: 1,
    maxQuantity: 2,
    respawnTime: 800,
    dropItems: [
      { item: 'cactus_fruit', quantity: 1, chance: 0.8 },
      { item: 'cactus_needle', quantity: 2, chance: 1.0 }
    ]
  },
  herbs: {
    name: 'Medicinal Herbs',
    visualModel: 'herb_plant',
    biomes: ['forest', 'jungle', 'marsh'],
    gatherSkillRequired: 1,
    gatherTime: 2.5,
    minQuantity: 1,
    maxQuantity: 2,
    respawnTime: 500,
    dropItems: [
      { item: 'healing_herb', quantity: 1, chance: 1.0 }
    ]
  },
  bamboo: {
    name: 'Bamboo',
    visualModel: 'bamboo_shoot',
    biomes: ['jungle', 'mountain'],
    gatherSkillRequired: 0,
    gatherTime: 2,
    minQuantity: 1,
    maxQuantity: 3,
    respawnTime: 300,
    dropItems: [
      { item: 'bamboo_shoot', quantity: 2, chance: 1.0 }
    ]
  },
  moss: {
    name: 'Moss Patch',
    visualModel: 'moss',
    biomes: ['tundra', 'mountain', 'forest'],
    gatherSkillRequired: 0,
    gatherTime: 1.5,
    minQuantity: 2,
    maxQuantity: 4,
    respawnTime: 250,
    dropItems: [
      { item: 'moss', quantity: 2, chance: 1.0 }
    ]
  },
  rocks: {
    name: 'Rock Pile',
    visualModel: 'rock_pile',
    biomes: ['mountain', 'desert', 'tundra'],
    gatherSkillRequired: 2,
    gatherTime: 4,
    minQuantity: 1,
    maxQuantity: 1,
    respawnTime: 1000,
    dropItems: [
      { item: 'stone', quantity: 3, chance: 1.0 },
      { item: 'flint', quantity: 1, chance: 0.4 }
    ]
  }
} as const;

export type BiomeResourceType = keyof typeof BIOME_RESOURCES_DATA;
