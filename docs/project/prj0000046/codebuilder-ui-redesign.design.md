# codebuilder-ui-redesign — Design Notes
_Agent: @3design | Status: COMPLETE_

## Component Architecture

```
CodeBuilder (React FC)
├── Pipeline Bar          — agent pills + Run/Stop/Reset
├── Sidebar               — agent list + system log strip
└── Main Panel
    ├── Panel Header      — icon + name + desc + LLM selector + tabs
    ├── Chat Tab          — message bubbles, mic, input, send
    ├── Logs Tab          — per-agent colour-coded lines, Clear, badge
    └── Doc Tab           — MarkdownView (preview) | <textarea> (edit)
                            + Edit/Preview toggle button
Status Bar                — idle/running · LLM label · listening · msg count
```

## Type Contracts

```typescript
type AgentId  = '0master'|'1project'|'2think'|'3design'|'4plan'|'5test'|'6code'|'7exec'|'8ql'|'9git';
type TabId    = 'chat' | 'logs' | 'doc';
type LlmId    = 'flm' | 'gpt41' | 'gpt5mini' | 'grok' | 'raptor';

interface ChatMessage { role: 'user'|'agent'; text: string; ts: string; }

interface AgentDef {
  id: AgentId; name: string; desc: string;
  icon: LucideIcon; color: string; docFile: string;
}
```

## State Design

| State | Type | Init |
|-------|------|------|
| `activeAgent` | `AgentId` | `'0master'` |
| `activeTab` | `TabId` | `'chat'` |
| `agentLlm` | `Record<AgentId, LlmId>` | all `'flm'` |
| `isRunning` | `boolean` | `false` |
| `messages` | `Record<AgentId, ChatMessage[]>` | greeting per agent |
| `inputText` | `Record<AgentId, string>` | all `''` |
| `agentDocs` | `Record<AgentId, string>` | all `''` (loaded async) |
| `docsLoading` | `Record<AgentId, boolean>` | all `true` |
| `docEditing` | `Record<AgentId, boolean>` | all `false` |
| `logs` | `string[]` | system init message |
| `agentLogs` | `Record<AgentId, string[]>` | all `[]` (loaded async) |
| `isListening` | `boolean` | `false` |

## API Contracts

### Backend (`backend/app.py`)

```
GET  /api/agent-doc/{agent_id}   → { content: string }
PUT  /api/agent-doc/{agent_id}   ← { content: string } → { status: "ok", path: string }
GET  /api/agent-log/{agent_id}   → { content: string }
PUT  /api/agent-log/{agent_id}   ← { content: string } → { status: "ok", path: string }
```

- `agent_id` validated against `_VALID_AGENT_IDS` frozenset before any fs operation.
- Docs stored at `.github/agents/<id>.agent.md`
- Logs stored at `docs/agents/<id>.log.md`

### Vite Dev Plugin (`web/vite.config.ts`)

`vite-agent-docs` plugin intercepts before the proxy:
```
GET  /api/agent-doc/:id  → fs.readFileSync('.github/agents/<id>.agent.md')
PUT  /api/agent-doc/:id  → fs.writeFileSync(...)
```
Validation: same `VALID` set (10 agent IDs). Returns `400` on unknown ID.

## `MarkdownView` Component Interface

```typescript
function MarkdownView({ content }: { content: string }): JSX.Element
```

Handles in one pass (no dependency):
- YAML frontmatter (`---` … `---`) → styled metadata card
- ATX headings h1/h2/h3
- Fenced code blocks (` ``` `)
- Bullet lists (`-` / `*`)
- Inline: bold (`**`), italic (`*`), backtick code (`` ` ``)
- Horizontal rules (`---`)
- Plain paragraphs

## `Assert-PortFree` Powershell Interface

```powershell
function Assert-PortFree {
    param([int]$Port, [string]$ServiceName)
    # Kills existing listener, waits 400 ms for OS socket release.
    # Exits script with code 1 if kill fails.
}
```

Called for `$RuntimePort`, `$BackendPort`, `$VitePort` before each `Start-DevWindow`.
