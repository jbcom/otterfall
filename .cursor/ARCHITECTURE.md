# Docker Architecture - Why Not Docker Compose?

## TL;DR

**We use `process-compose` instead of `docker-compose`** for orchestrating multiple development services.

## Why This Matters

Multiple AI code review bots flagged "missing docker-compose.yml" as a bug. This document clarifies our architecture.

## Our Stack

```
┌─────────────────────────────────────────────┐
│  Cursor Remote Container                     │
│  (nikolaik/python-nodejs:python3.13-nodejs24)│
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  process-compose                        │ │
│  │  ├── conport (ConPort memory)          │ │
│  │  ├── rivermarsh_crew (CrewAI)          │ │
│  │  ├── crew_monitor (Monitoring)         │ │
│  │  └── ... (see process-compose.yaml)    │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Why process-compose Over docker-compose?

### 1. Single Container Development
- **Cursor expects ONE container** with the dev environment
- docker-compose creates MULTIPLE containers (anti-pattern for Cursor)
- process-compose runs multiple processes INSIDE one container

### 2. Simpler Architecture
```bash
# docker-compose (multi-container)
docker-compose up -d dev
docker-compose exec dev bash
docker-compose up -d conport
docker-compose logs conport

# process-compose (single-container)
process-compose up -d
process-compose logs conport
```

### 3. Better for AI Agents
- All processes share the same filesystem
- No network bridges between containers
- Logs centralized in `./logs/`
- No volume mount complexity

### 4. Cross-Platform
- Works identically on macOS, Linux, Windows
- No Docker daemon required (can run natively)
- Lighter weight than Docker containers

## What We Don't Use

| ❌ Not Used | ✅ Instead Use |
|-------------|---------------|
| `docker-compose.yml` | `process-compose.yaml` |
| `supervisord.conf` | `process-compose.yaml` |
| `redis-server` | No task queue needed (yet) |
| Multiple containers | Single Cursor container |

## Configuration Files

### `.cursor/Dockerfile`
Defines the development container image used by Cursor.

### `.cursor/environment.json`
Tells Cursor which Dockerfile to use:
```json
{
  "build": {
    "context": "..",
    "dockerfile": ".cursor/Dockerfile"
  }
}
```

### `/process-compose.yaml` (project root)
Orchestrates multiple services inside the container:
- ConPort (project memory)
- CrewAI agents (code generation)
- Monitoring scripts

## For AI Code Reviewers

If you're seeing this from a PR:

✅ **This is correct** - We intentionally don't have:
- `.cursor/docker-compose.yml`
- `.cursor/supervisord.conf`  
- Redis/supervisor packages in Dockerfile

✅ **We do have**:
- `/process-compose.yaml` (project root)
- `process-compose` binary installed in Dockerfile

## Running the Stack

```bash
# Inside Cursor container (automatic)
process-compose up -d

# Check status
process-compose ps

# View logs
process-compose logs conport

# Stop all
process-compose down
```

## References

- process-compose: https://github.com/F1bonacc1/process-compose
- Cursor Environments: https://docs.cursor.com/advanced/environments
- nikolaik/python-nodejs: https://github.com/nikolaik/docker-python-nodejs
