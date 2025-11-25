# Dev Tools & Dependencies Maintenance Guide

This guide documents the development tools and their maintenance strategy for the Rivermarsh project.

## 🎯 Core Principle: Leverage Native Packages First

**Always prefer Debian Trixie native packages over manual downloads/installs.**

### Rationale
1. **Smaller image size** - No duplicate binaries or dependencies
2. **Faster builds** - Apt cache is faster than downloading tarballs
3. **Security updates** - Automatic via base image updates
4. **Reliability** - Debian packages are tested and stable

## 📦 Package Sources Priority

### 1. Debian Trixie Native (HIGHEST PRIORITY)
Use `apt-get install` for these tools:
- `git-lfs` - Large file storage (v3.6.1)
- `gh` - GitHub CLI (v2.46.0) 
- `just` - Task runner (v1.40.0)
- `build-essential` - C/C++ compilers for native modules
- `pkg-config` - Build tool dependency resolution

### 2. Base Image (nikolaik/python-nodejs)
Pre-installed, do NOT reinstall:
- `node` - Node.js v24.x
- `python` - Python 3.13.x
- `npm`, `npx` - Node package managers
- `corepack` - Package manager manager
- `uv` - Python package manager (v0.9.x)
- `git` - Version control

### 3. Corepack (for Node.js package managers)
```dockerfile
RUN corepack enable && \
    corepack prepare pnpm@9.15.0 --activate
```
**MUST match `package.json` "packageManager" field exactly.**

### 4. Official Installation Scripts
Use when no Debian package exists:
- `process-compose` - Use official script from F1bonacc1/process-compose repo
```dockerfile
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/F1bonacc1/process-compose/main/scripts/get-pc.sh)" -- -b /usr/local/bin
```

### 5. Manual Download (LAST RESORT)
Only use for tools with no better option. Always:
- Use versioned URLs (not `latest`)
- Verify checksums if available
- Clean up after extraction

## 🔧 Tool-Specific Guidelines

### Playwright
**DO NOT install system chromium!** Playwright bundles its own:
```dockerfile
RUN pnpm dlx playwright install-deps chromium && \
    pnpm dlx playwright install chromium
```

This installs to `/root/.cache/ms-playwright/chromium-*` and includes all required system libraries.

### MCP Servers (CrewAI Integration)

Current active servers (see `python/crew_agents/crewbase.yaml`):

| Server | Package | Purpose |
|--------|---------|---------|
| playwright | `@playwright/mcp` | Browser automation |
| context7 | `@upstash/context7-mcp` | Library docs (React, MUI, Three.js, etc.) |
| filesystem | `@modelcontextprotocol/server-filesystem` | File operations |
| git | `mcp-server-git` (uvx) | Git operations |
| conport | `conport-mcp` (uvx) | Context portal |

**Removed/Deprecated:**
- `@modelcontextprotocol/server-vite` - ❌ Broken, removed
- `@modelcontextprotocol/server-playwright` - ❌ Wrong package name

## 📊 Image Size Optimization Checklist

Before adding new tools, ask:
1. ✅ Is it available in Debian Trixie? → Use apt
2. ✅ Is it available via corepack (pnpm, yarn, etc.)? → Use corepack
3. ✅ Does it have an official install script? → Use the script
4. ✅ Can we use an MCP server instead of installing the tool? → Prefer MCP
5. ⚠️ Do we need both system + tool-bundled version? → Keep only one

### Example: Chromium Removal
**Before:** System chromium (70MB) + Playwright chromium (300MB) = 370MB  
**After:** Playwright chromium only (300MB) = 300MB saved (plus ~20 dependencies)

## 🔄 Maintenance Checklist

When updating tools:

### Monthly Review
- [ ] Check for Debian Trixie package updates (happens automatically with base image)
- [ ] Review process-compose releases (currently v1.78.0)
- [ ] Verify pnpm version matches package.json
- [ ] Test MCP servers still work with latest CrewAI

### When Adding New Tools
- [ ] Check Debian Trixie repos first: `apt-cache search <tool>`
- [ ] Check if tool has official install script
- [ ] Document in this file and README.md
- [ ] Test in Docker container before committing
- [ ] Measure image size impact: `docker images | grep rivermarsh-dev`

### When Removing Tools
- [ ] Search codebase for references: `grep -r "<tool>" .`
- [ ] Remove from Dockerfile
- [ ] Remove from crewbase.yaml (if MCP server)
- [ ] Remove from agents.yaml tools list
- [ ] Update README.md
- [ ] Rebuild and verify: `docker build -t rivermarsh-dev -f .cursor/Dockerfile .`

## 🚨 Common Pitfalls

### ❌ Don't Do This
```dockerfile
# Installing same tool multiple ways
RUN apt-get install chromium
RUN pnpm dlx playwright install chromium  # ← Duplicate!

# Hardcoding versions that break
RUN curl .../v1.51.1/tool.tar.gz  # ← 404 in the future

# Adding tools without checking apt
RUN curl https://github.com/.../gh-linux.tar.gz  # ← gh is in apt!
```

### ✅ Do This
```dockerfile
# Use Debian packages when available
RUN apt-get update && apt-get install -y \
    gh \
    git-lfs \
    just \
    && rm -rf /var/lib/apt/lists/*

# Use official scripts for tools not in Debian
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/F1bonacc1/process-compose/main/scripts/get-pc.sh)" -- -b /usr/local/bin

# Let Playwright manage its own chromium
RUN pnpm dlx playwright install-deps chromium && \
    pnpm dlx playwright install chromium
```

## 📝 Version Compatibility Matrix

| Tool | Dockerfile | Package.json | Notes |
|------|-----------|--------------|-------|
| pnpm | v9.15.0 | v9.15.0 | MUST match exactly |
| Node.js | v24.x | - | From base image |
| Python | v3.13.x | - | From base image |
| just | v1.40.0 | - | Debian native |
| gh | v2.46.0 | - | Debian native |
| git-lfs | v3.6.1 | - | Debian native |
| process-compose | v1.78.0 | - | Official script (auto-updates to latest) |
| Playwright | latest | - | Via pnpm dlx (version in MCP package) |

## 🔗 References

- Base Image: https://github.com/nikolaik/docker-python-nodejs
- Debian Trixie Packages: https://packages.debian.org/trixie/
- Process Compose: https://github.com/F1bonacc1/process-compose
- Playwright MCP: https://www.npmjs.com/package/@playwright/mcp
- Context7 MCP: https://www.npmjs.com/package/@upstash/context7-mcp
