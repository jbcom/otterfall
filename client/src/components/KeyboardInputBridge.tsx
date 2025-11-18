import { useEffect } from "react";
import { useKeyboardControls } from "@react-three/drei";

enum Controls {
  forward = "forward",
  back = "back",
  left = "left",
  right = "right",
  jump = "jump",
  interact = "interact",
  attack = "attack",
}

interface KeyboardInputBridgeProps {
  onInput: (input: { moveX: number; moveY: number; interact: boolean; attack: boolean; jump: boolean }) => void;
}

export function KeyboardInputBridge({ onInput }: KeyboardInputBridgeProps) {
  const [subscribe, getKeys] = useKeyboardControls<Controls>();

  useEffect(() => {
    const updateInput = () => {
      const keys = getKeys();
      
      let moveX = 0;
      let moveY = 0;
      
      if (keys.forward) moveY += 1;
      if (keys.back) moveY -= 1;
      if (keys.right) moveX += 1;
      if (keys.left) moveX -= 1;
      
      onInput({
        moveX,
        moveY,
        interact: keys.interact,
        attack: keys.attack,
        jump: keys.jump,
      });
    };

    const interval = setInterval(updateInput, 16);
    return () => clearInterval(interval);
  }, [getKeys, onInput]);

  return null;
}
