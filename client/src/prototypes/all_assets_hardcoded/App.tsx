import { Canvas } from "@react-three/fiber";
import { KeyboardControls, Sky } from "@react-three/drei";
import { Player } from "@/components/Player";
import { DioramaCamera } from "@/components/DioramaCamera";
import { GyroscopeCamera } from "@/components/GyroscopeCamera";
import { MarshlandTerrain } from "@/components/MarshlandTerrain";
import { NPCManager } from "@/components/OtterNPC";
import { VirtualJoysticks } from "@/components/VirtualJoysticks";
import { MobileActionButtons } from "@/components/MobileActionButtons";
import { DesktopKeyboardInput } from "@/components/DesktopKeyboardInput";
import { GameUI } from "@/components/GameUI";
import { SoundManager } from "@/components/SoundManager";
import { EffectComposer, Bloom, DepthOfField } from "@react-three/postprocessing";
import { useIsMobile } from "@/hooks/use-is-mobile";
import { Button } from "@mui/material";

enum Controls {
  forward = "forward",
  back = "back",
  left = "left",
  right = "right",
  jump = "jump",
  interact = "interact",
  attack = "attack",
}

interface AllAssetsHardcodedProps {
  onExit?: () => void;
}

function AllAssetsHardcoded({ onExit }: AllAssetsHardcodedProps) {
  const isMobile = useIsMobile();

  const keyMap = [
    { name: Controls.forward, keys: ["ArrowUp", "KeyW"] },
    { name: Controls.back, keys: ["ArrowDown", "KeyS"] },
    { name: Controls.left, keys: ["ArrowLeft", "KeyA"] },
    { name: Controls.right, keys: ["ArrowRight", "KeyD"] },
    { name: Controls.jump, keys: ["Space"] },
    { name: Controls.interact, keys: ["KeyE"] },
    { name: Controls.attack, keys: ["KeyF"] },
  ];

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative", overflow: "hidden" }}>
      {onExit && (
        <Button
          variant="contained"
          onClick={onExit}
          sx={{
            position: "absolute",
            top: 16,
            left: 16,
            zIndex: 1000,
          }}
        >
          Exit Prototype
        </Button>
      )}
      <KeyboardControls map={keyMap}>
        <Canvas
          shadows
          camera={{
            position: [0, 15, 15],
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
          
          <Sky
            distance={450000}
            sunPosition={[100, 20, 100]}
            inclination={0.6}
            azimuth={0.25}
          />

          <ambientLight intensity={0.5} />
          <directionalLight
            position={[50, 50, 25]}
            intensity={1}
            castShadow
            shadow-mapSize-width={2048}
            shadow-mapSize-height={2048}
            shadow-camera-far={200}
            shadow-camera-left={-50}
            shadow-camera-right={50}
            shadow-camera-top={50}
            shadow-camera-bottom={-50}
          />

          <fog attach="fog" args={["#7ab8d4", 30, 120]} />

          {!isMobile && <DesktopKeyboardInput />}
          {isMobile ? <GyroscopeCamera /> : <DioramaCamera />}
          <Player />
          <MarshlandTerrain />
          <NPCManager />

          <EffectComposer multisampling={8}>
            <Bloom
              intensity={0.6}
              luminanceThreshold={0.8}
              luminanceSmoothing={0.95}
              mipmapBlur
            />
            <DepthOfField
              focusDistance={0.015}
              focalLength={0.08}
              bokehScale={2.5}
            />
          </EffectComposer>
        </Canvas>

        <GameUI />
        <SoundManager />
        
        {isMobile && (
          <>
            <VirtualJoysticks />
            <MobileActionButtons />
          </>
        )}
      </KeyboardControls>
    </div>
  );
}

export default AllAssetsHardcoded;
