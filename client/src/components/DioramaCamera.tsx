import { useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { useRivermarsh } from "@/lib/stores/useRivermarsh";
import { useControlsStore } from "@/stores/useControlsStore";
import * as THREE from "three";

export function DioramaCamera() {
  const { camera } = useThree();
  const { player } = useRivermarsh();
  const cameraInput = useControlsStore((state) => state.camera);
  const setCameraAzimuth = useControlsStore((state) => state.setCameraAzimuth);
  
  const cameraOffset = useRef(new THREE.Vector3(0, 12, 12));
  const cameraRotation = useRef({ azimuth: 0, elevation: Math.PI / 6 });
  const targetPosition = useRef(new THREE.Vector3(...player.position));

  useFrame((state, delta) => {
    const playerPos = new THREE.Vector3(...player.position);
    
    targetPosition.current.lerp(playerPos, delta * 5);

    cameraRotation.current.azimuth -= cameraInput.x * delta * 2;
    cameraRotation.current.elevation = THREE.MathUtils.clamp(
      cameraRotation.current.elevation + cameraInput.y * delta,
      Math.PI / 12,
      Math.PI / 3
    );
    
    setCameraAzimuth(cameraRotation.current.azimuth);

    const distance = 15;
    const offsetX = distance * Math.sin(cameraRotation.current.azimuth) * Math.cos(cameraRotation.current.elevation);
    const offsetY = distance * Math.sin(cameraRotation.current.elevation);
    const offsetZ = distance * Math.cos(cameraRotation.current.azimuth) * Math.cos(cameraRotation.current.elevation);

    cameraOffset.current.set(offsetX, offsetY, offsetZ);

    const desiredPosition = targetPosition.current.clone().add(cameraOffset.current);
    camera.position.lerp(desiredPosition, delta * 8);

    camera.lookAt(targetPosition.current);
  });

  return null;
}
