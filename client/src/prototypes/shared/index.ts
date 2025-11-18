import { PrototypeManifest } from './types';

export const PROTOTYPES: PrototypeManifest[] = [
  {
    id: 'all_assets_hardcoded',
    title: 'Alpha PoC (All Assets Hardcoded)',
    description: 'Original hardcoded implementation with player, NPCs, terrain, and all game systems',
    order: 1,
    load: () => import('../all_assets_hardcoded/App') as Promise<{ default: React.ComponentType }>,
  },
  {
    id: 'biome_selector_diorama',
    title: 'Biome Selector Diorama',
    description: 'ECS-driven diorama rendering with SDF ground/sky, gyroscopic horizon, and biome controls',
    order: 2,
    load: () => import('../biome_selector_diorama/App') as Promise<{ default: React.ComponentType }>,
  },
];

export * from './types';
