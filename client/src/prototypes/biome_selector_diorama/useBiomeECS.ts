import { useEffect, useState } from 'react';
import { world } from '../../ecs/world';
import { BiomeComponent, BiomeType, BIOME_ARCHETYPES } from '../../ecs/components/BiomeComponent';
import { WeatherComponent, WeatherType, WEATHER_PRESETS } from '../../ecs/components/WeatherComponent';
import { TimeOfDayComponent, TimePhase, getTimeModifiers } from '../../ecs/components/TimeOfDayComponent';

export interface BiomeState {
  biome: BiomeType;
  weather: WeatherType;
  timePhase: TimePhase;
  timeOfDay: number;
}

const ENTITY_ID = 'biome-diorama-world';

export function useBiomeECS() {
  const [state, setState] = useState<BiomeState>({
    biome: 'marsh',
    weather: 'clear',
    timePhase: 'day',
    timeOfDay: 12,
  });

  useEffect(() => {
    const entity = world.add({
      id: ENTITY_ID,
      biome: {
        type: 'marsh',
        ...BIOME_ARCHETYPES.marsh,
      } as BiomeComponent,
      weather: {
        current: 'clear',
        ...WEATHER_PRESETS.clear,
        startTime: Date.now(),
        durationMinutes: 60,
        transitionProgress: 0,
        nextWeather: null,
      } as WeatherComponent,
      timeOfDay: {
        hour: 12,
        phase: 'day',
        timeScale: 1,
        ...getTimeModifiers(12, 0.5),
      } as TimeOfDayComponent,
    });

    return () => {
      world.remove(entity);
    };
  }, []);

  const setBiome = (biome: BiomeType) => {
    const entity = world.entities.find((e: any) => e.id === ENTITY_ID);
    if (entity && entity.biome) {
      entity.biome = {
        type: biome,
        ...BIOME_ARCHETYPES[biome],
      } as BiomeComponent;
      setState((s) => ({ ...s, biome }));
    }
  };

  const setWeather = (weather: WeatherType) => {
    const entity = world.entities.find((e: any) => e.id === ENTITY_ID);
    if (entity && entity.weather) {
      entity.weather = {
        ...entity.weather,
        current: weather,
        ...WEATHER_PRESETS[weather],
      } as WeatherComponent;
      setState((s) => ({ ...s, weather }));
    }
  };

  const setTimeOfDay = (hour: number, phase: TimePhase) => {
    const entity = world.entities.find((e: any) => e.id === ENTITY_ID);
    if (entity && entity.timeOfDay) {
      entity.timeOfDay = {
        ...entity.timeOfDay,
        hour,
        phase,
        ...getTimeModifiers(hour, 0.5),
      } as TimeOfDayComponent;
      setState((s) => ({ ...s, timeOfDay: hour, timePhase: phase }));
    }
  };

  const getEntity = () => {
    return world.entities.find((e: any) => e.id === ENTITY_ID);
  };

  return {
    state,
    setBiome,
    setWeather,
    setTimeOfDay,
    getEntity,
  };
}
