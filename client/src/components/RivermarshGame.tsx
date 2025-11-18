import { useState, useCallback } from "react";
import { Canvas } from "@react-three/fiber";
import { KeyboardControls, Sky } from "@react-three/drei";
import { Player } from "./Player";
import { MarshlandTerrain } from "./MarshlandTerrain";
import { NPCManager } from "./OtterNPC";
import { VirtualJoysticks } from "./VirtualJoysticks";
import { GameUI } from "./GameUI";
import { SoundManager } from "./SoundManager";
import { EffectComposer, Bloom, DepthOfField } from "@react-three/postprocessing";
import { useIsMobile } from "@/hooks/use-is-mobile";

enum Controls {
  forward = "forward",
  back = "back",
  left = "left",
  right = "right",
  jump = "jump",
  interact = "interact",
  attack = "attack",
}

export function RivermarshGame() {
  const isMobile = useIsMobile();
  
  const [mobileInput, setMobileInput] = useState({
    moveX: 0,
    moveY: 0,
    lookX: 0,
    lookY: 0,
  });

  const handleMove = useCallback((x: number, y: number) => {
    setMobileInput((prev) => ({ ...prev, moveX: x, moveY: y }));
  }, []);

  const handleLook = useCallback((x: number, y: number) => {
    setMobileInput((prev) => ({ ...prev, lookX: x, lookY: y }));
  }, []);

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
      <KeyboardControls map={keyMap}>
        <Canvas
          shadows
          camera={{
            position: [0, 2, 5],
            fov: 75,
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

          <fog attach="fog" args={["#87CEEB", 50, 150]} />

          <Player mobileInput={mobileInput} />
          <MarshlandTerrain />
          <NPCManager />

          <EffectComposer>
            <Bloom
              intensity={0.5}
              luminanceThreshold={0.9}
              luminanceSmoothing={0.9}
            />
            <DepthOfField
              focusDistance={0.02}
              focalLength={0.05}
              bokehScale={3}
            />
          </EffectComposer>
        </Canvas>

        <GameUI />
        <SoundManager />
        
        {isMobile && <VirtualJoysticks onMove={handleMove} onLook={handleLook} />}
      </KeyboardControls>
    </div>
  );
}
