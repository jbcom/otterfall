import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Button } from "@mui/material";
import { SDFGround } from "./SDFGround";
import { SDFSky } from "./SDFSky";
import { BiomeControls } from "./BiomeControls";
import { useBiomeECS } from "./useBiomeECS";

interface BiomeSelectorDioramaProps {
  onExit?: () => void;
}

function BiomeSelectorDiorama({ onExit }: BiomeSelectorDioramaProps) {
  const { state, setBiome, setWeather, setTimeOfDay, getEntity } = useBiomeECS();
  
  const entity = getEntity();
  if (!entity || !entity.biome || !entity.weather || !entity.timeOfDay) {
    return <div>Loading ECS world...</div>;
  }

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative", overflow: "hidden" }}>
      {onExit && (
        <Button
          variant="contained"
          onClick={onExit}
          sx={{
            position: "absolute",
            top: 16,
            right: 16,
            zIndex: 1000,
          }}
        >
          Exit Prototype
        </Button>
      )}

      <BiomeControls
        biome={state.biome}
        weather={state.weather}
        timePhase={state.timePhase}
        timeOfDay={state.timeOfDay}
        onBiomeChange={setBiome}
        onWeatherChange={setWeather}
        onTimeChange={setTimeOfDay}
      />

      <Canvas
        camera={{
          position: [0, 20, 20],
          fov: 50,
          near: 0.1,
          far: 1000,
        }}
        gl={{
          antialias: true,
          powerPreference: "high-performance",
        }}
      >
        <color attach="background" args={["#87CEEB"]} />

        <ambientLight intensity={0.3} />
        <directionalLight
          position={[50, 50, 25]}
          intensity={0.8}
          castShadow
        />

        <OrbitControls
          target={[0, 0, 0]}
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minPolarAngle={Math.PI / 6}
          maxPolarAngle={Math.PI / 2.5}
        />

        <SDFSky timeOfDay={entity.timeOfDay} weather={entity.weather} />
        <SDFGround biome={entity.biome} weather={entity.weather} timeOfDay={entity.timeOfDay} />
      </Canvas>
    </div>
  );
}

export default BiomeSelectorDiorama;
