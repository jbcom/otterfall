export const DAGGERFALL_DUNGEON_TYPES = {
  BORDER: 'border',
  NORMAL: 'normal',
  WET: 'wet',
  QUEST: 'quest',
  MAUSOLEUM: 'mausoleum',
  START: 'start',
} as const;

export type DungeonBlockType = typeof DAGGERFALL_DUNGEON_TYPES[keyof typeof DAGGERFALL_DUNGEON_TYPES];

export interface DungeonBlock {
  type: DungeonBlockType;
  width: number;
  height: number;
  depth: number;
  connections: {
    north: boolean;
    south: boolean;
    east: boolean;
    west: boolean;
  };
}

export const OTTER_DUNGEON_THEMES = {
  RIVER_CLAN_SANCTUARY: {
    name: 'River Clan Sanctuary',
    blockTypes: ['normal', 'wet'],
    enemyFactions: ['marsh_raiders'],
    lootTable: ['shell_armor', 'fishing_rod', 'river_pearl'],
  },
  MARSH_RAIDER_HIDEOUT: {
    name: 'Marsh Raider Hideout',
    blockTypes: ['normal', 'mausoleum'],
    enemyFactions: ['marsh_raiders'],
    lootTable: ['stolen_goods', 'crude_weapons', 'marsh_herbs'],
  },
  FLOODED_CAVERNS: {
    name: 'Flooded Caverns',
    blockTypes: ['wet', 'normal'],
    enemyFactions: ['hostile_otters', 'marsh_creatures'],
    lootTable: ['diving_gear', 'water_crystals', 'ancient_shells'],
  },
  ELDER_COUNCIL_VAULT: {
    name: 'Elder Council Vault',
    blockTypes: ['quest', 'mausoleum'],
    enemyFactions: ['guardians'],
    lootTable: ['elder_artifacts', 'ancient_scrolls', 'ceremonial_items'],
  },
} as const;

export const DUNGEON_GENERATION_CONFIG = {
  MIN_BLOCKS: 5,
  MAX_BLOCKS: 15,
  BLOCK_SIZE: 20,
  CORRIDOR_WIDTH: 3,
  ROOM_MIN_SIZE: 8,
  ROOM_MAX_SIZE: 16,
};
