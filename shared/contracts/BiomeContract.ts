/**
 * Biome Contract - Shared type definitions for biome system
 * 
 * CrewAI MUST implement this contract when building:
 * - Biome procedural generation
 * - Terrain rendering
 * - Environmental effects
 */

export type BiomeType = 
  | 'marsh'
  | 'forest'
  | 'desert'
  | 'tundra'
  | 'savanna'
  | 'mountain'
  | 'scrubland';

export interface BiomeColorPalette {
  primary: string;      // Hex color for dominant ground
  secondary: string;    // Accent color
  foliage: string;      // Plant tint
}

export interface BiomeContract {
  type: BiomeType;
  
  // Environmental properties
  temperature: number;      // -40 to 50°C
  moisture: number;         // 0.0 to 1.0
  terrainRoughness: number; // 0.0 to 1.0
  elevation: number;        // meters above sea level
  
  // Gameplay modifiers
  staminaDrainMod: number;
  movementSpeedMod: number;
  visibility: number;
  stealthBonus: number;
  
  // Spawning rules
  preySpawnRate: number;
  stockSpawnRate: number;
  predatorPatrolChance: number;
  
  // Resource types
  resources: string[];
  groundCover: string[];
  plantTypes: string[];
  
  // Rendering data
  colorPalette: BiomeColorPalette;
}

/**
 * CrewAI Deliverable: BiomeArchetypes
 * 
 * Provide default configurations for all 7 biomes
 */
export type BiomeArchetypes = Record<BiomeType, Omit<BiomeContract, 'type'>>;

/**
 * CrewAI Deliverable: BiomeGenerator
 * 
 * Procedural biome generation from seed
 */
export interface BiomeGeneratorContract {
  /**
   * Generate biome configuration from world seed
   * @param seed - World generation seed
   * @param chunkX - Chunk X coordinate
   * @param chunkZ - Chunk Z coordinate
   * @returns BiomeContract for this chunk
   */
  generateBiome(seed: number, chunkX: number, chunkZ: number): BiomeContract;
  
  /**
   * Blend between two biomes for smooth transitions
   */
  blendBiomes(biome1: BiomeContract, biome2: BiomeContract, blend: number): BiomeContract;
}
