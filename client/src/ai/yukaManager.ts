import * as YUKA from 'yuka';
import { Entity } from '../ecs/world';

export interface YukaBridge {
  ecsEntityId: string;
  yukaVehicle: YUKA.Vehicle;
  stateMachine: YUKA.StateMachine;
}

class YukaManager {
  private entityManager: YUKA.EntityManager;
  private time: YUKA.Time;
  private bridges: Map<string, YukaBridge>;

  constructor() {
    this.entityManager = new YUKA.EntityManager();
    this.time = new YUKA.Time();
    this.bridges = new Map();
    
    console.log('[Yuka] EntityManager initialized');
  }

  createVehicle(ecsEntity: Entity): YukaBridge {
    if (!ecsEntity.movement) {
      throw new Error('Entity must have movement component');
    }

    const vehicle = new YUKA.Vehicle();
    
    // Configure from ECS movement data
    vehicle.position.set(
      ecsEntity.movement.position[0],
      ecsEntity.movement.position[1],
      ecsEntity.movement.position[2]
    );
    
    vehicle.maxSpeed = ecsEntity.movement.runSpeed;
    vehicle.mass = ecsEntity.movement.mass;
    vehicle.maxForce = 10; // Tunable
    
    // Create state machine
    const stateMachine = new YUKA.StateMachine(vehicle);
    
    const bridge: YukaBridge = {
      ecsEntityId: ecsEntity.id,
      yukaVehicle: vehicle,
      stateMachine
    };
    
    this.bridges.set(ecsEntity.id, bridge);
    this.entityManager.add(vehicle);
    
    console.log(`[Yuka] Created vehicle for entity ${ecsEntity.id}`);
    
    return bridge;
  }

  removeVehicle(entityId: string) {
    const bridge = this.bridges.get(entityId);
    if (bridge) {
      this.entityManager.remove(bridge.yukaVehicle);
      this.bridges.delete(entityId);
    }
  }

  getBridge(entityId: string): YukaBridge | undefined {
    return this.bridges.get(entityId);
  }

  update(): number {
    const delta = this.time.update().getDelta();
    this.entityManager.update(delta);
    return delta;
  }

  getEntityManager(): YUKA.EntityManager {
    return this.entityManager;
  }
}

export const yukaManager = new YukaManager();
