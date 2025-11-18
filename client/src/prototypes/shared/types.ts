import { ReactNode } from 'react';

export interface PrototypeManifest {
  id: string;
  title: string;
  description: string;
  order: number;
  load: () => Promise<{ default: React.ComponentType }>;
}

export interface PrototypeAppProps {
  onExit?: () => void;
}
