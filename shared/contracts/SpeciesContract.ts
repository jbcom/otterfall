/**
 * Species Contract - Shared type definitions for creature/NPC system
 * 
 * CrewAI MUST implement this contract when building:
 * - DFU creature mapping to natural world species
 * - AI behavior systems
 * - Species stat balancing
 */

export type SpeciesArchetype = 
  | 'predator'    // Aggressive hunters (wolf, fox, badger)
  | 'prey'        // Fleeing herbivores (rabbit, deer, mouse)
  | 'omnivore'    // Mixed behavior (raccoon, bear)
  | 'scavenger'   // Opportunistic (crow, vulture)
  | 'neutral';    // Non-hostile (frog, turtle)

export interface SpeciesContract {
  id: string;                    // Unique identifier
  archetype: SpeciesArchetype;
  displayName: string;
  scientificName: string;        // e.g., "Lutra canadensis" (river otter)
  
  // Physical stats
  size: number;                  // 0.1 to 3.0 (meters)
  mass: number;                  // kg
  maxSpeed: number;              // m/s
  turnRate: number;              // degrees/second
  
  // Combat stats
  health: number;
  damage: number;
  attackRange: number;           // meters
  attackCooldown: number;        // seconds
  
  // AI behavior
  detectionRange: number;        // meters
  fleeThreshold: number;         // health % to flee at
  aggressionLevel: number;       // 0.0 to 1.0
  territoryRadius: number;       // meters
  
  // Movement capabilities
  canSwim: boolean;
  canClimb: boolean;
  canBurrow: boolean;
  canGlide: boolean;
  
  // Habitat preferences
  preferredBiomes: string[];     // BiomeType[]
  activeTimeOfDay: 'day' | 'night' | 'crepuscular' | 'any';
  
  // Visual/Audio (references to assets)
  modelPath?: string;
  soundSet?: string;
  
  // Drops/Loot
  dropTable: Array<{
    itemId: string;
    chance: number;              // 0.0 to 1.0
    quantity: { min: number; max: number };
  }>;
}

/**
 * CrewAI Deliverable: DFU Species Mapping
 * 
 * Map Daggerfall Unity fantasy creatures to Rivermarsh natural species
 */
export interface DFUSpeciesMappingContract {
  /**
   * Parse DFU creature data and map to natural world equivalents
   * 
   * Examples:
   * - DFU Wolf → Timber Wolf (Canis lupus)
   * - DFU Rat → Marsh Rat (Rattus norvegicus)
   * - DFU Bear → Black Bear (Ursus americanus)
   */
  mapDFUCreature(dfuCreatureId: string): SpeciesContract;
  
  /**
   * Get all mapped species
   */
  getAllSpecies(): SpeciesContract[];
  
  /**
   * Filter species by biome
   */
  getSpeciesByBiome(biomeType: string): SpeciesContract[];
}

/**
 * CrewAI Deliverable: Species Factory
 * 
 * Create ECS entities from species definitions
 */
export interface SpeciesFactoryContract {
  /**
   * Spawn a creature at given position
   */
  spawnCreature(
    speciesId: string,
    position: { x: number; y: number; z: number },
    level?: number
  ): string; // Returns entity ID
  
  /**
   * Get species data by ID
   */
  getSpecies(speciesId: string): SpeciesContract | null;
}
