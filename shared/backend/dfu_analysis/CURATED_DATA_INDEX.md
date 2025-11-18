# Curated DFU Data for Analysis

This directory contains pre-curated, organized Daggerfall Unity data for the CrewAI analysis task.

## Data Files

### 1. dfu_creatures_raw.json
**Source**: UESP Daggerfall Bestiary (https://en.uesp.net/wiki/Daggerfall:Bestiary)
**Content**: Complete creature stats for 38 DFU creatures
**Format**: Structured JSON with:
- Creature ID, name, type
- Level (1-21)
- Health ranges (min/max)
- Armor Class (D&D style, lower = better)
- Material requirements for damage
- Special abilities (Flying, Spellcaster, etc.)
- Disease transmission
- Language skills

**Sample Entry**:
```json
{
  "id": "grizzly_bear",
  "name": "Grizzly Bear",
  "type": "Animal",
  "level": 3,
  "health": {"min": 15, "max": 40},
  "armor_class": 6,
  "material_required": "None",
  "special_abilities": [],
  "disease": null
}
```

**Coverage**:
- 7 Animals (Rat → Sabertooth Tiger)
- 4 Atronachs (Fire, Ice, Flesh, Iron)
- 5 Daedra (Daedroth → Daedra Lord)
- 4 Orcs (Orc → Orc Warlord)
- 2 Lycanthropes (Werewolf, Wereboar)
- 8 Undead (Zombie → Ancient Lich)
- 8 Monsters (Imp, Spriggan, Centaur, etc.)

### 2. MobileEnemy.cs (if downloaded)
**Source**: DFU GitHub Repository
**Content**: C# enum/class definitions for enemy types
**Purpose**: Reference for DFU internal data structures

### 3. mappings/species.json
**Content**: Example mappings from DFU creatures to natural world species
**Status**: Contains 2 starter mappings (Timber Wolf, Marsh Rat)
**Expected**: Should contain 20+ mappings after analysis

### 4. mappings/biomes.json
**Content**: Climate/biome mapping template
**Status**: Empty template
**Expected**: DFU climate zones → Rivermarsh biomes

## Conversion Strategy

### DFU → Natural World Mapping Rules

1. **Size Scaling**: Fantasy creatures are oversized
   - DFU Giant → Scale down to realistic large mammal
   - DFU Rat → Normal rat proportions

2. **Fantasy → Natural Equivalents**:
   - **Werewolf** → Timber Wolf (Canis lupus) + behavioral aggression
   - **Vampire Bat** → Common Vampire Bat (Desmodus rotundus)
   - **Sabertooth Tiger** → Extinct Smilodon (use modern big cat stats)
   - **Giant** → Grizzly Bear (Ursus arctos) or Moose (Alces alces)
   - **Imp** → Raccoon (Procyon lotor) with mischievous behavior
   - **Spriggan** → Wild Boar (Sus scrofa) with territorial aggression

3. **Stat Conversion Formulas**:
```python
def convert_stats(dfu_creature):
    # Health scaling
    health_rivermarsh = (dfu_health_max * 0.75)
    
    # Damage scaling
    damage_rivermarsh = (dfu_damage_avg * 0.5)
    
    # Speed (DFU abstract → real kph)
    # DFU uses abstract speed values, convert to realistic animal speeds
    speed_map = {
        "rat": 15,      # Real rats: ~13 kph
        "wolf": 50,     # Real wolves: ~45-65 kph
        "bear": 35,     # Real bears: ~30-55 kph
    }
    
    # Mass estimation from size
    mass_kg = estimate_from_size_category(dfu_creature)
```

4. **Behavioral Mapping**:
   - **Pack social**: Wolves, rats → pack_social: true
   - **Nocturnal**: Most small predators → nocturnal: true
   - **Territorial**: Bears, big cats → territorial: true
   - **Aggression**: Scale 0.0-1.0 based on DFU hostility

## Analysis Tasks for CrewAI

### Task 1: Parse dfu_creatures_raw.json
- Extract all 38 creatures
- Identify natural world equivalents
- Apply conversion formulas

### Task 2: Generate species.json mappings
- Map each DFU creature to real species
- Include scientific names
- Provide habitat/ecology data
- Add behavioral parameters

### Task 3: Extract quest/dialogue patterns
- Review DFU wiki for quest structure
- Identify reusable templates
- Document dialogue tree patterns

### Task 4: Biome mapping
- Map DFU climate zones to Rivermarsh biomes:
  - Desert → Arid Grassland
  - Swamp → Wetland/Marsh
  - Mountain → Alpine/Subalpine
  - Woodland → Temperate Forest
  - Rainforest → Temperate Rainforest

## Quality Standards

✅ **Minimum 20 species mapped** (Currently have 2)
✅ **All stats scientifically plausible** for natural animals
✅ **Include behavioral parameters** (nocturnal, pack social, etc.)
✅ **Habitat preferences** based on real ecology
✅ **TypeScript-compatible JSON** output

## References

- UESP Daggerfall Bestiary: https://en.uesp.net/wiki/Daggerfall:Bestiary
- DFU GitHub: https://github.com/Interkarma/daggerfall-unity
- SpeciesContract.ts: `../../contracts/SpeciesContract.ts`
- BiomeContract.ts: `../../contracts/BiomeContract.ts`

## Notes for Agents

- **DO NOT** search the entire DFU codebase
- **USE** the curated dfu_creatures_raw.json as your primary source
- **REFERENCE** the conversion formulas above
- **OUTPUT** to mappings/species.json following SpeciesContract
- **VALIDATE** all stats are realistic for natural animals
