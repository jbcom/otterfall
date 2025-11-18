import { useRef, useMemo } from "react";
import { useFrame, useLoader } from "@react-three/fiber";
import * as THREE from "three";
import { TextureLoader } from "three";

export function MarshlandTerrain() {
  const grassTextureUrl = "/textures/grass.png";
  const grassTexture = useLoader(TextureLoader, grassTextureUrl);
  
  grassTexture.wrapS = grassTexture.wrapT = THREE.RepeatWrapping;
  grassTexture.repeat.set(20, 20);

  return (
    <>
      <Ground texture={grassTexture} />
      <Water />
      <InstancedGrass />
      <InstancedReeds />
      <Trees />
    </>
  );
}

function Ground({ texture }: { texture: THREE.Texture }) {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
      <planeGeometry args={[200, 200, 50, 50]} />
      <meshStandardMaterial map={texture} color="#4a7c3a" />
    </mesh>
  );
}

function Water() {
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
          uColor: { value: new THREE.Color(0x4a90e2) },
        },
        vertexShader: `
          uniform float uTime;
          varying vec2 vUv;
          varying float vElevation;
          
          void main() {
            vUv = uv;
            vec3 pos = position;
            
            float wave1 = sin(pos.x * 0.5 + uTime) * 0.1;
            float wave2 = sin(pos.y * 0.3 + uTime * 1.5) * 0.1;
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
            vec3 color = uColor + vElevation * 0.2;
            gl_FragColor = vec4(color, 0.7);
          }
        `,
        transparent: true,
      }),
    []
  );

  const waterPositions = useMemo(() => {
    return [
      [30, 0.05, 30],
      [-40, 0.05, 20],
      [50, 0.05, -30],
      [-30, 0.05, -40],
    ];
  }, []);

  return (
    <>
      {waterPositions.map((pos, i) => (
        <mesh
          key={i}
          ref={i === 0 ? waterRef : null}
          position={pos as [number, number, number]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[20, 20, 10, 10]} />
          <primitive object={waterMaterial.clone()} />
        </mesh>
      ))}
    </>
  );
}

function InstancedGrass() {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const count = 500;

  const positions = useMemo(() => {
    const pos = [];
    for (let i = 0; i < count; i++) {
      const x = (Math.random() - 0.5) * 180;
      const z = (Math.random() - 0.5) * 180;
      const y = 0.3;
      const scale = 0.3 + Math.random() * 0.4;
      const rotation = Math.random() * Math.PI * 2;
      pos.push({ x, y, z, scale, rotation });
    }
    return pos;
  }, []);

  useMemo(() => {
    if (!meshRef.current) return;

    const dummy = new THREE.Object3D();
    positions.forEach((pos, i) => {
      dummy.position.set(pos.x, pos.y, pos.z);
      dummy.rotation.y = pos.rotation;
      dummy.scale.set(pos.scale, pos.scale, pos.scale);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [positions]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]} castShadow>
      <coneGeometry args={[0.1, 0.8, 3]} />
      <meshStandardMaterial color="#3d5c2a" />
    </instancedMesh>
  );
}

function InstancedReeds() {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const count = 300;

  const positions = useMemo(() => {
    const waterPositions = [
      [30, 0, 30],
      [-40, 0, 20],
      [50, 0, -30],
      [-30, 0, -40],
    ];

    const pos: Array<{ x: number; y: number; z: number; scale: number; rotation: number }> = [];
    waterPositions.forEach((water) => {
      for (let i = 0; i < count / 4; i++) {
        const angle = Math.random() * Math.PI * 2;
        const distance = 8 + Math.random() * 8;
        const x = water[0] + Math.cos(angle) * distance;
        const z = water[2] + Math.sin(angle) * distance;
        const y = 0.5;
        const scale = 0.5 + Math.random() * 0.5;
        const rotation = Math.random() * Math.PI * 2;
        pos.push({ x, y, z, scale, rotation });
      }
    });
    return pos;
  }, []);

  useMemo(() => {
    if (!meshRef.current) return;

    const dummy = new THREE.Object3D();
    positions.forEach((pos, i) => {
      dummy.position.set(pos.x, pos.y, pos.z);
      dummy.rotation.y = pos.rotation;
      dummy.scale.set(pos.scale * 0.3, pos.scale * 2, pos.scale * 0.3);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [positions]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]} castShadow>
      <cylinderGeometry args={[0.05, 0.08, 2, 6]} />
      <meshStandardMaterial color="#5a7c4a" />
    </instancedMesh>
  );
}

function Trees() {
  const treePositions = useMemo(() => {
    const positions = [];
    for (let i = 0; i < 30; i++) {
      const x = (Math.random() - 0.5) * 160;
      const z = (Math.random() - 0.5) * 160;
      
      if (Math.abs(x) < 20 && Math.abs(z) < 20) continue;
      
      positions.push([x, 0, z]);
    }
    return positions;
  }, []);

  return (
    <>
      {treePositions.map((pos, i) => (
        <group key={i} position={pos as [number, number, number]}>
          <mesh position={[0, 1.5, 0]} castShadow>
            <cylinderGeometry args={[0.3, 0.4, 3, 8]} />
            <meshStandardMaterial color="#3d2817" />
          </mesh>
          <mesh position={[0, 3.5, 0]} castShadow>
            <coneGeometry args={[1.5, 3, 8]} />
            <meshStandardMaterial color="#2d4a1e" />
          </mesh>
        </group>
      ))}
    </>
  );
}
