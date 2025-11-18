/**
 * Consolidated predator species data
 * Includes visual, combat, movement, and AI properties
 */

export const PREDATOR_SPECIES_DATA = {
  otter: {
    // Visual
    name: 'River Otter',
    meshyPrompt: 'sculpture style river otter standing upright on hind legs in A-pose, sleek furry mammal with long tail and webbed paws, clean geometry, no water',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#5a4a3a',
    markings: ['white_chest', 'white_throat'],
    nativeBiome: ['marsh', 'forest'],
    
    // Combat
    baseHealth: 100,
    mass: 8, // kg
    attacks: [
      { name: 'Bite', type: 'bite' as const, damage: 15, staminaCost: 10, cooldown: 1.0, range: 1.5, knockback: 1, stunDuration: 0, animationId: 4 },
      { name: 'Tail Slap', type: 'tail_whip' as const, damage: 10, staminaCost: 8, cooldown: 0.8, range: 2.0, knockback: 2, stunDuration: 0, animationId: 17 },
      { name: 'Pounce', type: 'pounce' as const, damage: 20, staminaCost: 20, cooldown: 3.0, range: 3.0, knockback: 3, stunDuration: 0.5, animationId: 18 }
    ],
    
    // Movement
    walkSpeed: 2.5,
    runSpeed: 6.0,
    swimSpeed: 8.0, // Otters are excellent swimmers
    climbSpeed: 1.0,
    jumpHeight: 1.2,
    
    // AI
    personality: 'playful' as const,
    awarenessRadius: 15,
    aggressionLevel: 0.6,
    
    // Loot
    dropItems: [
      { item: 'otter_fur', quantity: 1, chance: 1.0 },
      { item: 'fish', quantity: 1, chance: 0.5 }
    ]
  },
  
  fox: {
    name: 'Red Fox',
    meshyPrompt: 'sculpture style red fox standing on hind legs in A-pose, bushy tail, pointed ears, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#d4664a',
    markings: ['white_chest', 'black_legs', 'white_tail_tip'],
    nativeBiome: ['forest', 'scrubland'],
    
    baseHealth: 80,
    mass: 6,
    attacks: [
      { name: 'Bite', damage: 12, staminaCost: 8, cooldown: 0.9, range: 1.2 },
      { name: 'Pounce', damage: 18, staminaCost: 15, cooldown: 2.5, range: 3.5 }
    ],
    
    walkSpeed: 3.0,
    runSpeed: 8.0, // Foxes are fast
    swimSpeed: 3.0,
    climbSpeed: 0.5,
    jumpHeight: 1.5,
    
    personality: 'cunning' as const,
    awarenessRadius: 18,
    aggressionLevel: 0.5,
    
    dropItems: [
      { item: 'fox_pelt', quantity: 1, chance: 1.0 }
    ]
  },
  
  badger: {
    name: 'European Badger',
    meshyPrompt: 'sculpture style European badger standing on hind legs in A-pose, stocky build, distinctive black and white face stripes, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#4a4a4a',
    markings: ['white_face_stripes', 'black_stripes'],
    nativeBiome: ['forest', 'scrubland'],
    
    baseHealth: 150, // Tank
    mass: 12,
    attacks: [
      { name: 'Bite', damage: 18, staminaCost: 12, cooldown: 1.2, range: 1.3 },
      { name: 'Claw Swipe', damage: 15, staminaCost: 10, cooldown: 1.0, range: 1.8 }
    ],
    
    walkSpeed: 1.8,
    runSpeed: 4.0, // Slow but tanky
    swimSpeed: 2.0,
    climbSpeed: 0.3,
    jumpHeight: 0.8,
    
    personality: 'aggressive' as const,
    awarenessRadius: 12,
    aggressionLevel: 0.8,
    
    dropItems: [
      { item: 'badger_hide', quantity: 1, chance: 1.0 }
    ]
  },
  
  wolf: {
    name: 'Gray Wolf',
    meshyPrompt: 'sculpture style gray wolf standing on hind legs in A-pose, athletic build, pointed ears, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'large' as const,
    primaryColor: '#6a6a5a',
    markings: ['darker_back', 'lighter_belly'],
    nativeBiome: ['forest', 'tundra', 'mountain'],
    
    baseHealth: 120,
    mass: 35,
    attacks: [
      { name: 'Bite', damage: 25, staminaCost: 15, cooldown: 1.5, range: 1.8 },
      { name: 'Lunge', damage: 30, staminaCost: 25, cooldown: 3.0, range: 4.0 }
    ],
    
    walkSpeed: 2.8,
    runSpeed: 10.0, // Fast endurance hunter
    swimSpeed: 4.0,
    climbSpeed: 0,
    jumpHeight: 1.5,
    
    personality: 'pack_hunter' as const,
    awarenessRadius: 25,
    aggressionLevel: 0.7,
    
    dropItems: [
      { item: 'wolf_pelt', quantity: 1, chance: 1.0 },
      { item: 'wolf_fang', quantity: 1, chance: 0.4 }
    ]
  },
  
  raccoon: {
    name: 'Raccoon',
    meshyPrompt: 'sculpture style raccoon standing on hind legs in A-pose, distinctive black eye mask, ringed tail, furry mammal with dexterous paws, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#7a7a6a',
    markings: ['black_eye_mask', 'ringed_tail'],
    nativeBiome: ['forest', 'marsh'],
    
    baseHealth: 70,
    mass: 5,
    attacks: [
      { name: 'Scratch', damage: 10, staminaCost: 6, cooldown: 0.7, range: 1.0 },
      { name: 'Bite', damage: 12, staminaCost: 8, cooldown: 1.0, range: 1.2 }
    ],
    
    walkSpeed: 2.2,
    runSpeed: 5.5,
    swimSpeed: 3.5,
    climbSpeed: 3.0, // Excellent climber
    jumpHeight: 1.3,
    
    personality: 'curious' as const,
    awarenessRadius: 14,
    aggressionLevel: 0.4,
    
    dropItems: [
      { item: 'raccoon_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  pangolin: {
    name: 'Pangolin',
    meshyPrompt: 'sculpture style pangolin standing on hind legs in A-pose, armored scales covering body, long tail, mammal with defensive plates, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#8a7a5a',
    markings: ['scale_pattern'],
    nativeBiome: ['savanna', 'forest'],
    
    baseHealth: 140, // Armored
    mass: 15,
    attacks: [
      { name: 'Tail Slam', damage: 22, staminaCost: 18, cooldown: 2.0, range: 2.5 },
      { name: 'Roll Attack', damage: 28, staminaCost: 30, cooldown: 4.0, range: 3.0 }
    ],
    
    walkSpeed: 1.5,
    runSpeed: 3.5, // Slow but armored
    swimSpeed: 2.5,
    climbSpeed: 1.5,
    jumpHeight: 0.6,
    
    personality: 'defensive' as const,
    awarenessRadius: 10,
    aggressionLevel: 0.3,
    
    dropItems: [
      { item: 'pangolin_scale', quantity: 2, chance: 1.0 }
    ]
  },
  
  mongoose: {
    name: 'Mongoose',
    meshyPrompt: 'sculpture style mongoose standing on hind legs in A-pose, sleek agile build, alert posture, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#9a8a6a',
    markings: ['darker_tail_tip'],
    nativeBiome: ['savanna', 'scrubland'],
    
    baseHealth: 60,
    mass: 3,
    attacks: [
      { name: 'Lightning Bite', damage: 14, staminaCost: 8, cooldown: 0.5, range: 1.0 },
      { name: 'Quick Strike', damage: 18, staminaCost: 12, cooldown: 1.0, range: 1.5 }
    ],
    
    walkSpeed: 3.5,
    runSpeed: 9.0, // Incredibly fast reflexes
    swimSpeed: 2.0,
    climbSpeed: 2.0,
    jumpHeight: 1.4,
    
    personality: 'aggressive' as const,
    awarenessRadius: 16,
    aggressionLevel: 0.75,
    
    dropItems: [
      { item: 'mongoose_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  coati: {
    name: 'Coati',
    meshyPrompt: 'sculpture style coati standing on hind legs in A-pose, long ringed tail, elongated snout, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#7a5a4a',
    markings: ['ringed_tail', 'white_snout'],
    nativeBiome: ['forest', 'jungle'],
    
    baseHealth: 90,
    mass: 7,
    attacks: [
      { name: 'Bite', damage: 13, staminaCost: 9, cooldown: 1.0, range: 1.3 },
      { name: 'Claw', damage: 11, staminaCost: 7, cooldown: 0.8, range: 1.5 }
    ],
    
    walkSpeed: 2.6,
    runSpeed: 6.5,
    swimSpeed: 3.0,
    climbSpeed: 4.0, // Excellent climber
    jumpHeight: 1.6,
    
    personality: 'playful' as const,
    awarenessRadius: 14,
    aggressionLevel: 0.5,
    
    dropItems: [
      { item: 'coati_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  meerkat: {
    name: 'Meerkat',
    meshyPrompt: 'sculpture style meerkat standing upright on hind legs in A-pose, alert sentinel posture, slender build, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#aa9a7a',
    markings: ['dark_eye_patches', 'striped_back'],
    nativeBiome: ['desert', 'savanna'],
    
    baseHealth: 50,
    mass: 1,
    attacks: [
      { name: 'Quick Bite', damage: 8, staminaCost: 5, cooldown: 0.6, range: 0.8 }
    ],
    
    walkSpeed: 2.8,
    runSpeed: 7.0,
    swimSpeed: 1.5,
    climbSpeed: 0.5,
    jumpHeight: 1.0,
    
    personality: 'pack_hunter' as const,
    awarenessRadius: 20, // Sentinel lookout ability
    aggressionLevel: 0.4,
    
    dropItems: [
      { item: 'meerkat_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  honey_badger: {
    name: 'Honey Badger',
    meshyPrompt: 'sculpture style honey badger standing on hind legs in A-pose, stocky fearless build, distinctive black and white coloration, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#3a3a3a',
    markings: ['white_back_stripe'],
    nativeBiome: ['desert', 'savanna', 'scrubland'],
    
    baseHealth: 160, // Nearly unkillable
    mass: 10,
    attacks: [
      { name: 'Ferocious Bite', damage: 24, staminaCost: 14, cooldown: 1.3, range: 1.4 },
      { name: 'Berserk Claw', damage: 20, staminaCost: 12, cooldown: 1.0, range: 1.6 }
    ],
    
    walkSpeed: 1.8,
    runSpeed: 4.5, // Not fast but unstoppable
    swimSpeed: 2.5,
    climbSpeed: 1.0,
    jumpHeight: 0.9,
    
    personality: 'aggressive' as const,
    awarenessRadius: 15,
    aggressionLevel: 0.95, // Fearless
    
    dropItems: [
      { item: 'honey_badger_hide', quantity: 1, chance: 1.0 }
    ]
  },
  
  red_panda: {
    name: 'Red Panda',
    meshyPrompt: 'sculpture style red panda standing on hind legs in A-pose, fluffy ringed tail, reddish fur, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#c47a5a',
    markings: ['ringed_tail', 'white_face_markings', 'darker_legs'],
    nativeBiome: ['mountain', 'forest'],
    
    baseHealth: 70,
    mass: 5,
    attacks: [
      { name: 'Swat', damage: 10, staminaCost: 7, cooldown: 0.8, range: 1.2 },
      { name: 'Bite', damage: 12, staminaCost: 9, cooldown: 1.1, range: 1.0 }
    ],
    
    walkSpeed: 2.0,
    runSpeed: 5.0,
    swimSpeed: 2.0,
    climbSpeed: 5.0, // Acrobatic tree climber
    jumpHeight: 2.0,
    
    personality: 'timid' as const,
    awarenessRadius: 12,
    aggressionLevel: 0.3,
    
    dropItems: [
      { item: 'red_panda_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  wombat: {
    name: 'Wombat',
    meshyPrompt: 'sculpture style wombat standing on hind legs in A-pose, stocky powerful build, short legs, furry mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#6a5a4a',
    markings: ['darker_nose'],
    nativeBiome: ['scrubland', 'forest'],
    
    baseHealth: 130,
    mass: 25,
    attacks: [
      { name: 'Headbutt', damage: 26, staminaCost: 16, cooldown: 2.0, range: 1.5 },
      { name: 'Body Slam', damage: 22, staminaCost: 18, cooldown: 2.5, range: 2.0 }
    ],
    
    walkSpeed: 1.5,
    runSpeed: 3.0, // Slow but powerful
    swimSpeed: 1.5,
    climbSpeed: 0,
    jumpHeight: 0.5,
    
    personality: 'defensive' as const,
    awarenessRadius: 10,
    aggressionLevel: 0.5,
    
    dropItems: [
      { item: 'wombat_fur', quantity: 1, chance: 1.0 }
    ]
  },
  
  tasmanian_devil: {
    name: 'Tasmanian Devil',
    meshyPrompt: 'sculpture style Tasmanian devil standing on hind legs in A-pose, muscular aggressive build, powerful jaws, black furry mammal with white markings, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#2a2a2a',
    markings: ['white_chest_patch', 'white_rump'],
    nativeBiome: ['scrubland', 'forest'],
    
    baseHealth: 110,
    mass: 9,
    attacks: [
      { name: 'Devastating Bite', damage: 30, staminaCost: 20, cooldown: 1.8, range: 1.4 },
      { name: 'Frenzy', damage: 35, staminaCost: 35, cooldown: 5.0, range: 1.5 }
    ],
    
    walkSpeed: 2.3,
    runSpeed: 6.0,
    swimSpeed: 2.5,
    climbSpeed: 0.8,
    jumpHeight: 1.0,
    
    personality: 'aggressive' as const,
    awarenessRadius: 16,
    aggressionLevel: 0.9, // Berserker
    
    dropItems: [
      { item: 'devil_hide', quantity: 1, chance: 1.0 }
    ]
  }
} as const;

export type PredatorSpecies = keyof typeof PREDATOR_SPECIES_DATA;
