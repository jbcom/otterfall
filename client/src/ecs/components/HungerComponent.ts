/**
 * Hunger Component - tracks creature hunger level
 */

export interface HungerComponent {
  current: number; // 0-100, current hunger level
  max: number; // Maximum hunger
  hungerRate: number; // How fast hunger increases per second
  lastUpdated: number; // Timestamp
}
