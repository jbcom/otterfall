import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { DUNGEON_GENERATION_CONFIG, OTTER_DUNGEON_THEMES, DungeonBlock, DungeonBlockType } from "@/data/daggerfallDungeonReference";

interface DungeonRoom {
  x: number;
  z: number;
  width: number;
  depth: number;
  type: DungeonBlockType;
  connections: {
    north: boolean;
    south: boolean;
    east: boolean;
    west: boolean;
  };
}

interface ProceduralDungeonProps {
  theme: keyof typeof OTTER_DUNGEON_THEMES;
  seed: number;
  position?: [number, number, number];
}

function seededRandom(seed: number) {
  let value = seed;
  return () => {
    value = (value * 9301 + 49297) % 233280;
    return value / 233280;
  };
}

function generateDungeonLayout(seed: number, blockTypes: string[]): DungeonRoom[] {
  const random = seededRandom(seed);
  const rooms: DungeonRoom[] = [];
  const numRooms = Math.floor(random() * (DUNGEON_GENERATION_CONFIG.MAX_BLOCKS - DUNGEON_GENERATION_CONFIG.MIN_BLOCKS)) + DUNGEON_GENERATION_CONFIG.MIN_BLOCKS;

  const startRoom: DungeonRoom = {
    x: 0,
    z: 0,
    width: DUNGEON_GENERATION_CONFIG.BLOCK_SIZE,
    depth: DUNGEON_GENERATION_CONFIG.BLOCK_SIZE,
    type: 'start',
    connections: { north: false, south: false, east: false, west: false },
  };
  rooms.push(startRoom);

  for (let i = 1; i < numRooms; i++) {
    const parentRoom = rooms[Math.floor(random() * rooms.length)];
    const direction = Math.floor(random() * 4);
    
    let newX = parentRoom.x;
    let newZ = parentRoom.z;
    
    switch (direction) {
      case 0:
        newZ += DUNGEON_GENERATION_CONFIG.BLOCK_SIZE;
        parentRoom.connections.north = true;
        break;
      case 1:
        newZ -= DUNGEON_GENERATION_CONFIG.BLOCK_SIZE;
        parentRoom.connections.south = true;
        break;
      case 2:
        newX += DUNGEON_GENERATION_CONFIG.BLOCK_SIZE;
        parentRoom.connections.east = true;
        break;
      case 3:
        newX -= DUNGEON_GENERATION_CONFIG.BLOCK_SIZE;
        parentRoom.connections.west = true;
        break;
    }

    if (rooms.some(r => r.x === newX && r.z === newZ)) {
      continue;
    }

    const roomType = blockTypes[Math.floor(random() * blockTypes.length)] as DungeonBlockType;
    
    const newRoom: DungeonRoom = {
      x: newX,
      z: newZ,
      width: DUNGEON_GENERATION_CONFIG.BLOCK_SIZE,
      depth: DUNGEON_GENERATION_CONFIG.BLOCK_SIZE,
      type: roomType,
      connections: { north: false, south: false, east: false, west: false },
    };

    switch (direction) {
      case 0: newRoom.connections.south = true; break;
      case 1: newRoom.connections.north = true; break;
      case 2: newRoom.connections.west = true; break;
      case 3: newRoom.connections.east = true; break;
    }

    rooms.push(newRoom);
  }

  return rooms;
}

function DungeonWalls({ room }: { room: DungeonRoom }) {
  const wallHeight = 6;
  const wallThickness = 0.5;

  const wallColor = room.type === 'wet' ? '#2a4a5a' : room.type === 'mausoleum' ? '#4a3a3a' : '#5a5a4a';

  return (
    <group position={[room.x, wallHeight / 2, room.z]}>
      {!room.connections.north && (
        <mesh position={[0, 0, room.depth / 2]} castShadow receiveShadow>
          <boxGeometry args={[room.width, wallHeight, wallThickness]} />
          <meshStandardMaterial color={wallColor} />
        </mesh>
      )}
      {!room.connections.south && (
        <mesh position={[0, 0, -room.depth / 2]} castShadow receiveShadow>
          <boxGeometry args={[room.width, wallHeight, wallThickness]} />
          <meshStandardMaterial color={wallColor} />
        </mesh>
      )}
      {!room.connections.east && (
        <mesh position={[room.width / 2, 0, 0]} castShadow receiveShadow>
          <boxGeometry args={[wallThickness, wallHeight, room.depth]} />
          <meshStandardMaterial color={wallColor} />
        </mesh>
      )}
      {!room.connections.west && (
        <mesh position={[-room.width / 2, 0, 0]} castShadow receiveShadow>
          <boxGeometry args={[wallThickness, wallHeight, room.depth]} />
          <meshStandardMaterial color={wallColor} />
        </mesh>
      )}
    </group>
  );
}

function DungeonFloor({ room }: { room: DungeonRoom }) {
  const floorColor = room.type === 'wet' ? '#1a3a4a' : room.type === 'mausoleum' ? '#3a2a2a' : '#4a4a3a';
  
  return (
    <mesh position={[room.x, 0, room.z]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[room.width, room.depth]} />
      <meshStandardMaterial color={floorColor} />
    </mesh>
  );
}

function WaterEffect({ room }: { room: DungeonRoom }) {
  const waterRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (waterRef.current) {
      const time = state.clock.getElapsedTime();
      (waterRef.current.material as THREE.ShaderMaterial).uniforms.uTime.value = time;
    }
  });

  const waterMaterial = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uColor: { value: new THREE.Color(0x2a5a8a) },
        },
        vertexShader: `
          uniform float uTime;
          varying vec2 vUv;
          varying float vElevation;
          
          void main() {
            vUv = uv;
            vec3 pos = position;
            
            float wave1 = sin(pos.x * 0.3 + uTime * 0.5) * 0.05;
            float wave2 = sin(pos.y * 0.2 + uTime * 0.7) * 0.05;
            pos.z += wave1 + wave2;
            
            vElevation = pos.z;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
          }
        `,
        fragmentShader: `
          uniform vec3 uColor;
          varying vec2 vUv;
          varying float vElevation;
          
          void main() {
            vec3 color = uColor + vElevation * 0.3;
            gl_FragColor = vec4(color, 0.6);
          }
        `,
        transparent: true,
      }),
    []
  );

  if (room.type !== 'wet') return null;

  return (
    <mesh
      ref={waterRef}
      position={[room.x, 0.2, room.z]}
      rotation={[-Math.PI / 2, 0, 0]}
    >
      <planeGeometry args={[room.width * 0.9, room.depth * 0.9, 10, 10]} />
      <primitive object={waterMaterial} />
    </mesh>
  );
}

export function ProceduralDungeon({ theme, seed, position = [0, 0, 0] }: ProceduralDungeonProps) {
  const dungeonTheme = OTTER_DUNGEON_THEMES[theme];
  
  const rooms = useMemo(() => {
    return generateDungeonLayout(seed, [...dungeonTheme.blockTypes]);
  }, [seed, dungeonTheme.blockTypes]);

  return (
    <group position={position}>
      {rooms.map((room, index) => (
        <group key={index}>
          <DungeonFloor room={room} />
          <DungeonWalls room={room} />
          <WaterEffect room={room} />
        </group>
      ))}
      
      <ambientLight intensity={0.2} />
      <pointLight position={[0, 10, 0]} intensity={0.5} distance={50} castShadow />
    </group>
  );
}
