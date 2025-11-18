
# Technical Decision Log

## 2025-01-18: Migration to Ruler Nested Structure

**Decision:** Adopt Ruler's nested `.ruler/` directory standard across the entire repository.

**Rationale:**
- Enables component-specific AI agent instructions
- Better organization than centralized markdown files
- Supports cross-agent collaboration (Copilot, Claude, Cursor, etc.)
- Aligns with Ruler's official documentation patterns

**Implementation:**
- Created `.ruler/` directories for: root, client, python, docs, crew_agents
- Moved domain-specific rules (ECS, R3F, shaders) to appropriate locations
- Migrated centralized docs to nested structure
- Configured `ruler.toml` with `nested = true`

**Impact:** 
- Documentation now scales with codebase structure
- AI agents get context-aware instructions
- Easier to maintain as project grows

---

## 2025-01-17: CrewAI with OpenRouter

**Decision:** Use OpenRouter's `auto` routing instead of fixed models.

**Rationale:**
- Automatic failover between providers
- Cost optimization (routes to cheapest capable model)
- Rate limit handling built-in
- Supports Claude 3.5 Sonnet, GPT-4o-mini, Codestral

**Implementation:**
- Set `OPENAI_API_BASE=https://openrouter.ai/api/v1`
- Configure `model: "openrouter/auto"` in CrewAI tasks
- Use LiteLLM for unified interface

**Impact:** More reliable agent execution with lower costs.

---

## 2025-01-16: Parallel Development Strategy

**Decision:** Split development into CrewAI (backend) and human (frontend) tracks.

**Rationale:**
- Maximize parallelization
- Leverage AI strengths (data processing, system architecture)
- Leverage human strengths (visual design, UX decisions)
- Faster overall development velocity

**Implementation:**
- Created `shared/contracts/` for type definitions
- Set up `shared/backend/` for CrewAI deliverables
- Agent focuses on `client/src/prototypes/` and integration
- Use process-compose for long-running CrewAI tasks

**Impact:** Backend systems build autonomously while human iterates on design.

---

## 2025-01-15: ECS Architecture with Miniplex

**Decision:** Use Miniplex for Entity Component System, not custom implementation.

**Rationale:**
- Type-safe with full TypeScript support
- React hooks integration (`useEntities`)
- Performant archetype-based queries
- Active maintenance and documentation

**Alternatives Considered:**
- bitECS (too low-level, no React integration)
- Custom implementation (reinventing wheel)

**Impact:** Clean ECS architecture with zero TypeScript errors.

---

## 2025-01-14: Mobile-First Performance

**Decision:** Target 60fps on mid-tier phones (iPhone 12, Galaxy S20 equivalent).

**Rationale:**
- Mobile is primary platform for exploration games
- Performance constraints force good architecture
- Desktop will easily exceed performance targets

**Implementation:**
- Instancing for all repeated geometry (>10 instances)
- LOD system with 3 levels (high/med/low poly)
- Texture atlasing and compression
- Shader precision qualifiers (mediump default)
- GPU profiling with React DevTools

**Impact:** Smooth experience on mobile, desktop gets bonus performance.

---

## 2025-01-13: React Three Fiber + Drei

**Decision:** Build 3D rendering with React Three Fiber, not vanilla Three.js.

**Rationale:**
- Declarative component model matches React patterns
- Drei provides essential helpers (Instances, Detailed, useGLTF)
- Easier state management with Zustand integration
- Better TypeScript support

**Alternatives Considered:**
- Vanilla Three.js (more verbose, harder to maintain)
- Babylon.js (less React ecosystem support)

**Impact:** Faster development with cleaner component architecture.

---

## Template for Future Decisions

```markdown
## YYYY-MM-DD: Decision Title

**Decision:** What was decided

**Rationale:** Why this decision was made

**Alternatives Considered:** What else was evaluated

**Implementation:** How it's being implemented

**Impact:** Effect on project
```
