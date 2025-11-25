# Rivermarsh Development Environment
# Supports: Node.js (React Three Fiber), Python (CrewAI), Android (Capacitor)

FROM node:24-bookworm-slim

# Display for GUI-based tests
ENV DISPLAY=:99

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build essentials
    git \
    git-lfs \
    curl \
    wget \
    build-essential \
    pkg-config \
    # Python 3.12+ for CrewAI
    python3 \
    python3-pip \
    python3-venv \
    # X11 libraries for GUI testing
    xvfb \
    x11-utils \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxinerama-dev \
    # Browser testing dependencies (Chromium + ChromeDriver)
    chromium \
    chromium-driver \
    # Headless browser support libraries (Playwright/Chromium)
    libgbm1 \
    libgbm-dev \
    libdrm2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgtk-3-dev \
    libnotify-dev \
    libnss3 \
    libnss3-dev \
    libxss1 \
    libxtst6 \
    xdg-utils \
    libatspi2.0-0 \
    libsecret-1-0 \
    libcups2 \
    libnspr4 \
    fonts-liberation \
    # Additional common browser deps
    libglib2.0-0 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxkbcommon0 \
    libxshmfence1 \
    libpango-1.0-0 \
    ffmpeg \
    # OpenGL/WebGL testing (React Three Fiber)
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    mesa-utils \
    # Android/Capacitor build prerequisites
    openjdk-17-jdk \
    unzip \
    gradle \
    ca-certificates \
    # Redis for agent task queue
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Initialize git-lfs with SMUDGE FILTER DISABLED
# Prevents crashes with large LFS repos - actual LFS ops happen in GitHub Actions
RUN git lfs install --system --skip-smudge

# Install uv (Python package manager - fast, modern)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install just command runner
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# Install process-compose (multi-process orchestration)
RUN curl -L -o /tmp/process-compose.tar.gz \
    "https://github.com/F1bonacc1/process-compose/releases/download/v1.51.1/process-compose_linux_amd64.tar.gz" \
    && tar -xzf /tmp/process-compose.tar.gz -C /usr/local/bin process-compose \
    && chmod +x /usr/local/bin/process-compose \
    && rm /tmp/process-compose.tar.gz

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# pnpm via Corepack (MANDATORY package manager for this project)
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9.15.0 --activate && pnpm --version

# Playwright: install required OS deps and cache Chromium browser
RUN pnpm dlx playwright install-deps
RUN pnpm dlx playwright install chromium

# Android SDK (for Capacitor Android builds)
ENV ANDROID_CMDLINE_TOOLS_VERSION=11076708
ENV ANDROID_SDK_ROOT=/opt/android-sdk ANDROID_HOME=/opt/android-sdk
ENV PATH="$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools"
RUN mkdir -p /opt/android-sdk/cmdline-tools \
    && curl -sSL -o /tmp/cmdtools.zip "https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_CMDLINE_TOOLS_VERSION}_latest.zip" \
    && unzip -q /tmp/cmdtools.zip -d /opt/android-sdk/cmdline-tools \
    && mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest \
    && rm -f /tmp/cmdtools.zip

RUN yes | sdkmanager --licenses && sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# Environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# Copy supervisord config for multi-process support
COPY .cursor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
