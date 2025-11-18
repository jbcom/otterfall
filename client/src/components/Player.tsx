import { useRef, useEffect } from "react";
import { useFrame } from "@react-three/fiber";
import { useRivermarsh } from "@/lib/stores/useRivermarsh";
import { useControlsStore } from "@/stores/useControlsStore";
import * as THREE from "three";

export function Player() {
  const playerRef = useRef<THREE.Mesh>(null);
  const velocityRef = useRef(new THREE.Vector3());
  const { updatePlayerPosition, player, isPaused, restoreStamina, useStamina, npcs, startDialogue, damageNPC } = useRivermarsh();
  
  const movementInput = useControlsStore((state) => state.movement);
  const cameraAzimuth = useControlsStore((state) => state.camera.azimuth);
  const actions = useControlsStore((state) => state.actions);

  const speed = 5;
  const sprintSpeed = 8;
  const jumpForce = 8;
  const gravity = -20;
  const groundY = 1;

  const interactCooldownRef = useRef(0);
  const attackCooldownRef = useRef(0);
  const prevInteractRef = useRef(false);
  const prevAttackRef = useRef(false);

  useEffect(() => {
    console.log("Player component mounted - diorama controls active");
  }, []);

  useFrame((state, delta) => {
    if (!playerRef.current || isPaused) return;
    
    const moveForward = movementInput.y;
    const moveRight = movementInput.x;

    const isMoving = Math.abs(moveForward) > 0.1 || Math.abs(moveRight) > 0.1;
    const isSprinting = isMoving && player.stats.stamina > 0;
    const currentSpeed = isSprinting ? sprintSpeed : speed;

    if (isSprinting) {
      useStamina(delta * 10);
    } else {
      restoreStamina(delta * 5);
    }

    const forward = new THREE.Vector3(
      Math.sin(cameraAzimuth),
      0,
      Math.cos(cameraAzimuth)
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

    if (actions.jump && Math.abs(playerRef.current.position.y - groundY) < 0.1 && player.stats.stamina > 20) {
      velocityRef.current.y = jumpForce;
      useStamina(20);
      console.log("Jump!");
    }

    interactCooldownRef.current = Math.max(0, interactCooldownRef.current - delta);
    attackCooldownRef.current = Math.max(0, attackCooldownRef.current - delta);

    if (actions.interact && !prevInteractRef.current && interactCooldownRef.current === 0) {
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
    prevInteractRef.current = actions.interact;

    if (actions.attack && !prevAttackRef.current && attackCooldownRef.current === 0 && player.stats.stamina > 15) {
      const playerPos = new THREE.Vector3(...player.position);
      const attackRange = 2.5;
      
      const targetNPC = npcs.find(npc => {
        const npcPos = new THREE.Vector3(...npc.position);
        const distance = playerPos.distanceTo(npcPos);
        return distance < attackRange && npc.type === "hostile";
      });

      if (targetNPC) {
        const baseDamage = 10;
        const weaponBonus = player.equipped.weapon?.stats?.attack || 0;
        const totalDamage = baseDamage + weaponBonus;
        
        console.log(`Attacking ${targetNPC.name} for ${totalDamage} damage!`);
        damageNPC(targetNPC.id, totalDamage);
        useStamina(15);
        attackCooldownRef.current = 0.6;
      } else {
        console.log("Attack missed - no enemy in range");
      }
    }
    prevAttackRef.current = actions.attack;

    velocityRef.current.y += gravity * delta;

    const newPosition = playerRef.current.position.clone();
    newPosition.add(velocityRef.current.clone().multiplyScalar(delta));

    if (newPosition.y <= groundY) {
      newPosition.y = groundY;
      velocityRef.current.y = 0;
    }

    playerRef.current.position.copy(newPosition);
    updatePlayerPosition([newPosition.x, newPosition.y, newPosition.z]);
  });

  return (
    <mesh ref={playerRef} position={player.position} castShadow>
      <boxGeometry args={[0.6, 0.8, 1]} />
      <meshStandardMaterial color="#8B6914" />
      
      <mesh position={[0, 0.5, 0.3]} castShadow>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshStandardMaterial color="#8B6914" />
      </mesh>
    </mesh>
  );
}
