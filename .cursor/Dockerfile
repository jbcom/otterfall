FROM node:24-bookworm-slim

# =============================================================================
# SYSTEM DEPENDENCIES
# =============================================================================
# Single consolidated layer for all apt packages to minimize image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials (required for native Node modules: better-sqlite3, etc.)
    build-essential \
    pkg-config \
    # Version control
    git \
    git-lfs \
    # Download utilities
    curl \
    wget \
    ca-certificates \
    # Python runtime (required for uv and CrewAI agents)
    python3 \
    python3-pip \
    # Playwright/Chromium dependencies (headless browser testing)
    chromium \
    chromium-driver \
    libgbm1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# GIT LFS CONFIGURATION
# =============================================================================
# CRITICAL: --skip-smudge prevents workspace crashes with large LFS repos
# LFS files appear as pointers (fine for Cursor/AI analysis)
# Actual LFS operations (checkout, pull) handled by GitHub Actions
RUN git lfs install --system --skip-smudge

# =============================================================================
# DEVELOPER TOOLS
# =============================================================================
# Install tools in a single layer to reduce image size

# Python package manager (uv) - Required for process-compose.yaml workflows
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/ && \
    uv --version

# Just command runner - Task automation
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | \
    bash -s -- --to /usr/local/bin

# Process-compose - Multi-process orchestration (required for CrewAI workflows)
RUN curl -L https://github.com/F1bonacc1/process-compose/releases/download/v1.51.1/process-compose_linux_amd64.tar.gz | \
    tar xz -C /usr/local/bin process-compose && \
    chmod +x /usr/local/bin/process-compose && \
    process-compose --version

# GitHub CLI - CI/CD integration
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# =============================================================================
# NODE.JS PACKAGE MANAGER (pnpm)
# =============================================================================
# MUST match package.json "packageManager" field exactly
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && \
    corepack prepare pnpm@9.15.0 --activate && \
    pnpm --version

# =============================================================================
# PLAYWRIGHT BROWSER CACHE
# =============================================================================
# Pre-install Playwright dependencies and Chromium browser
# This reduces startup time for tests and matches CI workflow
RUN pnpm dlx playwright install-deps chromium && \
    pnpm dlx playwright install chromium

# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================
# Selenium/WebDriver paths (for integration tests)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /workspace
