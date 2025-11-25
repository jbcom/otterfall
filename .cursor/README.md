# Rivermarsh - Cursor Docker Environment

This directory contains the Docker configuration for Cursor's remote development environment.

## 🎯 What's Included

- **Node.js 24** + **Python 3.13** via `nikolaik/python-nodejs` base image
- **pnpm 9.15.0** - Node package manager
- **uv** - Python package manager (pre-installed in base image)
- **process-compose v1.78.0** - Multi-process orchestration (replaces docker-compose)
- **Playwright + Chromium** - Browser automation for CrewAI MCP server
- **just v1.40.0** - Task runner (Debian native package)
- **GitHub CLI v2.46.0** - CI/CD integration (Debian native package)
- **git-lfs v3.6.1** - Large file storage (Debian native package)

### MCP Servers (for CrewAI Agents)
- **@playwright/mcp** - Browser automation
- **@upstash/context7-mcp** - Up-to-date library documentation
- **@modelcontextprotocol/server-filesystem** - File system access
- **mcp-server-git** - Git operations
- **conport-mcp** - Context portal for development

## 🚀 Usage

This Dockerfile is used **automatically** by Cursor when you open the workspace in a remote container.

### Manual Build (for testing)

```bash
# Build the image
docker build -t rivermarsh-dev -f .cursor/Dockerfile .

# Run interactively
docker run -it --rm -v $(pwd):/workspace rivermarsh-dev bash
```

## 📋 Development Workflow

### Frontend Development
```bash
pnpm install        # Install dependencies
pnpm run dev        # Start Vite dev server
pnpm run build      # Build production
pnpm test           # Run tests
```

### Python Development
```bash
cd python/crew_agents
uv sync             # Install dependencies
uv run crew_agents design      # Run game design flow
uv run pytest       # Run tests
```

### Multi-Process Orchestration

We use **process-compose** (not docker-compose) for running multiple services:

```bash
# Start all background processes
process-compose up -d

# View logs
process-compose logs

# Check status
process-compose ps

# Stop all
process-compose down
```

See `process-compose.yaml` in the project root for configuration.

## 🔧 Environment Specifications

### Included Tools
- **Node.js**: v24.x
- **Python**: 3.13 with uv package manager (pre-installed)
- **pnpm**: 9.15.0 (via corepack)
- **Playwright**: Pre-installed with bundled Chromium (for CrewAI MCP server)
- **process-compose**: v1.78.0 (multi-process orchestration)
- **GitHub CLI**: gh v2.46.0 (Debian native package)
- **just**: v1.40.0 (Debian native package)
- **git-lfs**: v3.6.1 (Debian native package)

### Image Optimizations
- **Size**: ~2.66GB (reduced from 3.15GB by removing duplicate chromium installations)
- **Native Debian packages**: Uses Trixie repos for git-lfs, gh, and just instead of manual downloads
- **Single Chromium**: Playwright bundles its own Chromium; system chromium removed to save space
- **Minimal layers**: Consolidated apt installations for faster builds and smaller cache

### Required Environment Variables
```bash
# For CrewAI
OPENROUTER_API_KEY=your-key-here

# For asset generation
MESHY_API_KEY=your-key-here

# For GitHub operations
GITHUB_TOKEN=your-token-here
```

## 🔗 Related Files

- `Dockerfile` - Main image definition
- `environment.json` - Cursor environment config
- `/process-compose.yaml` - Multi-process orchestration (project root)
- `rules/` - Cursor rules for agents
