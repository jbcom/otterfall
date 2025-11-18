import {
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Typography,
  Box,
  SelectChangeEvent,
} from '@mui/material';
import { BiomeType } from '../../ecs/components/BiomeComponent';
import { WeatherType } from '../../ecs/components/WeatherComponent';
import { TimePhase } from '../../ecs/components/TimeOfDayComponent';

interface BiomeControlsProps {
  biome: BiomeType;
  weather: WeatherType;
  timePhase: TimePhase;
  timeOfDay: number;
  onBiomeChange: (biome: BiomeType) => void;
  onWeatherChange: (weather: WeatherType) => void;
  onTimeChange: (hour: number, phase: TimePhase) => void;
}

const TIME_PHASES: { label: string; phase: TimePhase; hour: number }[] = [
  { label: 'Dawn', phase: 'dawn', hour: 6 },
  { label: 'Day', phase: 'day', hour: 12 },
  { label: 'Dusk', phase: 'dusk', hour: 18 },
  { label: 'Night', phase: 'night', hour: 23 },
];

export function BiomeControls({
  biome,
  weather,
  timePhase,
  timeOfDay,
  onBiomeChange,
  onWeatherChange,
  onTimeChange,
}: BiomeControlsProps) {
  const handleBiomeChange = (event: SelectChangeEvent) => {
    onBiomeChange(event.target.value as BiomeType);
  };

  const handleWeatherChange = (event: SelectChangeEvent) => {
    onWeatherChange(event.target.value as WeatherType);
  };

  const handleTimeChange = (_event: Event, value: number | number[]) => {
    const hour = value as number;
    let phase: TimePhase;
    
    if (hour >= 5 && hour < 7) phase = 'dawn';
    else if (hour >= 7 && hour < 17) phase = 'day';
    else if (hour >= 17 && hour < 19) phase = 'dusk';
    else phase = 'night';
    
    onTimeChange(hour, phase);
  };

  return (
    <Card
      sx={{
        position: 'absolute',
        top: 16,
        left: 16,
        minWidth: 280,
        maxWidth: 320,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        zIndex: 1000,
      }}
    >
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Biome Controls
        </Typography>

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="biome-select-label">Biome</InputLabel>
          <Select
            labelId="biome-select-label"
            value={biome}
            label="Biome"
            onChange={handleBiomeChange}
          >
            <MenuItem value="marsh">Grass (Marsh)</MenuItem>
            <MenuItem value="forest">Forest</MenuItem>
            <MenuItem value="desert">Desert</MenuItem>
            <MenuItem value="tundra">Tundra</MenuItem>
            <MenuItem value="savanna">Savanna</MenuItem>
            <MenuItem value="mountain">Mountain</MenuItem>
            <MenuItem value="scrubland">Scrubland</MenuItem>
          </Select>
        </FormControl>

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel id="weather-select-label">Weather</InputLabel>
          <Select
            labelId="weather-select-label"
            value={weather}
            label="Weather"
            onChange={handleWeatherChange}
          >
            <MenuItem value="clear">Clear</MenuItem>
            <MenuItem value="rain">Rain</MenuItem>
            <MenuItem value="fog">Fog</MenuItem>
            <MenuItem value="snow">Snow</MenuItem>
            <MenuItem value="storm">Storm</MenuItem>
            <MenuItem value="sandstorm">Sandstorm</MenuItem>
          </Select>
        </FormControl>

        <Box sx={{ mb: 1 }}>
          <Typography variant="body2" gutterBottom>
            Time of Day: {timePhase.charAt(0).toUpperCase() + timePhase.slice(1)} ({Math.floor(timeOfDay)}:00)
          </Typography>
          <Slider
            value={timeOfDay}
            min={0}
            max={24}
            step={0.5}
            onChange={handleTimeChange}
            marks={TIME_PHASES.map((tp) => ({
              value: tp.hour,
              label: tp.label,
            }))}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${Math.floor(value)}:${String(Math.round((value % 1) * 60)).padStart(2, '0')}`}
          />
        </Box>

        <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
          ECS-driven SDF rendering with dynamic biome updates
        </Typography>
      </CardContent>
    </Card>
  );
}
