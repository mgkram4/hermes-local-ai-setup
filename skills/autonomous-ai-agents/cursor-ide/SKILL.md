---
name: cursor-ide
description: Work effectively with Cursor IDE - the AI-first code editor. Understand Cursor's agent mode, rules system, MCP integration, and how to create custom skills and rules for optimal AI-assisted development.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Cursor, IDE, AI-Coding, Rules, MCP, Agent-Mode, VSCode]
    related_skills: [claude-code, hermes-agent, vscode]
---

# Cursor IDE — AI-First Development Guide

[Cursor](https://cursor.com) is an AI-first code editor built on VS Code. This skill covers how to work effectively with Cursor's AI features, create custom rules, and integrate with Hermes Agent.

## Cursor Architecture

### Key Components

| Component | Purpose |
|-----------|---------|
| **Agent Mode** | Autonomous coding with file access, terminal, and tool use |
| **Ask Mode** | Read-only exploration and Q&A (no file modifications) |
| **Rules System** | Persistent AI instructions (`.cursor/rules/`, `AGENTS.md`) |
| **MCP Servers** | External tool integration via Model Context Protocol |
| **Composer** | Multi-file editing and project-wide changes |
| **Chat** | Conversational AI assistance |

### Cursor vs Claude Code

| Feature | Cursor | Claude Code |
|---------|--------|-------------|
| Base | VS Code fork | Standalone CLI |
| Interface | GUI IDE | Terminal TUI |
| Rules | `.cursor/rules/*.md`, `AGENTS.md` | `CLAUDE.md`, `.claude/rules/` |
| MCP | Built-in MCP support | `claude mcp add` |
| Modes | Agent, Ask, Edit | Interactive, Print |
| Best For | Visual development | CLI automation |

## Rules System

Cursor uses a hierarchical rules system to provide persistent context to the AI.

### Rule Locations

| Location | Scope | Purpose |
|----------|-------|---------|
| `.cursor/rules/*.md` | Project | Project-specific rules (git-tracked) |
| `AGENTS.md` | Project root | Primary project instructions |
| `~/.cursor/rules/*.md` | Global | Personal rules across all projects |
| Cursor Settings | Global | UI-configured rules |

### Creating Effective Rules

#### File: `.cursor/rules/coding-standards.md`

```markdown
# Coding Standards

## TypeScript
- Use strict mode (`"strict": true` in tsconfig)
- Prefer `interface` over `type` for object shapes
- Use `const` assertions for literal types
- Always specify return types on functions

## React
- Use functional components with hooks
- Prefer named exports over default exports
- Use React.FC sparingly (prefer explicit props typing)
- Keep components under 200 lines

## Testing
- Write tests alongside implementation
- Use descriptive test names: `it('should X when Y')`
- Mock external dependencies, not internal modules
```

#### File: `AGENTS.md`

```markdown
# Project: My App

## Overview
A Next.js 14 application with TypeScript, Tailwind CSS, and Prisma ORM.

## Architecture
- `/app` - Next.js App Router pages and layouts
- `/components` - Reusable React components
- `/lib` - Utility functions and shared logic
- `/prisma` - Database schema and migrations

## Commands
- `npm run dev` - Start development server
- `npm run build` - Production build
- `npm run test` - Run Jest tests
- `npm run lint` - ESLint + Prettier

## Conventions
- Use kebab-case for file names
- Use PascalCase for components
- Use camelCase for functions and variables
- Prefix hooks with `use`
- Prefix context providers with `Provider`

## Database
- Always create migrations for schema changes
- Use transactions for multi-table operations
- Index foreign keys and frequently queried fields
```

### Rule Best Practices

1. **Be Specific**: "Use 2-space indentation" not "Format code nicely"
2. **Include Examples**: Show the pattern you want, not just describe it
3. **Organize by Topic**: Separate rules into focused files
4. **Update Regularly**: Rules should evolve with the project
5. **Don't Duplicate**: Reference other rules instead of copying

## Agent Mode

Agent Mode gives Cursor autonomous capabilities to:
- Read and write files
- Execute terminal commands
- Search the codebase
- Make multi-file changes

### Enabling Agent Mode

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Navigate to "Features" → "Agent"
3. Enable "Agent Mode"
4. Configure allowed tools and permissions

### Agent Mode Prompts

Effective prompts for Agent Mode:

```
# Good: Specific and actionable
"Add error handling to all API routes in /app/api/. Wrap handlers in try-catch,
log errors with console.error, and return appropriate HTTP status codes."

# Good: Multi-step with clear outcome
"Refactor the authentication system:
1. Extract auth logic from pages into /lib/auth.ts
2. Create useAuth hook for client-side auth state
3. Add middleware for protected routes
4. Update all pages to use the new system"

# Bad: Vague
"Make the code better"

# Bad: Too broad
"Rewrite everything in TypeScript"
```

### Agent Mode Safety

Configure permissions in Cursor Settings:

```json
{
  "cursor.agent.allowedTools": ["read", "write", "search"],
  "cursor.agent.requireConfirmation": true,
  "cursor.agent.maxFilesPerOperation": 10
}
```

## MCP Integration

Cursor supports Model Context Protocol (MCP) for external tool integration.

### Configuring MCP Servers

#### File: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["@anthropic-ai/server-postgres"],
      "env": {
        "DATABASE_URL": "${env:DATABASE_URL}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/server-filesystem", "--root", "${workspaceFolder}"]
    }
  }
}
```

### Using MCP Tools

Once configured, MCP tools appear in Cursor's tool palette:

```
@github:issue://123           # Reference a GitHub issue
@postgres:query               # Execute a database query
@filesystem:read              # Read files via MCP
```

### Popular MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| `@modelcontextprotocol/server-github` | GitHub integration | `npx` |
| `@anthropic-ai/server-postgres` | PostgreSQL queries | `npx` |
| `@anthropic-ai/server-filesystem` | File operations | `npx` |
| `@anthropic-ai/server-puppeteer` | Browser automation | `npx` |
| `@anthropic-ai/server-memory` | Persistent memory | `npx` |

## Creating Cursor Skills

Cursor skills are markdown files that provide specialized knowledge.

### Skill Location

```
~/.cursor/skills/
├── my-skill/
│   └── SKILL.md
└── another-skill/
    ├── SKILL.md
    └── templates/
        └── example.md
