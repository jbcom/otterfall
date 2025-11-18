
# Rivermarsh Game - Project Brief

## Vision
A cozy 3D otter adventure game blending exploration, fishing, questing, and relationship building in a realistic marshland setting. Think "Zelda: Breath of the Wild meets Stardew Valley" set in a natural ecosystem.

## Target Platform
- Web (React Three Fiber)
- Mobile-optimized (iOS/Android via WebGL)
- Performance: 60 FPS on mid-tier phones

## Core Technology Stack
- **Frontend**: React 18, TypeScript (strict), React Three Fiber, Zustand
- **ECS**: Miniplex for world simulation
- **AI**: Yuka.js for creature behaviors
- **Backend**: Python (mesh toolkit, CrewAI agents)
- **Build**: Vite 7, pnpm, Node 24, Python 3.13

## Architecture Pattern
- **AI-Agent Collaboration**: CrewAI handles backend systems, human handles frontend integration
- **Context Management**: ConPort (Context Portal MCP) for RAG and institutional memory
- **Nested Ruler Structure**: Each component has its own `.ruler/` directory
- **Type Safety**: Zero TypeScript errors enforced
- **Mobile-First Performance**: 60fps constraint on all rendering

## Current Sprint Focus
Building autonomous CrewAI development crew to accelerate:
1. ECS component schemas (contracts in `shared/contracts/`)
2. Daggerfall Unity data parsing (species/biome mapping)
3. Yuka AI integration (creature behaviors)
4. Procedural terrain/water rendering (SDF-based)
5. Quest/dialogue systems (RPG mechanics)

## Development Workflow
1. Define contracts in `shared/contracts/`
2. CrewAI agents build backend systems in `shared/backend/`
3. Human reviews and integrates with frontend prototypes
4. ConPort stores all decisions, progress, and patterns
5. Iterate based on testing feedback

## Key Constraints
- No PostgreSQL (using file-based persistence)
- No Replit-specific services
- ConPort for all context management (not project_brief.md)
- Alpha→Work→Omega workflow pattern mandatory
