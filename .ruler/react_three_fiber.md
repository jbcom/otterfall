
# React Three Fiber Development Guidelines

## Component Structure

### Scene Organization
```tsx
// Bad - Everything in one component
function Game() {
  return (
    <Canvas>
      <mesh>...</mesh>
      <mesh>...</mesh>
      <mesh>...</mesh>
      {/* 500 more lines */}
    </Canvas>
  );
}

// Good - Hierarchical composition
function Game() {
  return (
    <Canvas>
      <Scene />
      <Effects />
    </Canvas>
  );
}

function Scene() {
  return (
    <>
      <Environment />
      <Terrain />
      <Characters />
      <Props />
    </>
  );
}
```

## Performance Patterns

### Instancing (MANDATORY for >10 similar objects)
```tsx
import { Instance, Instances } from '@react-three/drei';

function Forest() {
  return (
    <Instances limit={1000} range={1000}>
      <treeGeometry />
      <meshStandardMaterial />
      {trees.map((pos, i) => (
        <Instance key={i} position={pos} />
      ))}
    </Instances>
  );
}
```

### LOD Implementation
```tsx
import { Detailed } from '@react-three/drei';

function Tree({ position }) {
  return (
    <Detailed distances={[0, 15, 30]}>
      <TreeHighPoly position={position} />
      <TreeMediumPoly position={position} />
      <TreeLowPoly position={position} />
    </Detailed>
  );
}
```

### Texture Loading
```tsx
import { useTexture } from '@react-three/drei';

// Good - Preload and cache
const TEXTURE_PATHS = {
  grass: '/textures/grass.png',
  sand: '/textures/sand.jpg',
} as const;

function Terrain() {
  const textures = useTexture(TEXTURE_PATHS);
  // textures.grass, textures.sand are now loaded
}
```

## Camera Setup

### Diorama Camera (Project Standard)
```tsx
import { PerspectiveCamera } from '@react-three/drei';

function DioramaCamera({ target }) {
  return (
    <PerspectiveCamera
      makeDefault
      position={[8, 5, 8]}
      fov={50}
      near={0.1}
      far={1000}
    />
  );
}
```

## Post-Processing Stack (MANDATORY ORDER)

```tsx
import { EffectComposer, Bloom, DepthOfField, SSAO } from '@react-three/postprocessing';

function Effects() {
  return (
    <EffectComposer>
      {/* 1. Bloom */}
      <Bloom luminanceThreshold={0.9} intensity={0.5} />
      
      {/* 2. Depth of Field */}
      <DepthOfField focusDistance={0} focalLength={0.02} bokehScale={2} />
      
      {/* 3. SSAO */}
      <SSAO samples={31} radius={5} intensity={40} />
      
      {/* 4. God Rays (custom) */}
      <GodRays />
      
      {/* 5. Color Grading (custom) */}
      <ColorGrading />
    </EffectComposer>
  );
}
```

## State Management with R3F

### Frame Loop Integration
```tsx
import { useFrame } from '@react-three/fiber';

function AnimatedObject() {
  const ref = useRef();
  
  useFrame((state, delta) => {
    // Good - Use delta for frame-rate independence
    ref.current.rotation.y += delta * 0.5;
    
    // Bad - Frame-dependent
    // ref.current.rotation.y += 0.01;
  });
  
  return <mesh ref={ref} />;
}
```

### Zustand Integration
```tsx
import { useGameStore } from '@/lib/stores/useGame';

function Player() {
  const position = useGameStore(s => s.player.position);
  const updatePosition = useGameStore(s => s.updatePlayerPosition);
  
  useFrame(() => {
    // Update ECS/Zustand from frame loop
    updatePosition(ref.current.position);
  });
}
```

## Mobile Optimization

### Conditional Quality
```tsx
import { useIsMobile } from '@/hooks/use-is-mobile';

function Water() {
  const isMobile = useIsMobile();
  
  return (
    <mesh>
      <planeGeometry args={[100, 100, isMobile ? 32 : 128]} />
      <waterMaterial 
        reflections={!isMobile}
        refractions={!isMobile}
      />
    </mesh>
  );
}
```

### Texture Resolution
```tsx
// Auto-detect and downscale
const textureSize = isMobile ? 1024 : 2048;
```

## Common Pitfalls

### ❌ Don't create geometries/materials in render
```tsx
// Bad
function Box() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} /> {/* Created every frame! */}
      <meshStandardMaterial color="red" />
    </mesh>
  );
}

// Good
const boxGeometry = new THREE.BoxGeometry(1, 1, 1);
const redMaterial = new THREE.MeshStandardMaterial({ color: 'red' });

function Box() {
  return <mesh geometry={boxGeometry} material={redMaterial} />;
}
```

### ❌ Don't use `useEffect` for animations
```tsx
// Bad - Race conditions, cleanup issues
useEffect(() => {
  const interval = setInterval(() => {
    ref.current.rotation.y += 0.01;
  }, 16);
  return () => clearInterval(interval);
}, []);

// Good - Use useFrame
useFrame((state, delta) => {
  ref.current.rotation.y += delta * 0.5;
});
```

## Testing R3F Components

```tsx
import { render } from '@react-three/test-renderer';

describe('Player', () => {
  it('renders at correct position', async () => {
    const renderer = await render(<Player position={[1, 2, 3]} />);
    const mesh = renderer.scene.children[0];
    expect(mesh.position.toArray()).toEqual([1, 2, 3]);
  });
});
```
