# Troubleshooting Flow

Decision trees for diagnosing Claude Code issues.

## Extension Not Working

```
Extension not working?
│
├─ What type?
│  │
│  ├─ Skill ─────────────► Go to: Skill Debugging Flow
│  ├─ Hook ──────────────► Go to: Hook Debugging Flow
│  ├─ Agent ─────────────► Go to: Agent Debugging Flow
│  ├─ Command ───────────► Go to: Command Debugging Flow
│  └─ MCP ───────────────► Go to: MCP Debugging Flow
```

## Skill Debugging Flow

```
Skill not activating?
│
├─ Does directory exist?
│  ├─ No ──► Create: mkdir -p .claude/skills/my-skill
│  └─ Yes
│      │
│      ├─ Does SKILL.md exist (exact case)?
│      │  ├─ No ──► Create SKILL.md (not skill.md)
│      │  └─ Yes
│      │      │
│      │      ├─ Does frontmatter start with ---?
│      │      │  ├─ No ──► Add --- at line 1
│      │      │  └─ Yes
│      │      │      │
│      │      │      ├─ Does frontmatter end with ---?
│      │      │      │  ├─ No ──► Add --- after last field
│      │      │      │  └─ Yes
│      │      │      │      │
│      │      │      │      ├─ Does name: match directory?
│      │      │      │      │  ├─ No ──► Fix name to match
│      │      │      │      │  └─ Yes
│      │      │      │      │      │
│      │      │      │      │      ├─ Does description have triggers?
│      │      │      │      │      │  ├─ No ──► Add "Triggers on: x, y, z"
│      │      │      │      │      │  └─ Yes
│      │      │      │      │      │      │
│      │      │      │      │      │      └─ Try: claude --debug
│      │      │      │      │      │         Look for skill loading errors
```

## Hook Debugging Flow

```
Hook not running?
│
├─ Is script executable?
│  ├─ No ──► chmod +x script.sh
│  └─ Yes
│      │
│      ├─ Is settings.json valid JSON?
│      │  ├─ No ──► Fix JSON syntax (jq '.' to validate)
│      │  └─ Yes
│      │      │
│      │      ├─ Is matcher correct? (case-sensitive!)
│      │      │  ├─ "bash" ──► Change to "Bash"
│      │      │  └─ Correct
│      │      │      │
│      │      │      ├─ Does path exist?
│      │      │      │  ├─ No ──► Fix path, use $CLAUDE_PROJECT_DIR
│      │      │      │  └─ Yes
│      │      │      │      │
│      │      │      │      ├─ Does script work manually?
│      │      │      │      │  │  echo '{"tool_name":"X"}' | ./script.sh
│      │      │      │      │  │
│      │      │      │      │  ├─ Fails ──► Fix script errors
│      │      │      │      │  └─ Works
│      │      │      │      │      │
│      │      │      │      │      └─ Run: /hooks
│      │      │      │      │         Is hook listed?
│      │      │      │      │         ├─ No ──► Check settings location
│      │      │      │      │         └─ Yes ──► Try claude --debug
```

## Agent Debugging Flow

```
Agent not being used?
│
├─ Is file in correct location?
│  ├─ ~/.claude/agents/name.md (user)
│  ├─ .claude/agents/name.md (project)
│  │
│  ├─ Wrong location ──► Move file
│  └─ Correct
│      │
│      ├─ Does filename match name: field?
│      │  ├─ No ──► Rename file or fix name field
│      │  └─ Yes
│      │      │
│      │      ├─ Does description include "Use for:"?
│      │      │  ├─ No ──► Add: "Use for: scenario1, scenario2"
│      │      │  └─ Yes
│      │      │      │
│      │      │      ├─ Run: /agents
│      │      │      │  Is agent listed?
│      │      │      │  │
│      │      │      │  ├─ No ──► Check YAML frontmatter syntax
│      │      │      │  └─ Yes
│      │      │      │      │
│      │      │      │      └─ Try explicit request:
│      │      │      │         "Use the my-agent agent for this"
```

## Command Debugging Flow

```
Command not working?
│
├─ Is file in correct location?
│  ├─ ~/.claude/commands/name.md (user)
│  ├─ .claude/commands/name.md (project)
│  │
│  ├─ Wrong location ──► Move file
│  └─ Correct
│      │
│      ├─ Does /command-name show in help?
│      │  ├─ No ──► Check YAML frontmatter
│      │  └─ Yes
│      │      │
│      │      └─ Command runs but fails?
│      │         ├─ Check instructions in command file
│      │         └─ Verify required tools are available
```

## MCP Debugging Flow

```
MCP server not connecting?
│
├─ Is server installed?
│  │  npx @modelcontextprotocol/server-X
│  │
│  ├─ "not found" ──► npm install -g @modelcontextprotocol/server-X
│  └─ Runs
│      │
│      ├─ Is server in .mcp.json?
│      │  ├─ No ──► Add server config or use: claude mcp add
│      │  └─ Yes
│      │      │
│      │      ├─ Are env vars set?
│      │      │  │  Check ${VAR} references in .mcp.json
│      │      │  │
│      │      │  ├─ Missing ──► Set env vars or add to .env
│      │      │  └─ Set
│      │      │      │
│      │      │      ├─ Is transport correct?
│      │      │      │  │  HTTP servers need --transport http
│      │      │      │  │
│      │      │      │  ├─ Wrong ──► Fix transport config
│      │      │      │  └─ Correct
│      │      │      │      │
│      │      │      │      └─ Try: claude --debug
│      │      │      │         Look for MCP connection errors
```

## Permission Debugging Flow

```
Tool blocked unexpectedly?
│
├─ Check deny rules first
│  │  jq '.permissions.deny' ~/.claude/settings.json
│  │
│  ├─ Tool in deny ──► Remove from deny list
│  └─ Not in deny
│      │
│      ├─ Check allow rules
│      │  │  jq '.permissions.allow' ~/.claude/settings.json
│      │  │
│      │  ├─ Tool not in allow ──► Add to allow list
│      │  └─ In allow
│      │      │
│      │      ├─ Is pattern correct?
│      │      │  │  "Bash(git:*)" allows only git commands
│      │      │  │
│      │      │  ├─ Pattern too narrow ──► Broaden pattern
│      │      │  └─ Pattern correct
│      │      │      │
│      │      │      ├─ Check PreToolUse hooks
│      │      │      │  │  /hooks
│      │      │      │  │
│      │      │      │  ├─ Hook blocking ──► Fix hook logic
│      │      │      │  └─ No blocking hook
│      │      │      │      │
│      │      │      │      └─ Run: claude --debug
│      │      │      │         Check permission decision logs
```

## General Debugging Checklist

When all else fails:

1. Run `claude --debug` and read output carefully
2. Verify file locations and names
3. Validate all JSON with `jq '.'`
4. Check YAML frontmatter syntax
5. Test components in isolation
6. Check file permissions (`ls -la`)
7. Verify environment variables
8. Review recent changes to config
9. Try with a fresh session
10. Check Claude Code version (`claude --version`)
