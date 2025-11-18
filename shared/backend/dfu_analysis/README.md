# Daggerfall Unity Data Analysis

This module contains parsers and mapping logic for converting Daggerfall Unity fantasy creatures and systems into Rivermarsh natural world equivalents.

## Directory Structure

```
dfu_analysis/
├── parsers/           # Python scripts for parsing DFU data
├── data/              # Raw extracted DFU data
├── mappings/          # Species and biome mapping files
└── tests/             # Unit tests
```

## Species Mapping

Fantasy creatures are mapped to natural world equivalents based on:
- Size and physical characteristics
- Behavioral patterns
- Habitat preferences
- Combat capabilities

### Core Mappings

| DFU Creature | Natural Species | Scientific Name |
|--------------|-----------------|------------------|
| Wolf | Timber Wolf | Canis lupus |
| Rat | Marsh Rat | Rattus norvegicus |
| Bear | Black Bear | Ursus americanus |
| Spider | Wolf Spider | Lycosidae |
| Snake | Eastern Diamondback | Crotalus adamanteus |
| Bat | Little Brown Bat | Myotis lucifugus |
| Scorpion | Forest Scorpion | Heterometrus longimanus |
| Giant Slaughterfish | Northern Pike | Esox lucius |
| Imp | Raccoon | Procyon lotor |
| Grizzly Bear | Grizzly Bear | Ursus arctos horribilis |

## Stat Conversion Formulas

```python
# DFU to Rivermarsh conversions
size = dfu_size * 0.1  # Scale down fantasy sizes
mass = size * size * 100  # Approximate mass from size
speed = dfu_speed * 0.5  # Balance movement speeds
health = dfu_health * 0.75  # Reduce health pools
damage = dfu_damage * 0.5  # Balance damage output
```

## Usage

```typescript
import { DFUSpeciesMapping } from './mappings/species';

// Get natural world equivalent
const wolfData = DFUSpeciesMapping.mapDFUCreature('wolf');

// Get all mapped species
const allSpecies = DFUSpeciesMapping.getAllSpecies();

// Filter by biome
const forestSpecies = DFUSpeciesMapping.getSpeciesByBiome('forest');
```