# Rivermarsh CrewAI Game Builder

AI-powered code generation for the Rivermarsh game, using CrewAI agents that **actually write code** to the codebase.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     GAME BUILDER CREW                           │
├─────────────┬─────────────┬─────────────────────────────────────┤
│ Senior      │ QA          │ Chief                               │
│ TypeScript  │ Engineer    │ Engineer                            │
│ Engineer    │             │                                     │
│             │             │                                     │
│ • Writes    │ • Reviews   │ • Evaluates                         │
│   code      │   for       │   completeness                      │
│ • Uses      │   errors    │ • Final                             │
│   tools     │             │   approval                          │
└─────────────┴─────────────┴─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TOOLS                                       │
├─────────────┬─────────────┬─────────────────────────────────────┤
│ Write Code  │ Read Code   │ List Directory                      │
│ File        │ File        │ Contents                            │
│             │             │                                     │
│ Writes to   │ Reads       │ Lists files                         │
│ allowed     │ existing    │ in project                          │
│ directories │ patterns    │                                     │
└─────────────┴─────────────┴─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE BASE                              │
├─────────────┬─────────────┬─────────────────────────────────────┤
│ ECS         │ Rendering   │ Game                                │
│ Patterns    │ Patterns    │ Architecture                        │
│             │             │                                     │
│ Working     │ R3F         │ Full game                           │
│ component   │ component   │ architecture                        │
│ examples    │ examples    │ documentation                       │
└─────────────┴─────────────┴─────────────────────────────────────┘
```

## How It Works

1. **Knowledge Base**: Contains actual working code from the game as reference patterns
2. **Planning**: CrewAI plans the task step-by-step before execution
3. **Code Generation**: Senior engineer reads existing patterns, writes new code
4. **QA Review**: QA engineer checks for errors and convention violations
5. **Final Approval**: Chief engineer ensures code meets requirements
6. **Memory**: Agents learn from past interactions to improve
7. **Training**: Human feedback further improves agent quality

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Code Writing** | ✅ | Agents write actual TypeScript to files |
| **Pattern Learning** | ✅ | Knowledge base with working code patterns |
| **Planning** | ✅ | Step-by-step task planning |
| **Memory** | ✅ | Learns from past interactions |
| **QA Review** | ✅ | Code reviewed before approval |
| **Training** | ✅ | Human feedback improves agents |
| **Code Execution** | ✅ | Can test code locally |

## Usage

### Build a Component

```bash
# Build a new ECS component
uv run crew_agents build "Create a QuestComponent for tracking player quests with objectives and rewards"

# Build an entity factory
uv run crew_agents build "Create a createQuestGiver entity factory that spawns NPCs with dialogue"
```

### Train the Crew

Training uses human feedback to improve agent quality:

```bash
# Run 5 training iterations with human feedback
uv run crew_agents train 5

# Save to custom filename
uv run crew_agents train 5 -f my_training.pkl
```

During training:
1. Agent generates code
2. You provide feedback on what's wrong/right
3. Agent improves based on feedback
4. Feedback is saved for future runs

### List Knowledge Sources

```bash
uv run crew_agents list-knowledge
```

### Test Tools

```bash
uv run crew_agents test-tools
```

## Configuration

### Environment Variables

```bash
# Required for LLM access
export OPENROUTER_API_KEY="your-key-here"

# Optional - for asset generation
export MESHY_API_KEY="your-key-here"
```

### LLM Configuration

The crew uses OpenRouter with automatic model selection:

```python
from crew_agents.config.llm import get_llm

# Default (auto-selects best model)
llm = get_llm("openrouter/auto")

# Or specify a model
llm = get_llm("openrouter/anthropic/claude-3.5-sonnet")
```

## Directory Structure

```
python/crew_agents/
├── knowledge/                    # Working code patterns
│   ├── ecs_patterns/
│   │   └── components.md
│   ├── rendering_patterns/
│   │   └── r3f_components.md
│   └── game_components/
│       └── architecture.md
├── src/crew_agents/
│   ├── crews/
│   │   └── game_builder/        # Main code-building crew
│   │       ├── config/
│   │       │   ├── agents.yaml
│   │       │   └── tasks.yaml
│   │       └── game_builder_crew.py
│   ├── tools/                   # File manipulation tools
│   │   └── file_tools.py
│   ├── config/
│   │   └── llm.py               # OpenRouter configuration
│   └── main.py                  # CLI entry point
└── trained_agents_data.pkl      # Training data (after training)
```

## Allowed Write Directories

For safety, the code writer tool only writes to specific directories:

- `client/src/ecs/components` - ECS component definitions
- `client/src/ecs/entities` - Entity factory functions
- `client/src/ecs/systems` - ECS systems
- `client/src/components` - React Three Fiber components
- `client/src/lib/stores` - Zustand stores
- `shared/contracts` - TypeScript contracts
- `shared/backend/ecs_world` - Backend ECS code

## Adding Knowledge

To add new patterns to the knowledge base:

1. Create a markdown file in the appropriate `knowledge/` subdirectory
2. Include actual working code examples
3. Document patterns and conventions
4. The crew will automatically use it

Example:
```markdown
# New Pattern Name

## Description
What this pattern does...

## Code Example
\`\`\`typescript
// Actual working code from the codebase
export interface MyComponent {
  ...
}
\`\`\`

## Key Patterns
- Pattern 1
- Pattern 2
```

## Development

### Running Tests

```bash
uv run pytest tests/unit/crew_agents/ -v
```

### Adding a New Crew

1. Create directory: `src/crew_agents/crews/new_crew/`
2. Add config: `config/agents.yaml`, `config/tasks.yaml`
3. Create crew class with `@CrewBase` decorator
4. Add to `crews/__init__.py`

## See Also

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI Training](https://docs.crewai.com/en/concepts/training)
- [CrewAI Planning](https://docs.crewai.com/en/concepts/planning)
- [CrewAI Coding Agents](https://docs.crewai.com/en/learn/coding-agents)
- [OpenRouter](https://openrouter.ai/)
