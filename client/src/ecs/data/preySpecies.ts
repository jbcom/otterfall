/**
 * Consolidated prey species data
 * Prey are living animals that flee from predators
 */

export const PREY_SPECIES_DATA = {
  rabbit: {
    name: 'Rabbit',
    meshyPrompt: 'sculpture style rabbit in A-pose, long ears, fluffy tail, quadruped mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#9a8a7a',
    markings: ['white_tail'],
    nativeBiome: ['forest', 'scrubland'],
    
    baseHealth: 30,
    mass: 2,
    attacks: [
      { name: 'Kick', damage: 3, staminaCost: 5, cooldown: 1.5, range: 0.8 }
    ],
    
    walkSpeed: 2.0,
    runSpeed: 9.0, // Very fast escape
    swimSpeed: 2.0,
    climbSpeed: 0,
    jumpHeight: 1.5,
    
    personality: 'timid' as const,
    awarenessRadius: 18, // Alert prey
    fleeThreshold: 0.95, // Flees at 95% health
    
    dropItems: [
      { item: 'rabbit_meat', quantity: 1, chance: 1.0 },
      { item: 'rabbit_pelt', quantity: 1, chance: 0.7 }
    ]
  },
  
  deer: {
    name: 'Deer',
    meshyPrompt: 'sculpture style deer in A-pose with small antlers, graceful build, quadruped mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'large' as const,
    primaryColor: '#aa8a6a',
    markings: ['white_spots', 'white_tail'],
    nativeBiome: ['forest', 'scrubland'],
    
    baseHealth: 80,
    mass: 40,
    attacks: [
      { name: 'Antler Strike', damage: 12, staminaCost: 15, cooldown: 2.0, range: 1.5 }
    ],
    
    walkSpeed: 2.5,
    runSpeed: 11.0, // Fast and agile
    swimSpeed: 4.0,
    climbSpeed: 0,
    jumpHeight: 2.0,
    
    personality: 'timid' as const,
    awarenessRadius: 22, // Very alert
    fleeThreshold: 0.9,
    
    dropItems: [
      { item: 'venison', quantity: 3, chance: 1.0 },
      { item: 'deer_hide', quantity: 1, chance: 1.0 },
      { item: 'antler_fragment', quantity: 1, chance: 0.4 }
    ]
  },
  
  grouse: {
    name: 'Grouse',
    meshyPrompt: 'sculpture style grouse bird in A-pose, plump ground bird with short wings, avian, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#7a6a5a',
    markings: ['speckled_pattern'],
    nativeBiome: ['forest', 'scrubland'],
    
    baseHealth: 20,
    mass: 0.5,
    attacks: [],
    
    walkSpeed: 1.5,
    runSpeed: 3.0,
    swimSpeed: 0,
    climbSpeed: 0,
    jumpHeight: 3.0, // Flies short distances
    
    personality: 'timid' as const,
    awarenessRadius: 14,
    fleeThreshold: 1.0, // Always flees
    
    dropItems: [
      { item: 'bird_meat', quantity: 1, chance: 1.0 },
      { item: 'feathers', quantity: 2, chance: 1.0 }
    ]
  },
  
  vole: {
    name: 'Vole',
    meshyPrompt: 'sculpture style vole in A-pose, small rodent with short tail, quadruped mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#6a5a4a',
    markings: [],
    nativeBiome: ['marsh', 'forest', 'scrubland'],
    
    baseHealth: 15,
    mass: 0.3,
    attacks: [],
    
    walkSpeed: 1.8,
    runSpeed: 5.0,
    swimSpeed: 2.0,
    climbSpeed: 0.5,
    jumpHeight: 0.5,
    
    personality: 'timid' as const,
    awarenessRadius: 10,
    fleeThreshold: 1.0,
    
    dropItems: [
      { item: 'small_meat', quantity: 1, chance: 0.8 }
    ]
  },
  
  capybara: {
    name: 'Capybara',
    meshyPrompt: 'sculpture style capybara in A-pose, large rodent with barrel body, semi-aquatic quadruped mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'large' as const,
    primaryColor: '#aa9a7a',
    markings: [],
    nativeBiome: ['marsh', 'jungle'],
    
    baseHealth: 90,
    mass: 50,
    attacks: [
      { name: 'Bite', damage: 8, staminaCost: 10, cooldown: 1.8, range: 1.2 }
    ],
    
    walkSpeed: 2.0,
    runSpeed: 4.0, // Slow on land
    swimSpeed: 6.0, // Fast in water
    climbSpeed: 0,
    jumpHeight: 0.6,
    
    personality: 'docile' as const,
    awarenessRadius: 12,
    fleeThreshold: 0.7,
    
    dropItems: [
      { item: 'capybara_meat', quantity: 4, chance: 1.0 },
      { item: 'thick_hide', quantity: 1, chance: 0.8 }
    ]
  },
  
  wallaby: {
    name: 'Wallaby',
    meshyPrompt: 'sculpture style wallaby in A-pose, kangaroo-like marsupial with powerful hind legs, quadruped mammal, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'medium' as const,
    primaryColor: '#9a8a6a',
    markings: ['white_chest'],
    nativeBiome: ['scrubland', 'forest'],
    
    baseHealth: 60,
    mass: 20,
    attacks: [
      { name: 'Kick', damage: 15, staminaCost: 12, cooldown: 1.5, range: 1.4 }
    ],
    
    walkSpeed: 2.5,
    runSpeed: 10.0, // Hopping is fast
    swimSpeed: 3.0,
    climbSpeed: 0,
    jumpHeight: 2.5,
    
    personality: 'timid' as const,
    awarenessRadius: 20,
    fleeThreshold: 0.85,
    
    dropItems: [
      { item: 'wallaby_meat', quantity: 2, chance: 1.0 },
      { item: 'wallaby_hide', quantity: 1, chance: 0.9 }
    ]
  },
  
  fish_bass: {
    name: 'Bass',
    meshyPrompt: 'sculpture style bass fish in swimming pose, streamlined body, fins extended, aquatic creature, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#5a6a4a',
    markings: ['darker_stripes'],
    nativeBiome: ['marsh'],
    
    baseHealth: 25,
    mass: 1.5,
    attacks: [],
    
    walkSpeed: 0,
    runSpeed: 0,
    swimSpeed: 7.0, // Aquatic only
    climbSpeed: 0,
    jumpHeight: 0,
    
    personality: 'docile' as const,
    awarenessRadius: 8,
    fleeThreshold: 1.0,
    
    dropItems: [
      { item: 'fish_meat', quantity: 1, chance: 1.0 },
      { item: 'fish_scales', quantity: 1, chance: 0.5 }
    ]
  },
  
  fish_trout: {
    name: 'Trout',
    meshyPrompt: 'sculpture style trout fish in swimming pose, spotted pattern, streamlined body, aquatic creature, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'small' as const,
    primaryColor: '#6a7a8a',
    markings: ['black_spots', 'red_stripe'],
    nativeBiome: ['marsh', 'mountain'],
    
    baseHealth: 20,
    mass: 1.0,
    attacks: [],
    
    walkSpeed: 0,
    runSpeed: 0,
    swimSpeed: 8.0, // Fast swimmer
    climbSpeed: 0,
    jumpHeight: 0.5, // Can jump out of water
    
    personality: 'timid' as const,
    awarenessRadius: 10,
    fleeThreshold: 1.0,
    
    dropItems: [
      { item: 'trout_meat', quantity: 1, chance: 1.0 }
    ]
  },
  
  crayfish: {
    name: 'Crayfish',
    meshyPrompt: 'sculpture style crayfish in pose, lobster-like crustacean with claws, aquatic creature, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#7a4a3a',
    markings: [],
    nativeBiome: ['marsh'],
    
    baseHealth: 10,
    mass: 0.2,
    attacks: [
      { name: 'Pinch', damage: 2, staminaCost: 3, cooldown: 1.0, range: 0.5 }
    ],
    
    walkSpeed: 0.8,
    runSpeed: 1.5,
    swimSpeed: 4.0,
    climbSpeed: 0,
    jumpHeight: 0,
    
    personality: 'defensive' as const,
    awarenessRadius: 6,
    fleeThreshold: 0.9,
    
    dropItems: [
      { item: 'crayfish_meat', quantity: 1, chance: 1.0 },
      { item: 'crayfish_shell', quantity: 1, chance: 0.6 }
    ]
  },
  
  frog: {
    name: 'Frog',
    meshyPrompt: 'sculpture style frog in A-pose, amphibian with bulging eyes and webbed feet, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#5a7a4a',
    markings: ['spotted_pattern'],
    nativeBiome: ['marsh', 'jungle'],
    
    baseHealth: 12,
    mass: 0.15,
    attacks: [],
    
    walkSpeed: 1.0,
    runSpeed: 2.0,
    swimSpeed: 5.0,
    climbSpeed: 1.0,
    jumpHeight: 2.0, // Excellent jumper
    
    personality: 'timid' as const,
    awarenessRadius: 8,
    fleeThreshold: 1.0,
    
    dropItems: [
      { item: 'frog_legs', quantity: 1, chance: 0.8 }
    ]
  },
  
  beetle: {
    name: 'Beetle',
    meshyPrompt: 'sculpture style beetle in pose, insect with shell and legs, arthropod, clean geometry',
    meshyArtStyle: 'sculpture' as const,
    size: 'tiny' as const,
    primaryColor: '#3a2a1a',
    markings: ['shiny_shell'],
    nativeBiome: ['forest', 'jungle', 'scrubland'],
    
    baseHealth: 5,
    mass: 0.05,
    attacks: [],
    
    walkSpeed: 0.5,
    runSpeed: 1.0,
    swimSpeed: 0,
    climbSpeed: 0.8,
    jumpHeight: 0.3,
    
    personality: 'docile' as const,
    awarenessRadius: 4,
    fleeThreshold: 1.0,
    
    dropItems: [
      { item: 'insect_parts', quantity: 1, chance: 0.5 }
    ]
  }
} as const;

export type PreySpecies = keyof typeof PREY_SPECIES_DATA;
