```markdown
# Rivermarsh Ecosystem Rules Document

This document outlines the ecological rules governing the Rivermarsh game world, designed to create a dynamic and emergent gameplay experience.

## 1. Food Web Diagrams (Text Representation)

These diagrams represent the flow of energy through each biome, highlighting key predator-prey relationships.  The player-controlled Otter is included.

*   **Central Marsh (CM):**
    *   Sun -> Cattails/Lily Pads
    *   Cattails/Lily Pads -> Ducks, Turtles
    *   Sun -> Algae -> Clams
    *   Sun -> Insects (Dragonflies)
    *   Insects -> Frogs
    *   Frogs -> Herons, Otter, Snakes
    *   Fish -> Herons, Otter, Snakes, Turtles
    *   Ducks -> Otter, Foxes
    *   Turtles -> Otter
    *   Snakes -> Herons
    *   Otter -> (Apex Predator - can eat Fish, Frogs, Ducks, Turtles, Clams)

*   **Mudflat Shoreline (MS):**
    *   Sun -> Algae -> Clams, Crabs
    *   Insects -> Shorebirds
    *   Clams -> Otter, Shorebirds
    *   Crabs -> Otter, Herons
    *   Shorebirds -> Foxes
    *   Otter -> (Apex Predator - can eat Clams, Crabs, Shorebirds)

*   **Cypress Swamp (CS):**
    *   Sun -> Cypress Trees -> Insects
    *   Insects -> Frogs
    *   Frogs -> Snakes, Alligators
    *   Fish -> Alligators, Snakes
    *   Snakes -> Alligators, Herons
    *   Otter -> Alligators, Snakes, Fish, Frogs
    *   Alligators -> Otter, Herons, Snakes, Fish

*   **River Delta (RD):**
    *   Sun -> River Plants
    *   River Plants -> Fish
    *   Fish -> Herons, Otter, Snakes, Alligators
    *   Insects -> Frogs
    *   Frogs -> Snakes, Herons, Otter
    *   Otter -> (Apex Predator - can eat Fish, Frogs)

*   **Cattail Fields (CF):**
    *   Sun -> Cattails
    *   Cattails -> Insects
    *   Insects -> Birds, Mice
    *   Mice -> Foxes, Snakes, Hawks
    *   Birds -> Hawks, Foxes
    *   Snakes -> Hawks
    *   Otter (occasional visitor) -> Mice, Birds, Fish (if near water)
    *   Hawks -> Foxes, Snakes

*   **Sandy Beach (SB):**
    *   Sun -> Algae -> Clams, Crabs
    *   Clams -> Gulls
    *   Crabs -> Gulls
    *   Gulls -> Foxes
    *   Otter (occasional visitor) -> Clams, Crabs

*   **Lake (LK):**
    *   Sun -> Algae -> Small Fish
    *   Small Fish -> Large Fish
    *   Large Fish -> Herons, Otters, Eagles
    *   Otters -> Large Fish, Small Fish
    *   Eagles -> Herons, Otters, Large Fish
    *   Herons -> Small Fish

## 2. Population Balance Formulas

These formulas determine how populations of different species change over time, based on factors like birth rate, death rate, food availability, and predation.

*   **General Formula:**

    `Population Change = (Birth Rate * Population) - (Death Rate * Population) +/- (Migration)`

*   **Birth Rate:**  Base birth rate modified by food availability.  If food is scarce, birth rate decreases.

    `Birth Rate = Base Birth Rate * (Food Availability / Max Food Consumption)`

*   **Death Rate:** Base death rate modified by predation risk and starvation.

    `Death Rate = Base Death Rate + (Predation Risk Factor * Predator Population) + (Starvation Factor * (1 - (Food Availability / Max Food Consumption)))`

*   **Specific Examples:**

    *   **Otter Population:**
        *   `Birth Rate (Otter) = BaseOtterBirthRate * (AvailableFish + AvailableFrogs + AvailableClams) / MaxOtterConsumption`
        *   `Death Rate (Otter) = BaseOtterDeathRate + (AlligatorPredation * AlligatorPopulation) + (Starvation * (1 - (AvailableFood / MaxOtterConsumption)))`

    *   **Fish Population:**
        *   `Birth Rate (Fish) = BaseFishBirthRate * (AvailableAlgae / MaxFishConsumption)`
        *   `Death Rate (Fish) = BaseFishDeathRate + (OtterPredation * OtterPopulation) + (HeronPredation * HeronPopulation) + (AlligatorPredation * AlligatorPopulation)`

    *   **Alligator Population:**
        *   `Birth Rate (Alligator) = BaseAlligatorBirthRate * (AvailableFish + AvailableFrogs + AvailableSnakes) / MaxAlligatorConsumption`
        *   `Death Rate (Alligator) = BaseAlligatorDeathRate + (Starvation * (1 - (AvailableFood / MaxAlligatorConsumption)))`  (Alligators have no natural predators in this ecosystem as adults)

*   **Carrying Capacity:** Each biome has a carrying capacity for each species.  As a population approaches its carrying capacity, birth rates decrease and death rates increase.

    `Carrying Capacity Modifier = 1 - (Current Population / Carrying Capacity)`
    This modifier is applied to both birth and death rates.

## 3. Resource Respawn Timers

These timers dictate how quickly resources regenerate in each biome.  Resource respawn rates are affected by weather and season.

*   **Fish:**
    *   Respawn Time: 60-120 seconds (faster during/after rain, slower in winter)
    *   Affected by: Rain (increased spawn rate), Season (decreased spawn rate in winter)
    *   Location: All water biomes

*   **Frogs:**
    *   Respawn Time: 90-180 seconds (faster after rain, slower in dry periods)
    *   Affected by: Rain (increased spawn rate), Drought (decreased spawn rate)
    *   Location: CM, CS, RD

*   **Clams:**
    *   Respawn Time: 120-240 seconds
    *   Affected by: Tide (more exposed at low tide), Pollution (player action reduces spawn rate)
    *   Location: MS, SB

*   **Cattails:**
    *   Respawn Time: 300-600 seconds
    *   Affected by: Storms (can be destroyed by storms, requiring longer respawn), Season (faster growth in spring/summer)
    *   Location: CM, CF

*   **Lily Pads:**
    *   Respawn Time: 180-360 seconds
    *   Affected by: Season (faster growth in spring/summer)
    *   Location: CM

*   **Berries (Hypothetical - if expanded beyond Rivermarsh):**
    *   Respawn Time: 240-480 seconds
    *   Affected by: Season (only available in certain seasons)
    *   Location: Forest edges (if Forest biome were added)

Resource depletion triggers a global "scarcity" flag, impacting birth rates across multiple species.

## 4. Migration Patterns

Species migrate between biomes based on food availability, season, and population density.

*   **Otters:**
    *   Primary Habitat: CM
    *   Migration Triggers:
        *   Food Scarcity in CM: Migrates to RD, MS, CS in search of food.
        *   Winter: May migrate to RD and LK for better access to fish under the ice (if ice mechanic is implemented).
    *   Migration Patterns:  Moves along waterways, prefers routes with cover.

*   **Herons:**
    *   Primary Habitat: CM, RD
    *   Migration Triggers:
        *   Food Scarcity: Follows fish populations.
        *   Winter: May migrate south (outside the Rivermarsh area) to warmer climates.

*   **Fish:**
    *   Migration Triggers:
        *   Spawning: Migrates from LK to RD to spawn.
        *   Temperature: Moves deeper into the LK during hot weather.
    *   Migration Patterns:  Follows river currents.

*   **Ducks:**
    *   Migration Triggers:
        *   Season: Migrates south (outside the Rivermarsh area) during winter.
    *   Migration Patterns:  Flies along established routes.

*   **Alligators:**
    *   Primary Habitat: CS
    *   Migration Triggers:
        *   Overpopulation: Younger alligators may migrate to RD or CM.
        *   Drought: Migrates to deeper water sources.

## 5. Seasonal Variations

Seasons significantly impact resource availability, creature behavior, and gameplay.

*   **Spring:**
    *   Increased Rainfall: Higher fish and frog populations.
    *   Plant Growth: Cattails and lily pads regenerate faster.
    *   Animal Breeding: Increased birth rates.
    *   Gameplay: Easier access to food, increased visibility.

*   **Summer:**
    *   Warm Temperatures: Increased activity for reptiles (snakes, alligators).
    *   Drought Risk: Can lead to lower frog populations and increased competition for resources.
    *   Gameplay: Risk of overheating, need to find shade.

*   **Autumn:**
    *   Decreasing Temperatures: Animals begin preparing for winter.
    *   Shorter Days: Reduced visibility.
    *   Migration: Birds and some mammals migrate south.
    *   Gameplay: Increased need for shelter, preparation for winter scarcity.

*   **Winter:**
    *   Cold Temperatures: Reduced activity for reptiles and amphibians.
    *   Ice Formation:  Can freeze over CM and RD, creating new traversal challenges and opportunities (ice skating, ice fishing - if implemented).
    *   Food Scarcity: Reduced resource availability.
    *   Gameplay: Increased need for shelter, hunting underwater (if diving mechanic exists), risk of hypothermia.

## 6. Cause-and-Effect Relationships (Emergent Gameplay)

Player actions have consequences that ripple through the ecosystem.

*   **Overhunting Fish:**
    *   Immediate Effect: Reduces fish population in the area.
    *   Long-Term Effect: Decreases food availability for otters, herons, and alligators.  May lead to migration of predators or reduced birth rates.  Clam population may increase slightly due to reduced predation on algae.

*   **Destroying Cattails:**
    *   Immediate Effect: Reduces cover for prey animals.
    *   Long-Term Effect: Increases predation risk for ducks and mice.  Reduces nesting sites for birds.  Can lead to soil erosion if widespread.

*   **Polluting Water (Hypothetical - if pollution mechanic is added):**
    *   Immediate Effect: Reduces fish and frog populations.
    *   Long-Term Effect: Decreases food availability for all predators.  Can lead to deformities in offspring.  Reduces clam population.

*   **Protecting a Species (Hypothetical - if conservation mechanic is added):**
    *   Immediate Effect: Increases the population of the protected species.
    *   Long-Term Effect: Can lead to cascading effects on the food web.  For example, protecting otters can reduce fish populations, which can benefit clam populations.

*   **Altering the Environment (e.g., Building a Dam - Hypothetical):**
    *   Immediate Effect: Changes water flow and creates new habitats.
    *   Long-Term Effect: Can flood areas, create new fishing spots, and alter migration patterns.  Impacts the populations of various species depending on the specific changes.

## 7. Species Contract Considerations (shared/contracts/SpeciesContract.ts)

While the exact structure of the `SpeciesContract.ts` isn't provided, the following considerations apply, assuming it defines species attributes and behaviors:

*   **Species Attributes:** The population formulas should align with species attributes defined in the contract (e.g., `birthRate`, `deathRate`, `foodConsumption`).
*   **Behavioral Patterns:**  Migration patterns and predator-prey interactions should be implemented based on the behavioral traits defined in the contract (e.g., `preferredPrey`, `migrationTriggers`, `habitat`).
*   **Diet:** The food web relationships should be explicitly linked to the diet defined in the SpeciesContract. For instance, if the SpeciesContract indicates that an Otter eats Fish and Frogs, the population formulas and resource respawn rates should ensure that these food sources are available.

## 8. DFU Creature Mappings (shared/backend/dfu_analysis/)

The DFU creature mappings provide data about creature models, animations, and behaviors. This data should be used to:

*   **Ensure Realistic Creature Behavior:** Implement realistic movement patterns, hunting strategies, and social interactions based on the DFU data.
*   **Optimize Performance:** Use the DFU data to optimize creature models and animations for mobile devices.
*   **Create Believable Visuals:** Ensure that creature appearances and animations are consistent with their ecological roles.

By carefully balancing these ecological rules, the Rivermarsh game world can become a truly dynamic and engaging environment where player actions have meaningful consequences, leading to emergent gameplay and a compelling survival experience.
```