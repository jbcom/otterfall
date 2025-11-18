import { useEffect } from "react";
import { useKeyboardControls } from "@react-three/drei";
import { useControlsStore } from "@/stores/useControlsStore";

enum Controls {
  forward = "forward",
  back = "back",
  left = "left",
  right = "right",
  jump = "jump",
  interact = "interact",
  attack = "attack",
}

export function DesktopKeyboardInput() {
  const [, getKeys] = useKeyboardControls<Controls>();
  const { setMovement, setAction } = useControlsStore();

  useEffect(() => {
    let rafId: number;

    const updateInput = () => {
      const keys = getKeys();
      
      const moveX = (keys.right ? 1 : 0) - (keys.left ? 1 : 0);
      const moveY = (keys.forward ? 1 : 0) - (keys.back ? 1 : 0);
      
      setMovement(moveX, moveY);
      setAction('jump', keys.jump);
      setAction('interact', keys.interact);
      setAction('attack', keys.attack);
      
      rafId = requestAnimationFrame(updateInput);
    };

    rafId = requestAnimationFrame(updateInput);

    return () => {
      cancelAnimationFrame(rafId);
      setMovement(0, 0);
      setAction('jump', false);
      setAction('interact', false);
      setAction('attack', false);
    };
  }, [getKeys, setMovement, setAction]);

  return null;
}
