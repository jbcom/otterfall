import { useRef, useEffect } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { useRivermarsh } from "@/lib/stores/useRivermarsh";
import * as THREE from "three";

interface PlayerProps {
  mobileInput: {
    moveX: number;
    moveY: number;
    lookX: number;
    lookY: number;
    interact: boolean;
    attack: boolean;
    jump: boolean;
  };
}

export function Player({ mobileInput }: PlayerProps) {
  const { camera } = useThree();
  const playerRef = useRef<THREE.Mesh>(null);
  const velocityRef = useRef(new THREE.Vector3());
  const { updatePlayerPosition, updatePlayerRotation, player, isPaused, restoreStamina, useStamina, npcs, startDialogue, damageNPC } = useRivermarsh();

  const speed = 5;
  const sprintSpeed = 8;
  const jumpForce = 8;
  const gravity = -20;
  const groundY = 1;

  const rotationRef = useRef({ x: 0, y: 0 });
  const interactCooldownRef = useRef(0);
  const attackCooldownRef = useRef(0);
  const prevInteractRef = useRef(false);
  const prevAttackRef = useRef(false);

  useEffect(() => {
    rotationRef.current = { x: player.rotation[0], y: player.rotation[1] };
  }, [player.rotation]);

  useEffect(() => {
    console.log("Player component mounted - keyboard controls active");
  }, []);

  useFrame((state, delta) => {
    if (!playerRef.current || isPaused) return;
    
    const moveForward = mobileInput.moveY;
    const moveRight = mobileInput.moveX;

    const isSprinting = mobileInput.moveY > 0 && player.stats.stamina > 0;
    const currentSpeed = isSprinting ? sprintSpeed : speed;

    if (isSprinting) {
      useStamina(delta * 10);
    } else {
      restoreStamina(delta * 5);
    }

    rotationRef.current.y -= mobileInput.lookX * delta * 2;
    rotationRef.current.x -= mobileInput.lookY * delta * 2;
    rotationRef.current.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, rotationRef.current.x));

    updatePlayerRotation([rotationRef.current.x, rotationRef.current.y]);

    const forward = new THREE.Vector3(
      Math.sin(rotationRef.current.y),
      0,
      Math.cos(rotationRef.current.y)
    );
    const right = new THREE.Vector3().crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();

    const movement = new THREE.Vector3();
    movement.addScaledVector(forward, moveForward);
    movement.addScaledVector(right, moveRight);
    
    if (movement.length() > 0) {
      movement.normalize();
    }

    velocityRef.current.x = movement.x * currentSpeed;
    velocityRef.current.z = movement.z * currentSpeed;

    if (mobileInput.jump && Math.abs(playerRef.current.position.y - groundY) < 0.1 && player.stats.stamina > 20) {
      velocityRef.current.y = jumpForce;
      useStamina(20);
      console.log("Jump!");
    }

    interactCooldownRef.current = Math.max(0, interactCooldownRef.current - delta);
    attackCooldownRef.current = Math.max(0, attackCooldownRef.current - delta);

    if (mobileInput.interact && !prevInteractRef.current && interactCooldownRef.current === 0) {
      const playerPos = new THREE.Vector3(...player.position);
      const interactRange = 3;
      
      const nearbyNPC = npcs.find(npc => {
        const npcPos = new THREE.Vector3(...npc.position);
        const distance = playerPos.distanceTo(npcPos);
        return distance < interactRange && (npc.type === "friendly" || npc.type === "quest_giver" || npc.type === "merchant");
      });

      if (nearbyNPC && nearbyNPC.dialogue) {
        console.log(`Interacting with ${nearbyNPC.name}`);
        startDialogue(nearbyNPC.id, nearbyNPC.name, nearbyNPC.dialogue);
        interactCooldownRef.current = 0.5;
      }
    }
    prevInteractRef.current = mobileInput.interact;

    if (mobileInput.attack && !prevAttackRef.current && attackCooldownRef.current === 0 && player.stats.stamina > 15) {
      const playerPos = new THREE.Vector3(...player.position);
      const attackRange = 2.5;
      
      const targetNPC = npcs.find(npc => {
        const npcPos = new THREE.Vector3(...npc.position);
        const distance = playerPos.distanceTo(npcPos);
        return distance < attackRange && npc.type === "hostile";
      });

      if (targetNPC) {
        const baseDamage = 10;
        const weaponBonus = player.equipment.weapon?.stats.attack || 0;
        const totalDamage = baseDamage + weaponBonus;
        
        console.log(`Attacking ${targetNPC.name} for ${totalDamage} damage!`);
        damageNPC(targetNPC.id, totalDamage);
        useStamina(15);
        attackCooldownRef.current = 0.6;
      } else {
        console.log("Attack missed - no enemy in range");
      }
    }
    prevAttackRef.current = mobileInput.attack;

    velocityRef.current.y += gravity * delta;

    const newPosition = playerRef.current.position.clone();
    newPosition.add(velocityRef.current.clone().multiplyScalar(delta));

    if (newPosition.y <= groundY) {
      newPosition.y = groundY;
      velocityRef.current.y = 0;
    }

    playerRef.current.position.copy(newPosition);
    updatePlayerPosition([newPosition.x, newPosition.y, newPosition.z]);

    camera.position.set(
      newPosition.x,
      newPosition.y + 0.5,
      newPosition.z
    );
    
    camera.rotation.set(rotationRef.current.x, rotationRef.current.y, 0);
  });

  return (
    <mesh ref={playerRef} position={player.position} visible={false}>
      <boxGeometry args={[0.5, 1, 0.5]} />
      <meshStandardMaterial color="#8B4513" />
    </mesh>
  );
}
