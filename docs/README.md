
# Rivermarsh Documentation

This directory contains detailed technical documentation. For quick reference, see [../replit.md](../replit.md).

## Architecture

- [ECS Systems](architecture/ECS_SYSTEMS.md) - Component lifecycle and system execution order
- [CrewAI Usage Guide](architecture/crewai_usage.md) - Running autonomous agents
- [Integration Guide](architecture/INTEGRATION_GUIDE.md) - Connecting CrewAI deliverables to frontend

## Development Workflows

- [Parallel Development](PARALLEL_DEVELOPMENT.md) - CrewAI backend + Agent frontend strategy
- [Session State](SESSION_STATE.md) - Current project status and blockers
- [Decision Log](DECISION_LOG.md) - User approvals and architect reviews

## Asset Generation

- [Otter Pipeline PoC](asset_generation/otter_pipeline_poc.md) - Meshy 3D asset workflow

## Troubleshooting

- [CrewAI Runbook](troubleshooting/CREWAI_RUNBOOK.md) - Common issues and solutions

## Ruler Integration

This project uses [Ruler](https://github.com/intellectronica/ruler) for distributed agent instructions:

- **Root standards:** [../.ruler/AGENTS.md](../.ruler/AGENTS.md)
- **Writing style:** [.ruler/writing_style.md](.ruler/writing_style.md)
- **Frontend patterns:** [../client/.ruler/AGENTS.md](../client/.ruler/AGENTS.md)
- **Backend conventions:** [../python/.ruler/AGENTS.md](../python/.ruler/AGENTS.md)
- **Shared contracts:** [../shared/.ruler/AGENTS.md](../shared/.ruler/AGENTS.md)

To generate agent-specific instruction files:
```bash
ruler apply
```

This creates files like `CLAUDE.md`, `.clinerules`, `.cursor/mcp.json`, etc.
