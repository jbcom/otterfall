/**
 * Time of Day Component - global cycle affecting creature behavior
 * 24-hour cycle with dawn/day/dusk/night phases
 */

export type TimePhase = 'dawn' | 'day' | 'dusk' | 'night';

export interface TimeOfDayComponent {
  hour: number;          // 0.0 to 24.0 (fractional for smooth transitions)
  phase: TimePhase;
  
  // Lighting properties (for renderer)
  sunIntensity: number;  // 0.0 to 1.0
  sunAngle: number;      // 0 to 360 degrees
  ambientLight: number;  // 0.0 to 1.0
  
  // Creature behavior modifiers
  nocturnalBonus: number;    // 1.5 = nocturnal predators 50% stronger at night
  preyAlertness: number;     // 1.5 = prey more skittish at dawn/dusk
  stealthBonus: number;      // 0.3 = easier to sneak at night
  
  // Visual atmosphere
  fogDensity: number;        // More fog at dawn/dusk
  starVisibility: number;    // 0.0 to 1.0
  moonPhase: number;         // 0.0 to 1.0 (affects night brightness)
  
  // Time flow
  timeScale: number;         // 1.0 = real-time, 60.0 = 1 game hour per real minute
}

// Time phase definitions
export const TIME_PHASES = {
  dawn: { start: 5, end: 7 },
  day: { start: 7, end: 17 },
  dusk: { start: 17, end: 19 },
  night: { start: 19, end: 5 }
} as const;

// Calculate time-based modifiers
export function getTimeModifiers(hour: number, moonPhase: number): Omit<TimeOfDayComponent, 'hour' | 'phase' | 'timeScale'> {
  const phase = getPhaseFromHour(hour);
  
  // Sun angle (6am = 0°, 12pm = 90°, 6pm = 180°)
  const sunAngle = ((hour - 6) / 12) * 180;
  
  // Sun intensity peaks at noon
  const sunIntensity = phase === 'day' 
    ? Math.sin(((hour - 6) / 12) * Math.PI) 
    : 0;
  
  // Ambient light is lower at night
  const ambientLight = phase === 'night' 
    ? 0.2 + (moonPhase * 0.3) // Moon provides some light
    : phase === 'day' 
    ? 1.0 
    : 0.6; // Dawn/dusk
  
  // Nocturnal creatures are stronger at night
  const nocturnalBonus = phase === 'night' ? 1.3 : 1.0;
  
  // Prey are most alert during transition periods
  const preyAlertness = (phase === 'dawn' || phase === 'dusk') ? 1.4 : 1.0;
  
  // Stealth is easier in darkness
  const stealthBonus = phase === 'night' 
    ? 0.4 
    : (phase === 'dawn' || phase === 'dusk') 
    ? 0.2 
    : 0;
  
  // Fog at dawn/dusk
  const fogDensity = (phase === 'dawn' || phase === 'dusk') ? 0.3 : 0;
  
  // Stars visible at night
  const starVisibility = phase === 'night' ? 1.0 : 0;
  
  return {
    sunIntensity,
    sunAngle,
    ambientLight,
    nocturnalBonus,
    preyAlertness,
    stealthBonus,
    fogDensity,
    starVisibility,
    moonPhase
  };
}

export function getPhaseFromHour(hour: number): TimePhase {
  const h = hour % 24;
  if (h >= TIME_PHASES.dawn.start && h < TIME_PHASES.dawn.end) return 'dawn';
  if (h >= TIME_PHASES.day.start && h < TIME_PHASES.day.end) return 'day';
  if (h >= TIME_PHASES.dusk.start && h < TIME_PHASES.dusk.end) return 'dusk';
  return 'night';
}
