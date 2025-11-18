
# CrewAI Troubleshooting Runbook

## Common Issues

### Task Fails to Start

**Symptoms**:
- `process-compose up <task>` shows "exited"
- No log output in `logs/crewai/<task>.log`

**Diagnosis**:
```bash
# Check environment
env | grep OPENROUTER
env | grep MESHY

# Verify task definition
cat crew_config/tasks.yaml | grep <task_name>

# Check dependencies
process-compose process list
```

**Solutions**:
1. Missing API keys → Add to `.envrc` and reload (`direnv allow`)
2. Invalid task YAML → Validate with `yamllint crew_config/tasks.yaml`
3. Dependency not met → Start prerequisite task first

### Task Hangs

**Symptoms**:
- Log shows "In progress" for > 10 minutes
- No new log entries
- High CPU usage

**Diagnosis**:
```bash
# Check task logs
tail -f logs/crewai/<task>.log | grep -E "ERROR|WARNING|iteration"

# Monitor OpenRouter usage
# Visit https://openrouter.ai/activity
```

**Solutions**:
1. Stuck reasoning loop → Restart task with lower `max_reasoning_attempts` in `agents.yaml`
2. Infinite iteration → Reduce `max_iter` for agent
3. API timeout → Check OpenRouter status, restart task

### Out of Memory

**Symptoms**:
- Task crashes with "Killed"
- `dmesg | grep -i killed` shows OOM killer

**Diagnosis**:
```bash
# Check memory usage
htop # Look for python processes

# Review task complexity
cat crew_config/tasks.yaml | grep -A 20 <task_name>
```

**Solutions**:
1. Split task into smaller subtasks
2. Reduce batch size in `tasks_batch1.yaml`
3. Increase swap space (temporary workaround)

### Integration Test Failures

**Symptoms**:
- CrewAI deliverable exists but fails CI
- TypeScript compilation errors
- Unit tests fail

**Diagnosis**:
```bash
# Run tests locally
cd shared/backend/<deliverable>
npm test -- --verbose

# Check TypeScript errors
npm run typecheck
```

**Solutions**:
1. Contract mismatch → Update contract or request CrewAI revision
2. Missing dependencies → Check `package.json` in deliverable
3. Path issues → Verify imports use correct relative paths

## Log Analysis Examples

### Successful Task Completion
```
[2025-01-18 10:15:32] Task started: ecs_component_schemas
[2025-01-18 10:18:45] Agent reasoning (attempt 1/3)
[2025-01-18 10:22:10] Files created: 12
[2025-01-18 10:25:30] Unit tests: 12/12 passed
[2025-01-18 10:26:00] Task completed successfully
```

### Failed Task (Reasoning Loop)
```
[2025-01-18 10:15:32] Task started: ecs_component_schemas
[2025-01-18 10:18:45] Agent reasoning (attempt 1/5)
[2025-01-18 10:22:10] Agent reasoning (attempt 2/5)
[2025-01-18 10:25:35] Agent reasoning (attempt 3/5)
[2025-01-18 10:29:00] Agent reasoning (attempt 4/5)
[2025-01-18 10:32:25] Agent reasoning (attempt 5/5)
[2025-01-18 10:35:50] Task failed: Max reasoning attempts exceeded
```

**Action**: Reduce `max_reasoning_attempts` for `ecs_architect` agent.

### Failed Task (API Error)
```
[2025-01-18 10:15:32] Task started: dfu_data_analysis
[2025-01-18 10:18:45] Fetching DFU data from web...
[2025-01-18 10:22:10] ERROR: HTTP 429 Rate Limit Exceeded
[2025-01-18 10:22:11] Task failed: API error
```

**Action**: Wait 5 minutes, restart task.

## Performance Optimization

### Reduce Task Duration

**Before**:
```yaml
# crew_config/agents.yaml
ecs_architect:
  max_reasoning_attempts: 5
  max_iter: 40
```

**After**:
```yaml
ecs_architect:
  max_reasoning_attempts: 3  # Faster decisions
  max_iter: 25               # Fewer iterations
```

### Parallel Execution Tips

- Run Batch 1 tasks together: `process-compose up ecs_component_schemas dfu_data_analysis`
- Monitor with: `watch -n 2 'process-compose process list'`
- Stop all: `process-compose down`

## References

- [crewai_usage.md](../architecture/crewai_usage.md) - Full usage guide
- [agents.yaml](../../crew_config/agents.yaml) - Agent configurations
- [tasks.yaml](../../crew_config/tasks.yaml) - Task definitions
