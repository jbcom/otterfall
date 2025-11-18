# Python Tooling Workspace

This directory contains the Python tooling workspace for the Rivermarsh game project, organized as a dual-language monorepo with separate TypeScript (client/) and Python (python/) components.

## Structure

```
python/
├── mesh_toolkit/          # Meshy SDK package
│   ├── pyproject.toml
│   └── src/
│       └── mesh_toolkit/
│           ├── __init__.py
│           ├── api/           # HTTP client and API wrappers
│           ├── services/      # Service layer (Text3D, Rigging, Animation, Retexture)
│           ├── persistence/   # Repository and storage layer
│           ├── catalog/       # Animation catalog and static data
│           ├── models.py      # Pydantic models and enums
│           └── logging.py     # Logging utilities
├── crew_agents/           # CrewAI agents package
│   ├── pyproject.toml
│   └── src/
│       └── crew_agents/
│           └── __main__.py   # Main crew execution script
├── scripts/               # Utility scripts
│   ├── generate_assets.py
│   └── update_meshy_catalog.py
├── tests/                 # Test suite
│   ├── conftest.py        # Shared pytest fixtures
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests with VCR cassettes
│       ├── cassettes/     # pytest-vcr HTTP recordings
│       └── fixtures/      # Test fixtures (GLB files, etc.)
└── README.md              # This file
```

## Packages

### mesh_toolkit

The Meshy SDK package provides a clean Python interface to the Meshy API for game asset generation.

**Key Features:**
- Text-to-3D model generation
- Auto-rigging for character models
- Animation application from 678+ preset animations
- Texture generation and retexturing
- VCR-recorded integration tests for cost-free testing

**Dependencies:**
- httpx (async HTTP client)
- tenacity (retry logic)
- pydantic (data validation)
- rich (console output)
- playwright (browser automation for catalog scraping)

**Installation:**
```bash
uv pip install -e python/mesh_toolkit
```

**Usage:**
```python
from mesh_toolkit import MeshyClient
from mesh_toolkit.services.text3d_service import Text3DService

client = MeshyClient(api_key="your-key")
service = Text3DService(client)
task = service.create_task(prompt="river otter", art_style="sculpture")
```

### crew_agents

CrewAI-based agents for game development automation using hierarchical multi-agent workflows.

**Dependencies:**
- crewai[anthropic] (multi-agent framework)
- crewai-tools (agent tooling)
- litellm (LLM routing)
- pyyaml (config loading)

**Installation:**
```bash
uv pip install -e python/crew_agents
```

**Usage:**
```bash
python -m crew_agents
```

## Workspace Configuration

This workspace uses `uv` for package management with a workspace configuration in the root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["python/mesh_toolkit", "python/crew_agents"]
```

## Development

### Install All Packages

Install both packages in editable mode:

```bash
uv pip install -e python/mesh_toolkit -e python/crew_agents
```

### Run Tests

```bash
# Run all tests
pytest python/tests/

# Run unit tests only
pytest python/tests/unit/

# Run integration tests (uses VCR cassettes)
pytest python/tests/integration/

# Run with coverage
pytest python/tests/ --cov=mesh_toolkit --cov=crew_agents
```

### Update Dependencies

```bash
# Add dependency to mesh_toolkit
cd python/mesh_toolkit
uv add httpx

# Add dependency to crew_agents
cd python/crew_agents
uv add crewai-tools

# Sync all workspace dependencies
uv sync
```

## Testing Strategy

### Unit Tests (`python/tests/unit/`)

- Fast, isolated tests with mocked dependencies
- No external API calls
- Test internal logic and edge cases

### Integration Tests (`python/tests/integration/`)

- Real API calls recorded with pytest-vcr
- Cassettes stored in `cassettes/` for replay
- GLB files downloaded to `fixtures/glb/` for quality review
- Run once to record, then replay for free

**VCR Benefits:**
- No API costs after initial recording
- Deterministic test results
- Fast test execution
- Offline development support

## Scripts

### generate_assets.py

Generate game assets using the Meshy SDK.

```bash
python python/scripts/generate_assets.py
```

### update_meshy_catalog.py

Scrape and update the Meshy animation catalog using Playwright.

```bash
python python/scripts/update_meshy_catalog.py
```

## Architecture Decisions

### Why Separate Packages?

- **mesh_toolkit**: Standalone SDK that could be published to PyPI
- **crew_agents**: Application-specific agents that depend on mesh_toolkit
- Clear dependency graph: `crew_agents → mesh_toolkit`

### Why src/ Layout?

- Prevents accidental imports from development directory
- Forces proper package installation
- Industry best practice for Python packages

### Why pytest-vcr?

- Meshy API calls are expensive (credits + time)
- VCR cassettes allow free test replay
- Integration tests verify real API behavior without cost

## Migration Notes

This structure replaces the previous flat layout:

**Before:**
```
tools/meshy/           → python/mesh_toolkit/src/mesh_toolkit/
game_dev_crew_advanced.py → python/crew_agents/src/crew_agents/__main__.py
tests/                 → python/tests/
scripts/               → python/scripts/
```

**Import Changes:**
```python
# Before
from tools.meshy.client import MeshyClient

# After
from mesh_toolkit.client import MeshyClient
```

All tests have been updated to use the new import paths.