```

### Skill Structure

```markdown
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
author: Your Name
---

# Skill Name

## Overview
What this skill helps with.

## When to Use
- Scenario 1
- Scenario 2

## Instructions
Step-by-step guidance for the AI.

## Examples
Concrete examples of usage.

## Templates
Reusable patterns and boilerplate.
```

### Skill Best Practices

1. **Single Responsibility**: One skill per domain
2. **Include Examples**: Show, don't just tell
3. **Provide Templates**: Reusable code snippets
4. **Document Triggers**: When should the AI use this skill?
5. **Version Control**: Track skill changes

## Keyboard Shortcuts

### Essential Shortcuts

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Open Chat | Cmd + L | Ctrl + L |
| Open Composer | Cmd + I | Ctrl + I |
| Toggle Agent Mode | Cmd + Shift + A | Ctrl + Shift + A |
| Accept Suggestion | Tab | Tab |
| Reject Suggestion | Esc | Esc |
| Next Suggestion | Alt + ] | Alt + ] |
| Previous Suggestion | Alt + [ | Alt + [ |
| Inline Edit | Cmd + K | Ctrl + K |
| Generate in Terminal | Cmd + K (in terminal) | Ctrl + K |

### Navigation

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Go to File | Cmd + P | Ctrl + P |
| Go to Symbol | Cmd + Shift + O | Ctrl + Shift + O |
| Go to Definition | F12 | F12 |
| Find References | Shift + F12 | Shift + F12 |
| Search Workspace | Cmd + Shift + F | Ctrl + Shift + F |

## Cursor + Hermes Integration

### Using Hermes from Cursor

When working in Cursor with Hermes Agent running:

1. **Hermes as MCP Server**: Configure Hermes as an MCP server for Cursor
2. **Shared Rules**: Sync rules between `.cursor/rules/` and Hermes skills
3. **Complementary Roles**: Use Cursor for visual editing, Hermes for automation

### Hermes MCP Configuration

```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"],
      "env": {
        "HERMES_HOME": "${env:HOME}/.hermes"
      }
    }
  }
}
```

### Workflow: Cursor + Hermes

```
1. Use Cursor for:
   - Visual code editing
   - Interactive debugging
   - Real-time AI suggestions
   - Multi-file refactoring

2. Use Hermes for:
   - Background automation
   - CLI-based workflows
   - Scheduled tasks
   - Multi-platform messaging
   - Long-running operations
```

## Troubleshooting

### Common Issues

#### AI Not Following Rules

1. Check rule file location (`.cursor/rules/` or `AGENTS.md`)
2. Ensure rules are specific and actionable
3. Restart Cursor to reload rules
4. Check for conflicting rules

#### MCP Server Not Connecting

1. Verify server is installed: `npx @server-name --version`
2. Check environment variables are set
3. Review Cursor's MCP logs (Output panel → MCP)
4. Test server manually: `npx @server-name`

#### Agent Mode Not Working

1. Ensure Agent Mode is enabled in settings
2. Check file permissions
3. Verify workspace trust settings
4. Review allowed tools configuration

### Debug Mode

Enable verbose logging:

```json
{
  "cursor.debug.enabled": true,
  "cursor.debug.logLevel": "verbose"
}
```

View logs: Help → Toggle Developer Tools → Console

## Best Practices

### For AI-Assisted Development

1. **Write Clear Commit Messages**: AI can learn from your history
2. **Use Descriptive Names**: Better names = better AI understanding
3. **Comment Complex Logic**: Help AI understand intent
4. **Keep Files Focused**: Smaller files = better context
5. **Update Rules Regularly**: Evolve rules with your project

### For Team Collaboration

1. **Share Rules via Git**: `.cursor/rules/` should be tracked
2. **Document Custom Skills**: Help teammates understand AI behavior
3. **Standardize MCP Config**: Use consistent server configurations
4. **Review AI Changes**: Always review before committing

### For Performance

1. **Limit Context Size**: Don't include entire codebase in prompts
2. **Use Specific References**: `@file.ts` instead of "the file"
3. **Break Large Tasks**: Smaller tasks = faster responses
4. **Cache MCP Results**: Avoid repeated expensive queries

## Resources

- **Cursor Documentation**: https://docs.cursor.com
- **Cursor Discord**: https://discord.gg/cursor
- **MCP Specification**: https://modelcontextprotocol.io
- **VS Code Docs**: https://code.visualstudio.com/docs (base editor)
