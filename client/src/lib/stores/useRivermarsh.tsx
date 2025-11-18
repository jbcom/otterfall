import { create } from "zustand";
import { subscribeWithSelector } from "zustand/middleware";

export type OtterFaction = "river_clan" | "marsh_raiders" | "lone_wanderers" | "elder_council" | "neutral";
export type QuestStatus = "available" | "active" | "completed" | "failed";

export interface PlayerStats {
  health: number;
  maxHealth: number;
  stamina: number;
  maxStamina: number;
  otterAffinity: number;
  level: number;
  experience: number;
}

export interface InventoryItem {
  id: string;
  name: string;
  type: "weapon" | "consumable" | "quest_item" | "treasure";
  quantity: number;
  description: string;
}

export interface Quest {
  id: string;
  title: string;
  description: string;
  giver: string;
  status: QuestStatus;
  objectives: string[];
  completedObjectives: number[];
  rewards: {
    experience: number;
    items?: InventoryItem[];
    affinityChange?: number;
  };
}

export interface OtterNPC {
  id: string;
  name: string;
  faction: OtterFaction;
  position: [number, number, number];
  type: "friendly" | "hostile" | "neutral" | "merchant" | "quest_giver";
  dialogue?: string[];
  quests?: string[];
  health?: number;
  maxHealth?: number;
}

export interface GameState {
  player: {
    position: [number, number, number];
    rotation: [number, number];
    stats: PlayerStats;
    inventory: InventoryItem[];
    activeQuests: Quest[];
    completedQuests: Quest[];
    factionReputation: Record<OtterFaction, number>;
  };
  npcs: OtterNPC[];
  gameTime: number;
  isPaused: boolean;
  showInventory: boolean;
  showQuestLog: boolean;
  activeDialogue: {
    npcId: string;
    npcName: string;
    messages: string[];
    currentIndex: number;
  } | null;
  
  updatePlayerPosition: (position: [number, number, number]) => void;
  updatePlayerRotation: (rotation: [number, number]) => void;
  updatePlayerStats: (stats: Partial<PlayerStats>) => void;
  addInventoryItem: (item: InventoryItem) => void;
  removeInventoryItem: (itemId: string, quantity: number) => void;
  startQuest: (quest: Quest) => void;
  updateQuestObjective: (questId: string, objectiveIndex: number) => void;
  completeQuest: (questId: string) => void;
  toggleInventory: () => void;
  toggleQuestLog: () => void;
  togglePause: () => void;
  startDialogue: (npcId: string, npcName: string, messages: string[]) => void;
  nextDialogue: () => void;
  endDialogue: () => void;
  takeDamage: (amount: number) => void;
  heal: (amount: number) => void;
  useStamina: (amount: number) => void;
  restoreStamina: (amount: number) => void;
  addExperience: (amount: number) => void;
  spawnNPC: (npc: OtterNPC) => void;
  removeNPC: (npcId: string) => void;
  damageNPC: (npcId: string, amount: number) => void;
}

