import { useEffect, useRef } from "react";
import nipplejs from "nipplejs";

interface VirtualJoysticksProps {
  onMove: (x: number, y: number) => void;
  onLook: (x: number, y: number) => void;
}

export function VirtualJoysticks({ onMove, onLook }: VirtualJoysticksProps) {
  const moveContainerRef = useRef<HTMLDivElement>(null);
  const lookContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!moveContainerRef.current || !lookContainerRef.current) return;

    const moveManager = nipplejs.create({
      zone: moveContainerRef.current,
      mode: "static",
      position: { left: "15%", bottom: "15%" },
      color: "rgba(100, 150, 200, 0.5)",
      size: 120,
    });

    const lookManager = nipplejs.create({
      zone: lookContainerRef.current,
      mode: "static",
      position: { right: "15%", bottom: "15%" },
      color: "rgba(200, 150, 100, 0.5)",
      size: 120,
    });

    moveManager.on("move", (evt, data) => {
      const forward = data.vector.y;
      const right = data.vector.x;
      onMove(right, forward);
    });

    moveManager.on("end", () => {
      onMove(0, 0);
    });

    lookManager.on("move", (evt, data) => {
      const deltaX = data.vector.x * 0.5;
      const deltaY = data.vector.y * 0.5;
      onLook(deltaX, deltaY);
    });

    lookManager.on("end", () => {
      onLook(0, 0);
    });

    return () => {
      moveManager.destroy();
      lookManager.destroy();
    };
  }, [onMove, onLook]);

  return (
    <>
      <div
        ref={moveContainerRef}
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
      <div
        ref={lookContainerRef}
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
    </>
  );
}
