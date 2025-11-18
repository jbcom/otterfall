import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface AdvancedWaterProps {
  position?: [number, number, number];
  size?: [number, number];
}

export function AdvancedWater({ position = [0, 0, 0], size = [100, 100] }: AdvancedWaterProps) {
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
          uWaterColor: { value: new THREE.Color(0x2a5a8a) },
          uDeepWaterColor: { value: new THREE.Color(0x1a3a5a) },
          uFoamColor: { value: new THREE.Color(0x8ab4d4) },
          uCausticIntensity: { value: 0.4 },
        },
        vertexShader: `
          uniform float uTime;
          varying vec2 vUv;
          varying vec3 vPosition;
          varying float vElevation;
          
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
          
          float fbm(vec2 p) {
            float value = 0.0;
            float amplitude = 0.5;
            float frequency = 1.0;
            
            for (int i = 0; i < 4; i++) {
              value += amplitude * noise(p * frequency);
              amplitude *= 0.5;
              frequency *= 2.0;
            }
            
            return value;
          }
          
          void main() {
            vUv = uv;
            vPosition = position;
            
            vec3 pos = position;
            
            float wave1 = sin(pos.x * 0.4 + uTime * 0.8) * 0.15;
            float wave2 = sin(pos.y * 0.3 + uTime * 1.2) * 0.12;
            float wave3 = sin((pos.x + pos.y) * 0.2 + uTime * 0.6) * 0.1;
            
            float noiseValue = fbm(vec2(pos.x * 0.1, pos.y * 0.1) + uTime * 0.05);
            
            pos.z += wave1 + wave2 + wave3 + noiseValue * 0.1;
            
            vElevation = pos.z;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
          }
        `,
        fragmentShader: `
          uniform float uTime;
          uniform vec3 uWaterColor;
          uniform vec3 uDeepWaterColor;
          uniform vec3 uFoamColor;
          uniform float uCausticIntensity;
          varying vec2 vUv;
          varying vec3 vPosition;
          varying float vElevation;
          
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
          
          float caustic(vec2 uv, float time) {
            vec2 p = uv * 10.0;
            
            float c1 = noise(p + time * 0.3);
            float c2 = noise(p * 1.5 - time * 0.2);
            float c3 = noise(p * 2.0 + time * 0.4);
            
            return (c1 + c2 + c3) / 3.0;
          }
          
          void main() {
            vec2 causticUV = vUv + vec2(sin(uTime * 0.5) * 0.1, cos(uTime * 0.3) * 0.1);
            float causticPattern = caustic(causticUV, uTime);
            causticPattern = pow(causticPattern, 2.0) * uCausticIntensity;
            
            float depthFactor = smoothstep(-0.1, 0.1, vElevation);
            vec3 waterColor = mix(uDeepWaterColor, uWaterColor, depthFactor);
            
            vec3 finalColor = waterColor + vec3(causticPattern);
            
            if (vElevation > 0.08) {
              finalColor = mix(finalColor, uFoamColor, smoothstep(0.08, 0.12, vElevation));
            }
            
            float fresnel = pow(1.0 - abs(dot(normalize(vPosition), vec3(0.0, 0.0, 1.0))), 2.0);
            finalColor += vec3(fresnel * 0.1);
            
            gl_FragColor = vec4(finalColor, 0.75);
          }
        `,
        transparent: true,
        side: THREE.DoubleSide,
      }),
    []
  );

  return (
    <mesh
      ref={waterRef}
      position={position}
      rotation={[-Math.PI / 2, 0, 0]}
      receiveShadow
    >
      <planeGeometry args={[size[0], size[1], 64, 64]} />
      <primitive object={waterMaterial} />
    </mesh>
  );
}