export const useRivermarsh = create<GameState>()(
  subscribeWithSelector((set, get) => ({
    player: {
      position: [0, 1, 0],
      rotation: [0, 0],
      stats: {
        health: 100,
        maxHealth: 100,
        stamina: 100,
        maxStamina: 100,
        otterAffinity: 50,
        level: 1,
        experience: 0,
      },
      inventory: [
        {
          id: "starter_fish",
          name: "Fresh Fish",
          type: "consumable",
          quantity: 3,
          description: "A tasty fish that restores health. Otters love these!",
        },
      ],
      activeQuests: [],
      completedQuests: [],
      factionReputation: {
        river_clan: 50,
        marsh_raiders: 0,
        lone_wanderers: 25,
        elder_council: 30,
        neutral: 50,
      },
    },
    npcs: [],
    gameTime: 0,
    isPaused: false,
    showInventory: false,
    showQuestLog: false,
    activeDialogue: null,

    updatePlayerPosition: (position) =>
      set((state) => ({
        player: { ...state.player, position },
      })),

    updatePlayerRotation: (rotation) =>
      set((state) => ({
        player: { ...state.player, rotation },
      })),

    updatePlayerStats: (stats) =>
      set((state) => ({
        player: {
          ...state.player,
          stats: { ...state.player.stats, ...stats },
        },
      })),

    addInventoryItem: (item) =>
      set((state) => {
        const existingItem = state.player.inventory.find((i) => i.id === item.id);
        if (existingItem) {
          return {
            player: {
              ...state.player,
              inventory: state.player.inventory.map((i) =>
                i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
              ),
            },
          };
        }
        return {
          player: {
            ...state.player,
            inventory: [...state.player.inventory, item],
          },
        };
      }),

    removeInventoryItem: (itemId, quantity) =>
      set((state) => ({
        player: {
          ...state.player,
          inventory: state.player.inventory
            .map((item) =>
              item.id === itemId
                ? { ...item, quantity: item.quantity - quantity }
                : item
            )
            .filter((item) => item.quantity > 0),
        },
      })),

    startQuest: (quest) =>
      set((state) => ({
        player: {
          ...state.player,
          activeQuests: [...state.player.activeQuests, { ...quest, status: "active" }],
        },
      })),

    updateQuestObjective: (questId, objectiveIndex) =>
      set((state) => ({
        player: {
          ...state.player,
          activeQuests: state.player.activeQuests.map((quest) =>
            quest.id === questId
              ? {
                  ...quest,
                  completedObjectives: [...quest.completedObjectives, objectiveIndex],
                }
              : quest
          ),
        },
      })),

    completeQuest: (questId) =>
      set((state) => {
        const quest = state.player.activeQuests.find((q) => q.id === questId);
        if (!quest) return state;

        get().addExperience(quest.rewards.experience);
        
        if (quest.rewards.items) {
          quest.rewards.items.forEach((item) => get().addInventoryItem(item));
        }

        if (quest.rewards.affinityChange) {
          get().updatePlayerStats({
            otterAffinity: state.player.stats.otterAffinity + quest.rewards.affinityChange,
          });
        }

        return {
          player: {
            ...state.player,
            activeQuests: state.player.activeQuests.filter((q) => q.id !== questId),
            completedQuests: [...state.player.completedQuests, { ...quest, status: "completed" }],
          },
        };
      }),

    toggleInventory: () =>
      set((state) => ({
        showInventory: !state.showInventory,
        showQuestLog: false,
      })),

    toggleQuestLog: () =>
      set((state) => ({
        showQuestLog: !state.showQuestLog,
        showInventory: false,
      })),

    togglePause: () =>
      set((state) => ({
        isPaused: !state.isPaused,
      })),

    startDialogue: (npcId, npcName, messages) =>
      set({
        activeDialogue: {
          npcId,
          npcName,
          messages,
          currentIndex: 0,
        },
        isPaused: true,
      }),

    nextDialogue: () =>
      set((state) => {
        if (!state.activeDialogue) return state;
        const nextIndex = state.activeDialogue.currentIndex + 1;
        if (nextIndex >= state.activeDialogue.messages.length) {
          return {
            activeDialogue: null,
            isPaused: false,
          };
        }
        return {
          activeDialogue: {
            ...state.activeDialogue,
            currentIndex: nextIndex,
          },
        };
      }),

    endDialogue: () =>
      set({
        activeDialogue: null,
        isPaused: false,
      }),

    takeDamage: (amount) =>
      set((state) => {
        const newHealth = Math.max(0, state.player.stats.health - amount);
        return {
          player: {
            ...state.player,
            stats: { ...state.player.stats, health: newHealth },
          },
        };
      }),

    heal: (amount) =>
      set((state) => {
        const newHealth = Math.min(
          state.player.stats.maxHealth,
          state.player.stats.health + amount
        );
        return {
          player: {
            ...state.player,
            stats: { ...state.player.stats, health: newHealth },
          },
        };
      }),

    useStamina: (amount) =>
      set((state) => ({
        player: {
          ...state.player,
          stats: {
            ...state.player.stats,
            stamina: Math.max(0, state.player.stats.stamina - amount),
          },
        },
      })),

    restoreStamina: (amount) =>
      set((state) => ({
        player: {
          ...state.player,
          stats: {
            ...state.player.stats,
            stamina: Math.min(
              state.player.stats.maxStamina,
              state.player.stats.stamina + amount
            ),
          },
        },
      })),

    addExperience: (amount) =>
      set((state) => {
        const newExp = state.player.stats.experience + amount;
        const expForNextLevel = state.player.stats.level * 100;
        
        if (newExp >= expForNextLevel) {
          const newLevel = state.player.stats.level + 1;
          return {
            player: {
              ...state.player,
              stats: {
                ...state.player.stats,
                experience: newExp - expForNextLevel,
                level: newLevel,
                maxHealth: state.player.stats.maxHealth + 10,
                health: state.player.stats.maxHealth + 10,
                maxStamina: state.player.stats.maxStamina + 5,
                stamina: state.player.stats.maxStamina + 5,
              },
            },
          };
        }

        return {
          player: {
            ...state.player,
            stats: { ...state.player.stats, experience: newExp },
          },
        };
      }),

    spawnNPC: (npc) =>
      set((state) => ({
        npcs: [...state.npcs, npc],
      })),

    removeNPC: (npcId) =>
      set((state) => ({
        npcs: state.npcs.filter((npc) => npc.id !== npcId),
      })),

    damageNPC: (npcId, amount) =>
      set((state) => ({
        npcs: state.npcs.map((npc) => {
          if (npc.id === npcId && npc.health !== undefined) {
            const newHealth = Math.max(0, npc.health - amount);
            return { ...npc, health: newHealth };
          }
          return npc;
        }),
      })),
  }))
);
