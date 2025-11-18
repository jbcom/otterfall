import { useEffect, useRef } from "react";
import nipplejs from "nipplejs";
import { useControlsStore } from "@/stores/useControlsStore";

export function VirtualJoysticks() {
  const moveContainerRef = useRef<HTMLDivElement>(null);
  const lookContainerRef = useRef<HTMLDivElement>(null);
  const { setMovement, setCamera, resetMovement, resetCamera } = useControlsStore();

  useEffect(() => {
    if (!moveContainerRef.current || !lookContainerRef.current) return;

    const moveManager = nipplejs.create({
      zone: moveContainerRef.current,
      mode: "static",
      position: { right: "15%", bottom: "15%" },
      color: "rgba(100, 150, 200, 0.7)",
      size: 120,
      threshold: 0.1,
    });

    const lookManager = nipplejs.create({
      zone: lookContainerRef.current,
      mode: "static",
      position: { left: "15%", bottom: "15%" },
      color: "rgba(200, 150, 100, 0.7)",
      size: 120,
      threshold: 0.1,
    });

    moveManager.on("move", (evt, data) => {
      const clampedDistance = Math.min(data.distance, 60) / 60;
      const forward = data.vector.y * clampedDistance;
      const right = data.vector.x * clampedDistance;
      setMovement(right, forward);
    });

    moveManager.on("end", () => {
      resetMovement();
    });

    lookManager.on("move", (evt, data) => {
      const clampedDistance = Math.min(data.distance, 60) / 60;
      const deltaX = data.vector.x * clampedDistance * 0.8;
      const deltaY = data.vector.y * clampedDistance * 0.8;
      setCamera(deltaX, deltaY);
    });

    lookManager.on("end", () => {
      resetCamera();
    });

    return () => {
      moveManager.destroy();
      lookManager.destroy();
    };
  }, [setMovement, setCamera, resetMovement, resetCamera]);

  return (
    <>
      <div
        ref={moveContainerRef}
        style={{
          position: "fixed",
          bottom: 0,
          right: 0,
          width: "50%",
          height: "40%",
          zIndex: 1000,
          pointerEvents: "auto",
        }}
      />
      <div
        ref={lookContainerRef}
        style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          width: "50%",
          height: "40%",
          zIndex: 1000,
          pointerEvents: "auto",
        }}
      />
    </>
  );
}
