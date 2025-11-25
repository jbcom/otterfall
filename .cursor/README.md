# Rivermarsh - Docker Development Environment

This directory contains a production-grade Docker environment for Rivermarsh game development.

## 🎯 Why This Setup?

- **Consistency**: Matches GitHub Actions CI environment exactly
- **Full Stack**: Node.js 24 + Python 3.12 + Android SDK
- **No Version Conflicts**: Eliminates "works on my machine" issues
- **Complete Toolchain**: All dependencies pre-installed (uv, pnpm, Playwright, Android SDK)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Start interactive development shell
docker-compose -f .cursor/docker-compose.yml up -d dev
docker-compose -f .cursor/docker-compose.yml exec dev bash

# Inside container:
pnpm run dev        # Start Vite dev server
pnpm run build      # Build production
pnpm test           # Run tests
```

### CrewAI Development

```bash
# Run CrewAI flows
docker-compose -f .cursor/docker-compose.yml --profile crewai run crewai

# Or manually:
cd python/crew_agents
uv run crew_agents design      # Run game design flow
uv run crew_agents implement   # Run implementation flow
uv run crew_agents assets      # Run asset generation flow
```

## 📋 Common Tasks

### Frontend Development
```bash
# Start dev server (accessible at http://localhost:5173)
docker-compose run --rm -p 5173:5173 dev pnpm run dev

# Build production
docker-compose run --rm dev pnpm run build

# Run tests
docker-compose run --rm dev pnpm test
```

### Python Development
```bash
# Sync dependencies
cd python/crew_agents && uv sync

# Run CrewAI
uv run crew_agents design

# Run tests
uv run pytest
```

### Android Build
```bash
# Build APK
docker-compose run --rm --profile android android pnpm run cap:build:android
```

## 🔧 Environment Specifications

### Included Tools
- **Node.js**: v24.x
- **Python**: 3.12 with uv package manager
- **pnpm**: 9.15.0 (via corepack)
- **Java**: OpenJDK 17
- **Android SDK**: API 34, Build Tools 34.0.0
- **Playwright**: Pre-installed with Chromium
- **GitHub CLI**: gh
- **just**: Command runner

### Required Environment Variables
```bash
# For CrewAI
OPENROUTER_API_KEY=your-key-here

# For asset generation
MESHY_API_KEY=your-key-here

# For GitHub operations
GITHUB_TOKEN=your-token-here
```

## 📊 Volume Management

Named volumes for performance:
- `node_modules`: npm dependencies cache
- `python_venv`: Python virtual environment
- `android_gradle`: Android Gradle cache
- `gradle_cache`: Global Gradle cache

### Clean volumes if needed:
```bash
docker-compose -f .cursor/docker-compose.yml down -v
docker volume prune
```

## 🔗 Related Files

- `Dockerfile` - Main image definition
- `docker-compose.yml` - Service orchestration
- `environment.json` - Cursor environment config
- `supervisord.conf` - Multi-process management
- `rules/` - Cursor rules for agents
