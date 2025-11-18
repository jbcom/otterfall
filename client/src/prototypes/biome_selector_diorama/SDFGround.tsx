import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { BiomeComponent } from '../../ecs/components/BiomeComponent';
import { WeatherComponent } from '../../ecs/components/WeatherComponent';
import { TimeOfDayComponent } from '../../ecs/components/TimeOfDayComponent';

interface SDFGroundProps {
  biome: BiomeComponent;
  weather: WeatherComponent;
  timeOfDay: TimeOfDayComponent;
}

export function SDFGround({ biome, weather, timeOfDay }: SDFGroundProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uBiomeColor: { value: new THREE.Color(biome.colorPalette.primary) },
      uSecondaryColor: { value: new THREE.Color(biome.colorPalette.secondary) },
      uFoliageColor: { value: new THREE.Color(biome.colorPalette.foliage) },
      uWeatherIntensity: { value: weather.intensity },
      uSunIntensity: { value: timeOfDay.sunIntensity },
      uAmbientLight: { value: timeOfDay.ambientLight },
      uMoisture: { value: biome.moisture },
      uRoughness: { value: biome.terrainRoughness },
    }),
    []
  );

  useFrame((state) => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.ShaderMaterial;
      material.uniforms.uTime.value = state.clock.elapsedTime;
      material.uniforms.uBiomeColor.value.set(biome.colorPalette.primary);
      material.uniforms.uSecondaryColor.value.set(biome.colorPalette.secondary);
      material.uniforms.uFoliageColor.value.set(biome.colorPalette.foliage);
      material.uniforms.uWeatherIntensity.value = weather.intensity;
      material.uniforms.uSunIntensity.value = timeOfDay.sunIntensity;
      material.uniforms.uAmbientLight.value = timeOfDay.ambientLight;
      material.uniforms.uMoisture.value = biome.moisture;
      material.uniforms.uRoughness.value = biome.terrainRoughness;
    }
  });

  const vertexShader = `
    varying vec2 vUv;
    varying vec3 vPosition;
    
    void main() {
      vUv = uv;
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;

  const fragmentShader = `
    uniform float uTime;
    uniform vec3 uBiomeColor;
    uniform vec3 uSecondaryColor;
    uniform vec3 uFoliageColor;
    uniform float uWeatherIntensity;
    uniform float uSunIntensity;
    uniform float uAmbientLight;
    uniform float uMoisture;
    uniform float uRoughness;
    
    varying vec2 vUv;
    varying vec3 vPosition;
    
    // Simple noise function
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }
    
    float noise(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      
      float a = hash(i);
      float b = hash(i + vec2(1.0, 0.0));
      float c = hash(i + vec2(0.0, 1.0));
      float d = hash(i + vec2(1.0, 1.0));
      
      return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
    }
    
    // SDF for ground plane
    float sdPlane(vec3 p) {
      return p.y;
    }
    
    void main() {
      // Create varied terrain using noise
      float n = noise(vUv * 10.0 + uTime * 0.1);
      float detail = noise(vUv * 50.0);
      
      // Mix colors based on biome properties
      vec3 baseColor = mix(uBiomeColor, uSecondaryColor, n);
      baseColor = mix(baseColor, uFoliageColor, detail * uMoisture);
      
      // Add roughness variation
      float roughnessNoise = noise(vUv * 20.0 + vec2(uTime * 0.05));
      baseColor = mix(baseColor, baseColor * 0.7, roughnessNoise * uRoughness);
      
      // Apply lighting
      float lighting = uAmbientLight + uSunIntensity * 0.5;
      vec3 litColor = baseColor * lighting;
      
      // Weather effects (darken in rain/fog)
      litColor = mix(litColor, litColor * 0.6, uWeatherIntensity * 0.5);
      
      gl_FragColor = vec4(litColor, 1.0);
    }
  `;

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
      <planeGeometry args={[100, 100, 1, 1]} />
      <shaderMaterial
        uniforms={uniforms}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}
