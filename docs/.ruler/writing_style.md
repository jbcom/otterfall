
# Documentation Writing Standards

## Structure

- Start with **Overview** section
- Use **## Heading** for major sections
- Use **### Subheading** for subsections
- Include **Next Steps** or **References** at end

## Code Examples

Always include:
- Language identifier in fenced code blocks
- Context comments explaining non-obvious patterns
- Both "Bad" and "Good" examples for anti-patterns

## Cross-References

### Internal Documentation Links
Use relative paths from current file:
```markdown
<!-- From docs/.ruler/writing_style.md -->
See [ECS Patterns](../../.ruler/ecs_patterns.md) for details.

<!-- From client/.ruler/rendering_pipeline.md -->
See [React Three Fiber Guidelines](../../.ruler/react_three_fiber.md).
```

### Code References
Link to specific files in the codebase:
```markdown
See [`world.ts`](../../client/src/ecs/world.ts) for Entity type definition.
```

### External Documentation
Use Context7 MCP tool for up-to-date library docs:
```markdown
<!-- Instead of linking to potentially outdated docs -->
Consult latest React Three Fiber documentation via Context7.
```

## Clarity

- Write in present tense
- Use active voice
- Avoid unnecessary jargon
- Define acronyms on first use
