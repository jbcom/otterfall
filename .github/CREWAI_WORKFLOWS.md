# CrewAI GitHub Actions Workflows

This document describes how CrewAI integrates with GitHub Actions for autonomous development management.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Issues/PRs ──────► crewai-orchestrator.yml ──────► CrewAI Flows   │
│       │                      │                           │         │
│       │                      ▼                           ▼         │
│       │              ┌───────────────┐         ┌─────────────────┐ │
│       │              │ Route Action  │         │ tdd_prototype   │ │
│       │              │ - analyze     │         │ meshy_asset     │ │
│       │              │ - review      │         │ batch_gen       │ │
│       │              │ - plan        │         │ integration     │ │
│       │              └───────────────┘         └─────────────────┘ │
│       │                                               │            │
│       ▼                                               ▼            │
│  hitl-review-handler.yml ◄───────────────── Asset Generation      │
│       │                                               │            │
│       │                    ┌──────────────────────────┘            │
│       │                    │                                       │
│       ▼                    ▼                                       │
│  /approve ────────► meshy-asset-pipeline.yml ◄──── Meshy Webhooks │
│  /reject                   │                            ▲         │
│  /regenerate               │                            │         │
│                            ▼                            │         │
│                     repository_dispatch ◄──── webhook_proxy.py    │
│                                                         │         │
└─────────────────────────────────────────────────────────┼─────────┘
                                                          │
                                              ┌───────────┴───────────┐
                                              │     Meshy API         │
                                              │  (text-to-3D, etc)    │
                                              └───────────────────────┘
```

## Workflows

### 1. `crewai-orchestrator.yml` - Main Orchestrator

The central workflow that coordinates all CrewAI activities.

**Triggers:**
- `workflow_dispatch` - Manual trigger with flow selection
- `issues` - New issues with `crewai` or `ai-ready` labels
- `issue_comment` - Commands like `@crewai analyze`
- `schedule` - Daily planning (9am UTC), weekly review (Monday 10am)
- `push` - Feature branch validation

**Usage:**
```yaml
# Manual trigger via GitHub UI or CLI
gh workflow run crewai-orchestrator.yml \
  -f flow=tdd_prototype \
  -f flow_args='{"feature": "new_biome"}'
```

### 2. `meshy-asset-pipeline.yml` - Asset Generation

Handles the async Meshy API workflow for 3D asset generation.

**Triggers:**
- `workflow_dispatch` - Manual generation for specific species
- `repository_dispatch` - Webhook callbacks from Meshy API

**Usage:**
```yaml
# Generate otter assets
gh workflow run meshy-asset-pipeline.yml \
  -f species=otter \
  -f prompt="A realistic river otter, detailed fur texture"
```

### 3. `hitl-review-handler.yml` - Human Review

Processes human feedback on generated assets.

**Commands (via issue comments):**
- `/approve` - Approve and integrate assets
- `/reject <reason>` - Reject with feedback
- `/regenerate` - Regenerate with same params
- `/tweak <adjustments>` - Regenerate with changes

## Setup Instructions

### 1. Repository Secrets

Add these secrets in Settings → Secrets and variables → Actions:

| Secret | Description |
|--------|-------------|
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM access |
| `ANTHROPIC_API_KEY` | Anthropic API key (alternative) |
| `MESHY_API_KEY` | Meshy API key for 3D generation |
| `MESHY_WEBHOOK_URL` | Base URL for webhook proxy |

### 2. Webhook Proxy Setup

For Meshy API webhooks to trigger GitHub Actions:

**Option A: Local Development (ngrok)**
```bash
# Terminal 1: Start webhook proxy
cd python/scripts
GITHUB_TOKEN=ghp_xxx GITHUB_REPO=owner/otterfall python webhook_proxy.py

# Terminal 2: Expose via ngrok
ngrok http 8000
# Use the ngrok URL as MESHY_WEBHOOK_URL
```

**Option B: Cloud Deployment**
Deploy `webhook_proxy.py` to:
- AWS Lambda with API Gateway
- Google Cloud Functions
- Cloudflare Workers
- Any HTTP endpoint that can call GitHub API

### 3. Issue Labels

Create these labels for proper workflow routing:

| Label | Color | Description |
|-------|-------|-------------|
| `crewai` | `#7057ff` | Triggers CrewAI analysis |
| `ai-ready` | `#0e8a16` | Ready for autonomous work |
| `hitl-review` | `#fbca04` | Needs human review |
| `revision-needed` | `#d93f0b` | Rejected, needs revision |

## CrewAI Commands

Use these commands in issues/PRs to interact with CrewAI:

| Command | Description |
|---------|-------------|
| `@crewai analyze` | Analyze issue and propose solution |
| `@crewai implement` | Start implementation flow |
| `@crewai review` | Request code review |
| `@crewai status` | Get current progress status |
| `/approve` | Approve HITL review item |
| `/reject <reason>` | Reject with feedback |

## Flow Descriptions

### TDD Prototype Flow
Standard 4-phase development:
1. **Design** - Technical design with specs
2. **Implement** - Build based on design
3. **Validate** - QA testing
4. **Document** - Update documentation

### Meshy Asset Flow
3D asset generation pipeline:
1. **Text-to-3D** - Generate static model
2. **Rigging** - Add skeleton
3. **Animation** - Apply animations
4. **Retexture** - Create variants
5. **HITL Review** - Human approval

### Prototype Assessment Flow
Evaluate prototype readiness:
- Routes to: `deploy`, `refactor`, or `next_slice`

## Monitoring

### Workflow Status
Check workflow runs:
```bash
gh run list --workflow=crewai-orchestrator.yml
gh run view <run-id>
```

### Logs
View CrewAI logs:
```bash
gh run view <run-id> --log
```

### Debugging
Enable debug logging by adding secret:
- `ACTIONS_STEP_DEBUG` = `true`

## Best Practices

1. **Label issues appropriately** - Use `crewai` label for AI work
2. **Provide clear descriptions** - CrewAI reads issue bodies
3. **Review HITL items promptly** - Don't let reviews pile up
4. **Monitor API costs** - Track OpenRouter/Meshy usage
5. **Test locally first** - Use `uv run python -m crew_agents.run_flow` locally

## Troubleshooting

### Workflow not triggering
- Check issue has correct labels
- Verify secrets are set
- Check workflow permissions in repo settings

### CrewAI errors
- Check API keys are valid
- Verify crewbase.yaml syntax
- Check agent/task configuration

### Webhook not received
- Verify webhook proxy is running
- Check ngrok/cloud function logs
- Verify GITHUB_TOKEN has repo scope
