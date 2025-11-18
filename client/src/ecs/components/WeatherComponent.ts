/**
 * Weather Component - global state affecting entire world
 * Changes over time, affects visibility, combat, and resource gathering
 */

export type WeatherType = 
  | 'clear'
  | 'rain'
  | 'fog'
  | 'snow'
  | 'storm'
  | 'sandstorm'; // Desert-specific

export interface WeatherComponent {
  current: WeatherType;
  intensity: number;     // 0.0 to 1.0
  transitionProgress: number; // 0.0 to 1.0 when changing weather
  nextWeather: WeatherType | null;
  
  // Wind affects particle systems and plant sway
  windSpeed: number;     // 0 to 20 m/s
  windDirection: [number, number]; // Normalized vector
  
  // Gameplay effects
  visibilityMod: number;      // 0.3 = heavy fog, 1.0 = clear
  soundMuffling: number;      // 0.0 to 1.0 (1.0 = thunder drowns out footsteps)
  fireEffectiveness: number;  // Rain makes fire attacks weaker
  waterDepthIncrease: number; // Rain raises water levels
  
  // Duration tracking
  startTime: number;     // Timestamp when this weather began
  durationMinutes: number; // How long it will last
}

// Weather presets
export const WEATHER_PRESETS: Record<WeatherType, Omit<WeatherComponent, 'current' | 'startTime' | 'durationMinutes' | 'transitionProgress' | 'nextWeather'>> = {
  clear: {
    intensity: 0,
    windSpeed: 2,
    windDirection: [1, 0],
    visibilityMod: 1.0,
    soundMuffling: 0.0,
    fireEffectiveness: 1.0,
    waterDepthIncrease: 0
  },
  
  rain: {
    intensity: 0.6,
    windSpeed: 8,
    windDirection: [0.7, 0.7],
    visibilityMod: 0.7,
    soundMuffling: 0.4,
    fireEffectiveness: 0.5, // Fire attacks half as effective
    waterDepthIncrease: 0.2 // Water level rises
  },
  
  fog: {
    intensity: 0.8,
    windSpeed: 1,
    windDirection: [0, 0],
    visibilityMod: 0.3, // Severe visibility reduction
    soundMuffling: 0.2,
    fireEffectiveness: 0.8,
    waterDepthIncrease: 0
  },
  
  snow: {
    intensity: 0.5,
    windSpeed: 5,
    windDirection: [0.5, 0.8],
    visibilityMod: 0.6,
    soundMuffling: 0.5, // Snow muffles sound
    fireEffectiveness: 0.7,
    waterDepthIncrease: 0
  },
  
  storm: {
    intensity: 1.0,
    windSpeed: 15,
    windDirection: [1, 0.5],
    visibilityMod: 0.4,
    soundMuffling: 0.8, // Thunder is loud
    fireEffectiveness: 0.2, // Storm nearly negates fire
    waterDepthIncrease: 0.5 // Flooding
  },
  
  sandstorm: {
    intensity: 0.9,
    windSpeed: 20,
    windDirection: [1, 0],
    visibilityMod: 0.2, // Nearly blind
    soundMuffling: 0.6,
    fireEffectiveness: 0.3,
    waterDepthIncrease: 0
  }
};

// Weather transition rules by biome
export const WEATHER_TRANSITIONS = {
  marsh: ['clear', 'rain', 'fog', 'storm'],
  forest: ['clear', 'rain', 'fog'],
  desert: ['clear', 'sandstorm'],
  tundra: ['clear', 'snow', 'storm'],
  savanna: ['clear', 'rain'],
  mountain: ['clear', 'fog', 'snow'],
  scrubland: ['clear', 'fog']
} as const;
