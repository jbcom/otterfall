import { describe, it, expect, beforeEach } from 'vitest';
import { World } from 'miniplex';
import type { Entity } from './world';
import { hasPhysics, hasAI, isInteractable } from './world';

describe('ECS World', () => {
  let world: World<Entity>;

  beforeEach(() => {
    world = new World<Entity>();
  });

  describe('Entity Creation', () => {
    it('creates an entity with basic properties', () => {
      const entity = world.add({
        id: 'test-entity',
        transform: {
          position: { x: 0, y: 0, z: 0 },
          rotation: { x: 0, y: 0, z: 0, w: 1 },
          scale: { x: 1, y: 1, z: 1 },
        },
      });

      expect(entity.id).toBe('test-entity');
      expect(entity.transform?.position.x).toBe(0);
    });

    it('creates an entity with health component', () => {
      const entity = world.add({
        id: 'creature',
        health: {
          current: 100,
          max: 100,
        },
      });

      expect(entity.health?.current).toBe(100);
      expect(entity.health?.max).toBe(100);
    });

    it('allows adding components after creation', () => {
      const entity = world.add({ id: 'partial' });
      
      world.addComponent(entity, 'health', { current: 50, max: 100 });
      
      expect(entity.health?.current).toBe(50);
    });

    it('removes components correctly', () => {
      const entity = world.add({
        id: 'full',
        health: { current: 100, max: 100 },
      });
      
      world.removeComponent(entity, 'health');
      
      expect(entity.health).toBeUndefined();
    });
  });

  describe('Entity Queries', () => {
    beforeEach(() => {
      // Add various entities
      world.add({
        id: 'player',
        transform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
        physical: { mass: 70, friction: 0.5, restitution: 0.2 },
        health: { current: 100, max: 100 },
      });
      
      world.add({
        id: 'npc',
        transform: { position: { x: 5, y: 0, z: 5 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
        species: { type: 'otter', role: 'prey' },
        aiControl: { behavior: 'idle', target: null },
      });
      
      world.add({
        id: 'static-prop',
        transform: { position: { x: 10, y: 0, z: 10 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
      });
    });

    it('queries entities with specific components', () => {
      const withHealth = world.with('health');
      
      expect([...withHealth].length).toBe(1);
      expect([...withHealth][0].id).toBe('player');
    });

    it('queries entities with multiple components', () => {
      const withTransformAndPhysical = world.with('transform', 'physical');
      
      expect([...withTransformAndPhysical].length).toBe(1);
      expect([...withTransformAndPhysical][0].id).toBe('player');
    });

    it('queries entities without specific components', () => {
      const withoutHealth = world.without('health');
      const ids = [...withoutHealth].map(e => e.id);
      
      expect(ids).toContain('npc');
      expect(ids).toContain('static-prop');
      expect(ids).not.toContain('player');
    });
  });

  describe('Type Guards', () => {
    it('hasPhysics returns true for entities with transform and physical', () => {
      const entity: Entity = {
        id: 'physical-entity',
        transform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
        physical: { mass: 1, friction: 0.5, restitution: 0.2 },
      };
      
      expect(hasPhysics(entity)).toBe(true);
    });

    it('hasPhysics returns false for entities without physical', () => {
      const entity: Entity = {
        id: 'no-physics',
        transform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
      };
      
      expect(hasPhysics(entity)).toBe(false);
    });

    it('hasAI returns true for AI-controlled entities', () => {
      const entity: Entity = {
        id: 'ai-entity',
        transform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
        species: { type: 'otter', role: 'prey' },
        aiControl: { behavior: 'wander', target: null },
      };
      
      expect(hasAI(entity)).toBe(true);
    });

    it('isInteractable returns true for interactable entities', () => {
      const entity: Entity = {
        id: 'interactable-entity',
        transform: { position: { x: 0, y: 0, z: 0 }, rotation: { x: 0, y: 0, z: 0, w: 1 }, scale: { x: 1, y: 1, z: 1 } },
        interactable: { type: 'pickup', label: 'Berry', range: 2 },
      };
      
      expect(isInteractable(entity)).toBe(true);
    });
  });

  describe('Entity Lifecycle', () => {
    it('removes entities from world', () => {
      const entity = world.add({ id: 'to-remove' });
      const initialSize = world.entities.length;
      
      world.remove(entity);
      
      expect(world.entities.length).toBe(initialSize - 1);
    });

    it('clears all entities', () => {
      world.add({ id: 'entity-1' });
      world.add({ id: 'entity-2' });
      world.add({ id: 'entity-3' });
      
      world.clear();
      
      expect(world.entities.length).toBe(0);
    });
  });
});
