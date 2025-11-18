// TypeScript declarations for Yuka AI library
declare module 'yuka' {
  export class Vector3 {
    x: number;
    y: number;
    z: number;
    constructor(x?: number, y?: number, z?: number);
    set(x: number, y: number, z: number): this;
    copy(v: Vector3): this;
    toArray(): [number, number, number];
    distanceTo(v: Vector3): number;
    squaredDistanceTo(v: Vector3): number;
    applyMatrix4(m: Matrix4): this;
  }

  export class Matrix4 {
    elements: Float32Array;
    constructor();
    getInverse(m: Matrix4): this;
  }

  export class GameEntity {
    uuid: string;
    name: string;
    position: Vector3;
    rotation: Quaternion;
    scale: Vector3;
    worldMatrix: Matrix4;
    boundingRadius: number;
    manager: EntityManager | null;
    
    constructor();
    setRenderComponent(component: any, callback: (entity: GameEntity, component: any) => void): this;
    update(delta: number): this;
  }

  export class Vehicle extends GameEntity {
    velocity: Vector3;
    mass: number;
    maxSpeed: number;
    maxForce: number;
    steering: SteeringManager;
    target: Vector3 | null;
    
    constructor();
    rotateTo(target: Vector3, delta: number): boolean;
  }

  export class SteeringManager {
    add(behavior: SteeringBehavior): this;
    remove(behavior: SteeringBehavior): this;
    clear(): this;
  }

  export class SteeringBehavior {
    weight: number;
    active: boolean;
  }

  export class SeekBehavior extends SteeringBehavior {
    constructor(target: Vector3);
  }

  export class FleeBehavior extends SteeringBehavior {
    constructor(target: Vector3, panicDistance: number);
  }

  export class ArriveBehavior extends SteeringBehavior {
    constructor(target: Vector3, deceleration?: number);
  }

  export class PursuitBehavior extends SteeringBehavior {
    constructor(target: Vehicle);
  }

  export class EvadeBehavior extends SteeringBehavior {
    constructor(target: Vehicle, panicDistance: number);
  }

  export class WanderBehavior extends SteeringBehavior {
    radius: number;
    distance: number;
    jitter: number;
    constructor();
  }

  export class ObstacleAvoidanceBehavior extends SteeringBehavior {
    obstacles: GameEntity[];
    constructor(obstacles?: GameEntity[]);
  }

  export class FollowPathBehavior extends SteeringBehavior {
    constructor(path: Path, nextWaypointDistance?: number);
  }

  export class OffsetPursuitBehavior extends SteeringBehavior {
    constructor(leader: Vehicle, offset: Vector3);
  }

  export class CohesionBehavior extends SteeringBehavior {
    constructor(vehicles: Vehicle[]);
  }

  export class SeparationBehavior extends SteeringBehavior {
    constructor(vehicles: Vehicle[]);
  }

  export class AlignmentBehavior extends SteeringBehavior {
    constructor(vehicles: Vehicle[]);
  }

  export class Path {
    waypoints: Vector3[];
    constructor();
    add(waypoint: Vector3): this;
  }

  export class State {
    enter?(owner: any): void;
    execute?(owner: any): void;
    exit?(owner: any): void;
  }

  export class StateMachine {
    owner: any;
    currentState: State | null;
    
    constructor(owner?: any);
    add(name: string, state: State): this;
    changeTo(name: string): this;
    update(): this;
  }

  export class Goal {
    owner: any;
    status: number;
    
    static STATUS: {
      INACTIVE: number;
      ACTIVE: number;
      COMPLETED: number;
      FAILED: number;
    };
    
    constructor(owner: any);
    activate(): void;
    execute(): void;
    terminate(): void;
  }

  export class CompositeGoal extends Goal {
    subgoals: Goal[];
    
    addSubgoal(goal: Goal): this;
    clearSubgoals(): this;
    executeSubgoals(): number;
    replanIfFailed(): void;
  }

  export class EntityManager {
    entities: GameEntity[];
    
    constructor();
    add(entity: GameEntity): this;
    remove(entity: GameEntity): this;
    update(delta: number): this;
  }

  export class Time {
    constructor();
    update(): this;
    getDelta(): number;
  }

  export class Quaternion {
    x: number;
    y: number;
    z: number;
    w: number;
    
    constructor(x?: number, y?: number, z?: number, w?: number);
  }
}
