import { useEffect, useRef } from "react";
import { useAudio } from "@/lib/stores/useAudio";

export function SoundManager() {
  const { setBackgroundMusic, setHitSound, setSuccessSound, isMuted } = useAudio();
  const backgroundMusicRef = useRef<HTMLAudioElement | null>(null);
  const hitSoundRef = useRef<HTMLAudioElement | null>(null);
  const successSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const bgMusic = new Audio("/sounds/background.mp3");
    bgMusic.loop = true;
    bgMusic.volume = 0.3;
    backgroundMusicRef.current = bgMusic;
    setBackgroundMusic(bgMusic);

    const hitSound = new Audio("/sounds/hit.mp3");
    hitSound.volume = 0.4;
    hitSoundRef.current = hitSound;
    setHitSound(hitSound);

    const successSound = new Audio("/sounds/success.mp3");
    successSound.volume = 0.5;
    successSoundRef.current = successSound;
    setSuccessSound(successSound);

    return () => {
      bgMusic.pause();
      bgMusic.currentTime = 0;
      bgMusic.src = "";
      
      hitSound.pause();
      hitSound.currentTime = 0;
      hitSound.src = "";
      
      successSound.pause();
      successSound.currentTime = 0;
      successSound.src = "";
      
      setBackgroundMusic(null);
      setHitSound(null);
      setSuccessSound(null);
    };
  }, [setBackgroundMusic, setHitSound, setSuccessSound]);

  useEffect(() => {
    if (backgroundMusicRef.current) {
      if (isMuted) {
        backgroundMusicRef.current.pause();
      } else {
        backgroundMusicRef.current.play().catch((e) => {
          console.log("Background music autoplay prevented:", e);
        });
      }
    }
  }, [isMuted]);

  return null;
}
