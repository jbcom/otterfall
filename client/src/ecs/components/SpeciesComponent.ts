/**
 * Species Component - defines what kind of creature this is
 * Globally diverse species, not just Western fauna
 */

// Predators (playable + NPC hunters)
export type PredatorSpecies =
  // Temperate
  | 'otter'       // River otter - swimmer, fisher, playful but fierce
  | 'fox'         // Red fox - cunning, agile, versatile
  | 'badger'      // European badger - tank, burrow specialist
  | 'wolf'        // Gray wolf - pack tactics, endurance hunter
  | 'raccoon'     // Raccoon - clever, tool user, scrappy
  
  // Tropical/Subtropical
  | 'pangolin'    // Pangolin - armored tank, rolling attack
  | 'mongoose'    // Mongoose - lightning reflexes, cobra hunter
  | 'coati'       // Coati - climber, balanced fighter
  
  // Desert
  | 'meerkat'     // Meerkat - pack tactics, lookout ability
  | 'honey_badger' // Honey badger - fearless, venom resistant
  
  // Mountain
  | 'red_panda'   // Red panda - acrobatic, tree climber
  
  // Australia/Oceania
  | 'wombat'      // Wombat - burrow defense, headbutt specialist
  | 'tasmanian_devil'; // Tasmanian devil - ferocious bite, berserker

// Prey (living animals you can hunt - all have AI behavior)
export type PreySpecies =
  // Land animals (flee behavior)
  | 'rabbit'      // Fast, timid, easy to catch
  | 'deer'        // Medium speed, wary, good rewards
  | 'grouse'      // Ground bird, flies short distances
  | 'vole'        // Tiny, quick, minimal rewards
  | 'capybara'    // Large, slow, near water
  | 'wallaby'     // Australia - medium speed, good rewards
  
  // Aquatic creatures (swim behavior)
  | 'fish_bass'   // Common fish
  | 'fish_trout'  // Rarer fish
  | 'crayfish'    // Small crustacean
  | 'frog'        // Amphibian
  
  // Insects (minimal AI, easy to catch)
  | 'beetle';     // Insect

export type AnySpecies = PredatorSpecies | PreySpecies;

export interface SpeciesComponent {
  type: AnySpecies;
  category: 'predator' | 'prey';
  
  // Meshy generation data (for pre-build script)
  meshyPrompt: string;
  meshyArtStyle: 'realistic' | 'sculpture';
  
  // Visual properties
  size: 'tiny' | 'small' | 'medium' | 'large';
  primaryColor: string;
  markings: readonly string[] | string[];
  
  // Natural home biome
  nativeBiome: readonly string[] | string[];
  
  // Resource drops when hunted/gathered
  dropItems: Array<{
    item: string;
    quantity: number;
    chance: number;
  }>;
}

// Species definitions with Meshy prompts
export const SPECIES_DEFINITIONS: Record<PredatorSpecies, Omit<SpeciesComponent, 'type' | 'category'>> = {
  otter: {
    meshyPrompt: 'sculpture style river otter standing upright on hind legs in A-pose, sleek furry mammal with long tail and webbed paws, clean geometry, no water',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#5a4a3a',
    markings: ['white_chest', 'white_throat'],
    nativeBiome: ['marsh', 'forest'],
    dropItems: []
  },
  
  fox: {
    meshyPrompt: 'sculpture style red fox standing on hind legs in A-pose, bushy tail, pointed ears, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'small',
    primaryColor: '#d4664a',
    markings: ['white_chest', 'black_legs', 'white_tail_tip'],
    nativeBiome: ['forest', 'scrubland'],
    dropItems: []
  },
  
  badger: {
    meshyPrompt: 'sculpture style European badger standing on hind legs in A-pose, stocky build, distinctive black and white face stripes, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#4a4a4a',
    markings: ['white_face_stripes', 'black_stripes'],
    nativeBiome: ['forest', 'scrubland'],
    dropItems: []
  },
  
  wolf: {
    meshyPrompt: 'sculpture style gray wolf standing on hind legs in A-pose, athletic build, pointed ears, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'large',
    primaryColor: '#6a6a5a',
    markings: ['darker_back', 'lighter_belly'],
    nativeBiome: ['forest', 'tundra', 'mountain'],
    dropItems: []
  },
  
  raccoon: {
    meshyPrompt: 'sculpture style raccoon standing on hind legs in A-pose, distinctive black eye mask, ringed tail, furry mammal with dexterous paws, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'small',
    primaryColor: '#7a7a6a',
    markings: ['black_eye_mask', 'ringed_tail'],
    nativeBiome: ['forest', 'marsh'],
    dropItems: []
  },
  
  pangolin: {
    meshyPrompt: 'sculpture style pangolin standing on hind legs in A-pose, scaled armor covering body, long tail, mammal with protective scales, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#8a7a5a',
    markings: ['armored_scales', 'tan_belly'],
    nativeBiome: ['savanna', 'forest'],
    dropItems: []
  },
  
  mongoose: {
    meshyPrompt: 'sculpture style mongoose standing on hind legs in A-pose, sleek athletic build, alert posture, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'small',
    primaryColor: '#9a8a6a',
    markings: ['lighter_belly'],
    nativeBiome: ['savanna', 'desert'],
    dropItems: []
  },
  
  coati: {
    meshyPrompt: 'sculpture style coati standing on hind legs in A-pose, long ringed tail, elongated snout, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#7a5a4a',
    markings: ['ringed_tail', 'white_snout'],
    nativeBiome: ['forest', 'scrubland'],
    dropItems: []
  },
  
  meerkat: {
    meshyPrompt: 'sculpture style meerkat standing upright in A-pose, slender build, alert lookout posture, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'small',
    primaryColor: '#b89a7a',
    markings: ['darker_back_stripes', 'eye_patches'],
    nativeBiome: ['desert', 'savanna'],
    dropItems: []
  },
  
  honey_badger: {
    meshyPrompt: 'sculpture style honey badger standing on hind legs in A-pose, stocky fearless build, distinctive white back stripe, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#3a3a3a',
    markings: ['white_back_stripe'],
    nativeBiome: ['desert', 'savanna', 'scrubland'],
    dropItems: []
  },
  
  red_panda: {
    meshyPrompt: 'sculpture style red panda standing on hind legs in A-pose, fluffy ringed tail, reddish fur, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#c47a5a',
    markings: ['ringed_tail', 'white_face_markings', 'darker_legs'],
    nativeBiome: ['mountain', 'forest'],
    dropItems: []
  },
  
  wombat: {
    meshyPrompt: 'sculpture style wombat standing on hind legs in A-pose, stocky powerful build, short legs, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#6a5a4a',
    markings: ['darker_nose'],
    nativeBiome: ['scrubland', 'forest'],
    dropItems: []
  },
  
  tasmanian_devil: {
    meshyPrompt: 'sculpture style Tasmanian devil standing on hind legs in A-pose, muscular aggressive build, powerful jaws, black furry mammal with white markings, clean geometry',
    meshyArtStyle: 'sculpture',
    size: 'medium',
    primaryColor: '#2a2a2a',
    markings: ['white_chest_patch', 'white_rump'],
    nativeBiome: ['scrubland', 'forest'],
    dropItems: []
  }
};
