
# Shader Development Guidelines (GLSL)

## Naming Conventions (MANDATORY)

```glsl
// Uniforms - Global parameters
uniform float u_time;
uniform vec2 u_resolution;
uniform sampler2D u_texture;

// Attributes - Per-vertex data
attribute vec3 a_position;
attribute vec2 a_uv;

// Varyings - Vertex → Fragment interpolation
varying vec2 v_uv;
varying vec3 v_worldPosition;

// Constants - Uppercase
const float PI = 3.14159265359;
const float MAX_DISTANCE = 1000.0;
```

## Mobile Shader Optimization

### Precision Qualifiers (Critical for Mobile)
```glsl
// Fragment shader header
precision mediump float; // Default for mobile

// High precision only when necessary
uniform highp sampler2D u_texture;
varying highp vec3 v_position; // If needed for calculations

// Low precision for colors, normals
varying lowp vec3 v_normal;
varying lowp vec4 v_color;
```

### Branch Avoidance
```glsl
// Bad - Branching kills performance on mobile
float result;
if (value > 0.5) {
  result = complexCalculation(value);
} else {
  result = simpleCalculation(value);
}

// Good - Use step() or mix()
float t = step(0.5, value); // 0.0 or 1.0
float result = mix(
  simpleCalculation(value),
  complexCalculation(value),
  t
);
```

## Water Shader Pattern (Gerstner Waves)

```glsl
// Vertex Shader
uniform float u_time;
uniform vec4 u_waves[4]; // [amplitude, wavelength, speed, direction]

vec3 gerstnerWave(vec3 pos, vec4 wave) {
  float k = 2.0 * PI / wave.y; // Wavelength → frequency
  float c = sqrt(9.8 / k); // Wave speed
  vec2 d = normalize(wave.zw); // Direction
  float f = k * (dot(d, pos.xz) - c * u_time);
  
  return vec3(
    d.x * wave.x * cos(f),
    wave.x * sin(f),
    d.y * wave.x * cos(f)
  );
}

void main() {
  vec3 pos = position;
  
  // Sum multiple waves
  pos += gerstnerWave(position, u_waves[0]);
  pos += gerstnerWave(position, u_waves[1]);
  pos += gerstnerWave(position, u_waves[2]);
  pos += gerstnerWave(position, u_waves[3]);
  
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  v_worldPosition = pos;
}
```

## SDF (Signed Distance Field) Patterns

```glsl
// Basic SDF shapes
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// SDF operations
float opUnion(float d1, float d2) {
  return min(d1, d2);
}

float opSubtraction(float d1, float d2) {
  return max(-d1, d2);
}

float opIntersection(float d1, float d2) {
  return max(d1, d2);
}

// Smooth union (organic blending)
float opSmoothUnion(float d1, float d2, float k) {
  float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
  return mix(d2, d1, h) - k * h * (1.0 - h);
}
```

## Noise Functions (Include from glsl-noise)

```glsl
// Import via vite-plugin-glsl
#pragma glslify: snoise3 = require('glsl-noise/simplex/3d')
#pragma glslify: cnoise3 = require('glsl-noise/classic/3d')

// Fractal Brownian Motion (terrain)
float fbm(vec3 p) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  
  for (int i = 0; i < 4; i++) {
    value += amplitude * snoise3(p * frequency);
    frequency *= 2.0;
    amplitude *= 0.5;
  }
  
  return value;
}
```

## Caustics Shader (Water Refraction)

```glsl
// Fragment shader
uniform sampler2D u_causticsTexture;
uniform float u_time;

void main() {
  // Distort UVs with animated noise
  vec2 uv1 = v_uv + vec2(u_time * 0.1, u_time * 0.05);
  vec2 uv2 = v_uv - vec2(u_time * 0.08, u_time * 0.12);
  
  float caustic1 = texture2D(u_causticsTexture, uv1).r;
  float caustic2 = texture2D(u_causticsTexture, uv2).r;
  
  // Combine for organic movement
  float caustics = min(caustic1, caustic2);
  
  // Apply to base color
  vec3 color = v_baseColor + caustics * 0.3;
  gl_FragColor = vec4(color, 1.0);
}
```

## Depth-Based Color (Water Clarity)

```glsl
uniform sampler2D u_depthTexture;
uniform vec3 u_shallowColor;
uniform vec3 u_deepColor;
uniform float u_depthFalloff;

void main() {
  // Read depth from depth buffer
  float depth = texture2D(u_depthTexture, gl_FragCoord.xy / u_resolution).r;
  
  // Convert to world space depth
  float waterDepth = linearizeDepth(depth);
  
  // Mix colors based on depth
  float depthFactor = 1.0 - exp(-waterDepth * u_depthFalloff);
  vec3 color = mix(u_shallowColor, u_deepColor, depthFactor);
  
  gl_FragColor = vec4(color, 1.0);
}
```

## Shader Integration with R3F

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';
import vertexShader from './shaders/water.vert';
import fragmentShader from './shaders/water.frag';

const WaterMaterial = shaderMaterial(
  {
    u_time: 0,
    u_waves: [
      [0.05, 2.0, 1.0, 1.0, 0.0],
      [0.03, 1.5, 0.8, 0.7, 0.7],
    ],
  },
  vertexShader,
  fragmentShader
);

extend({ WaterMaterial });

// Usage
function Water() {
  const ref = useRef();
  
  useFrame((state) => {
    ref.current.u_time = state.clock.elapsedTime;
  });
  
  return (
    <mesh>
      <planeGeometry args={[100, 100, 128, 128]} />
      <waterMaterial ref={ref} />
    </mesh>
  );
}
```

## Common Pitfalls

### ❌ Expensive Operations in Fragment Shader
```glsl
// Bad - sqrt/sin/cos every pixel!
for (int i = 0; i < 100; i++) {
  color += sin(i * 0.1) * texture2D(u_tex, uv);
}

// Good - Pre-calculate in vertex or CPU
uniform float u_precomputedValues[100];
```

### ❌ Texture Reads in Loops
```glsl
// Bad
for (int i = 0; i < 8; i++) {
  color += texture2D(u_texture, uv + offsets[i]);
}

// Better - Unroll loop manually
color += texture2D(u_texture, uv + offsets[0]);
color += texture2D(u_texture, uv + offsets[1]);
// ... etc (compiler can optimize)
```

## Debugging Shaders

```glsl
// Visualize UVs
gl_FragColor = vec4(v_uv, 0.0, 1.0);

// Visualize normals
gl_FragColor = vec4(v_normal * 0.5 + 0.5, 1.0);

// Visualize depth
gl_FragColor = vec4(vec3(depth), 1.0);
```
