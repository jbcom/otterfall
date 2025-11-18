import { Species } from './components';

// Predator species definitions
export const PREDATOR_SPECIES: Species[] = [
  {
    id: 'marsh_wolf',
    type: 'predator',
    displayName: 'Marsh Wolf',
    maxSpeed: 8,
    turnRate: 2.5,
    size: 1.2
  },
  {
    id: 'river_snake',
    type: 'predator',
    displayName: 'River Snake',
    maxSpeed: 5,
    turnRate: 3.0,
    size: 0.8
  },
  {
    id: 'swamp_hawk',
    type: 'predator',
    displayName: 'Swamp Hawk',
    maxSpeed: 12,
    turnRate: 4.0,
    size: 0.9
  },
  // More predators...
];

// Prey species definitions
export const PREY_SPECIES: Species[] = [
  {
    id: 'marsh_rabbit',
    type: 'prey',
    displayName: 'Marsh Rabbit',
    maxSpeed: 7,
    turnRate: 3.0,
    size: 0.5
  },
  {
    id: 'river_fish',
    type: 'prey',
    displayName: 'River Fish',
    maxSpeed: 6,
    turnRate: 3.5,
    size: 0.4
  },
  {
    id: 'marsh_frog',
    type: 'prey',
    displayName: 'Marsh Frog',
    maxSpeed: 4,
    turnRate: 2.5,
    size: 0.3
  },
  // More prey...
];

// Helper functions
export const getSpeciesById = (id: string): Species | undefined => {
  return [...PREDATOR_SPECIES, ...PREY_SPECIES].find(species => species.id === id);
};

export const getPredators = (): Species[] => PREDATOR_SPECIES;

export const getPrey = (): Species[] => PREY_SPECIES;
