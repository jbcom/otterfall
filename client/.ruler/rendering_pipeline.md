
# Rendering Pipeline Guidelines

## Render Pass Order (MANDATORY)

1. **SDF Sky/Fog** - Raymarched atmosphere
2. **Terrain/Water** - Base environment geometry
3. **GLB Actors** - Animated creatures/props
4. **SDF Effects** - Caustics, fog volumes, fur shells
5. **Post-processing** - Bloom, DoF, SSAO, color grading

## Performance Budget (Mobile Target: 60fps)

- Total draw calls: < 100
- Vertex count: < 500k per frame
- Texture memory: < 200MB
- Shader complexity: < 200 instructions per pixel

## Integration with ECS

Rendering systems query ECS world for:
- Transform components (position, rotation, scale)
- Mesh components (geometry, material refs)
- Animation components (current clip, time)

See [React Three Fiber Guidelines](../../.ruler/react_three_fiber.md) for R3F patterns.
See [Shader Guidelines](../../.ruler/shaders.md) for GLSL optimization.
