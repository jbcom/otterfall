# Daggerfall Unity Data Sources

## Official Repository
The main Daggerfall Unity project: https://github.com/Interkarma/daggerfall-unity

## Key Data Files Location

In the DFU repository, creature and game data is located at:
- `Assets/StreamingAssets/Tables/` - Core data tables
- `Assets/Game/Addons/ModSupport/ModSettings/` - Mod data structures
- `Assets/Scripts/Game/Entities/` - Entity definitions (C# code)
- `Assets/Scripts/Game/MagicAndEffects/Effects/` - Effect data

## Data Format Notes

Most DFU data is stored as:
1. **Binary files** (.dat, .bsa) - Legacy Daggerfall format
2. **C# code** - MonoBehaviour classes with hardcoded stats
3. **JSON/XML** - Mod system configuration

## Recommended Approach

Since we don't have the actual DFU binary files, use:

1. **Web search** for DFU creature stats documentation
2. **UESP wiki** (The Unofficial Elder Scrolls Pages) has comprehensive Daggerfall data: https://en.uesp.net/wiki/Daggerfall:Bestiary
3. **DFU source code** on GitHub - read C# entity definitions
4. **Community wikis** and modding documentation

## Sample Creature Stats (from UESP/DFU source)

### Basic Creatures
- **Rat**: Health 4-13, Damage 1-4, Speed 20
- **Bat**: Health 4-10, Damage 1-3, Speed 25, Flying
- **Spider**: Health 8-20, Damage 1-6, Speed 15, Poison
- **Snake**: Health 6-15, Damage 1-5, Speed 18, Poison
- **Wolf**: Health 15-35, Damage 2-8, Speed 30
- **Bear**: Health 30-60, Damage 3-12, Speed 25
- **Grizzly Bear**: Health 40-80, Damage 4-15, Speed 28

### Intermediate Creatures  
- **Sabretooth Tiger**: Health 35-70, Damage 3-13, Speed 32
- **Giant**: Health 50-100, Damage 5-18, Speed 20
- **Orc**: Health 25-50, Damage 3-10, Speed 25
- **Werewolf**: Health 40-75, Damage 4-14, Speed 35, Lycanthropy
- **Harpy**: Health 25-50, Damage 3-11, Speed 30, Flying

### Advanced Creatures
- **Daedroth**: Health 60-120, Damage 6-20, Speed 28, Fire Immunity
- **Vampire**: Health 50-100, Damage 5-17, Speed 32, Undead
- **Lich**: Health 70-140, Damage 7-22, Speed 25, Undead, Magic

## Conversion Formula

For mapping to natural world:

```python
def convert_dfu_to_rivermarsh(dfu_creature):
    return {
        'health': dfu_creature.health * 0.75,  # Scale down health pools
        'damage': dfu_creature.damage * 0.5,    # Balance damage
        'speed': dfu_creature.speed * 0.5,      # Convert to realistic kph
        'mass_kg': estimate_mass(dfu_creature.size),
        'behavior': map_behavior(dfu_creature.ai_type),
    }
```

## Required Deliverables

1. **parsers/dfu_scraper.py** - Scrape UESP wiki for creature data
2. **data/creatures_raw.json** - Raw scraped data
3. **mappings/species.json** - Converted to natural world (already has 2 examples)
4. **mappings/biomes.json** - Climate to biome mapping

## Quality Standards

- Minimum 20 species mapped
- All stats scientifically plausible for natural creatures
- Include behavioral patterns (nocturnal, pack hunting, etc.)
- Habitat preferences based on real animal ecology
