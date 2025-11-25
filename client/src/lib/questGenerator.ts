import { Quest, OtterFaction, InventoryItem } from "./stores/useRivermarsh";

interface QuestTemplate {
  title: string;
  description: string;
  objectives: string[];
  rewards: {
    experience: number;
    items?: InventoryItem[];
    affinityChange?: number;
  };
  requiredFaction?: OtterFaction;
  requiredLevel?: number;
}

const QUEST_TEMPLATES: Record<string, QuestTemplate[]> = {
  river_clan: [
    {
      title: "Restore the River Flow",
      description: "The ancient river has been blocked by debris. Help the River Clan restore the natural flow.",
      objectives: [
        "Find the source of the blockage",
        "Clear 5 debris piles",
        "Report back to Elder Ripple",
      ],
      rewards: {
        experience: 150,
        affinityChange: 10,
        items: [{
          id: "river_pearl",
          name: "River Pearl",
          type: "treasure",
          quantity: 1,
          description: "A beautiful pearl from the deep rivers, treasured by the River Clan.",
          stats: { fishingBonus: 5 },
        }],
      },
    },
    {
      title: "Teach the Young Otters",
      description: "Young otters need to learn the ancient swimming techniques. Demonstrate your mastery.",
      objectives: [
        "Swim through 3 underwater rings",
        "Dive to 10 meters depth",
        "Catch 5 fish for the students",
      ],
      rewards: {
        experience: 100,
        affinityChange: 5,
        items: [{
          id: "swimming_medal",
          name: "Swimming Medal",
          type: "treasure",
          quantity: 1,
          description: "Recognition from the River Clan for swimming prowess.",
          stats: { swimSpeed: 3 },
        }],
      },
    },
  ],
  marsh_raiders: [
    {
      title: "Infiltrate the Hideout",
      description: "The Marsh Raiders have stolen valuable artifacts. Sneak into their hideout and recover them.",
      objectives: [
        "Locate the Marsh Raider hideout",
        "Retrieve 3 stolen artifacts",
        "Escape undetected",
      ],
      rewards: {
        experience: 200,
        items: [{
          id: "stealth_cloak",
          name: "Shadow Cloak",
          type: "armor",
          equipmentSlot: "accessory",
          quantity: 1,
          description: "A dark cloak that helps with sneaking.",
          stats: { defense: 2 },
        }],
      },
    },
  ],
  elder_council: [
    {
      title: "The Ancient Prophecy",
      description: "Decipher the ancient otter scrolls hidden in the flooded caverns.",
      objectives: [
        "Enter the flooded caverns",
        "Find 4 ancient scroll fragments",
        "Return to the Elder Council",
      ],
      rewards: {
        experience: 250,
        affinityChange: 15,
        items: [{
          id: "wisdom_amulet",
          name: "Amulet of Wisdom",
          type: "treasure",
          equipmentSlot: "accessory",
          quantity: 1,
          description: "An ancient amulet bearing the wisdom of past generations.",
          stats: { defense: 5 },
        }],
      },
    },
  ],
  lone_wanderers: [
    {
      title: "Survival of the Fittest",
      description: "Prove your worth to the Lone Wanderers by surviving alone in the wilderness.",
      objectives: [
        "Forage 10 marsh herbs",
        "Build a temporary shelter",
        "Survive 2 nights alone",
      ],
      rewards: {
        experience: 180,
        affinityChange: 8,
        items: [{
          id: "survival_kit",
          name: "Survival Kit",
          type: "tool",
          quantity: 1,
          description: "Essential tools for wilderness survival.",
        }],
      },
    },
  ],
};

const PROCEDURAL_OBJECTIVES = [
  "Collect {count} {item}",
  "Defeat {count} {enemy}",
  "Explore {location}",
  "Deliver message to {npc}",
  "Escort {npc} to {location}",
  "Find the lost {item}",
  "Investigate {location}",
];

const ITEMS = ["fish", "shells", "herbs", "pearls", "artifacts"];
const ENEMIES = ["Marsh Raiders", "hostile otters", "swamp creatures"];
const LOCATIONS = ["the flooded caverns", "the ancient ruins", "the deep marshes", "the hidden grotto"];
const NPCS = ["Elder Ripple", "Swift Paws", "Whisker Sage", "Marsh Guide"];

function generateRandomObjective(seed: number): string {
  const templateIndex = seed % PROCEDURAL_OBJECTIVES.length;
  const template = PROCEDURAL_OBJECTIVES[templateIndex] ?? "Collect {count} {item}";
  
  const item = ITEMS[seed % ITEMS.length] ?? "fish";
  const enemy = ENEMIES[seed % ENEMIES.length] ?? "hostile otters";
  const location = LOCATIONS[seed % LOCATIONS.length] ?? "the marshes";
  const npc = NPCS[seed % NPCS.length] ?? "Elder Ripple";
  
  return template
    .replace("{count}", String(Math.floor((seed % 10) + 3)))
    .replace("{item}", item)
    .replace("{enemy}", enemy)
    .replace("{location}", location)
    .replace("{npc}", npc);
}

export function generateQuest(faction: OtterFaction, playerLevel: number, seed: number): Quest {
  const templates = QUEST_TEMPLATES[faction] ?? [];
  const giver = NPCS[seed % NPCS.length] ?? "Elder Ripple";
  
  if (templates.length > 0 && seed < templates.length) {
    const template = templates[seed];
    if (template) {
      return {
        id: `quest_${faction}_${seed}`,
        title: template.title,
        description: template.description,
        giver,
        status: "available",
        objectives: template.objectives,
        completedObjectives: [],
        rewards: {
          ...template.rewards,
          experience: template.rewards.experience + playerLevel * 10,
        },
      };
    }
  }
  
  const numObjectives = Math.floor((seed % 3) + 2);
  const objectives: string[] = [];
  for (let i = 0; i < numObjectives; i++) {
    objectives.push(generateRandomObjective(seed + i));
  }
  
  return {
    id: `quest_procedural_${faction}_${seed}`,
    title: `${faction.replace("_", " ").toUpperCase()} Mission #${seed}`,
    description: `A procedurally generated quest for the ${faction} faction.`,
    giver,
    status: "available",
    objectives,
    completedObjectives: [],
    rewards: {
      experience: 50 + playerLevel * 15,
      affinityChange: 5,
    },
  };
}

export function generateQuestChain(faction: OtterFaction, playerLevel: number): Quest[] {
  const quests: Quest[] = [];
  const baseQuests = QUEST_TEMPLATES[faction] || [];
  
  for (let i = 0; i < baseQuests.length; i++) {
    quests.push(generateQuest(faction, playerLevel, i));
  }
  
  const numProceduralQuests = 3;
  for (let i = 0; i < numProceduralQuests; i++) {
    quests.push(generateQuest(faction, playerLevel, baseQuests.length + i + 100));
  }
  
  return quests;
}
