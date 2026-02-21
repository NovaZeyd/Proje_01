---
name: context-manager
description: Proactively manages conversation context limits, prevents context overflow, and maintains project continuity across sessions. Use when (1) context usage exceeds 60%, (2) starting long projects requiring multiple sessions, (3) needing to checkpoint/summarize conversation state, (4) working with large codebases or files, (5) conversation needs compaction or reset with memory preservation.
---

# Context Manager

Intelligent context management to prevent "context limit exceeded" errors and maintain project continuity.

## Core Principles

1. **Proactive > Reactive** - Act before hitting limits
2. **Memory Persistence** - Store critical info in files, not just context
3. **Checkpoint System** - Save state at major milestones
4. **Progressive Disclosure** - Load details only when needed

## Quick Actions

### Check Context Status
```
User: "Context durumum nedir?" or "/status"
→ Run session_status, report: "Context X%/262k (Y tokens) - SAFE/WARNING/CRITICAL"
```

### Checkpoint (Manual Trigger)
```
User: "CHECKPOINT" or "Checkpoint al"
→ 1. Summarize key decisions, code, state
→ 2. Write to memory/YYYY-MM-DD.md or MEMORY.md
→ 3. List files modified
→ 4. Confirm: "Checkpoint saved. Continuing..."
```

### Compact Now
```
User: "/compact"
→ Trigger immediate compaction
→ Report: "Compacted from X to Y tokens (-Z%)"
```

## Smart Workflows

### Starting Long Projects

**AUTO-INIT on new project:**
1. Create `PROJECT_NAME.md` in workspace root
2. Add header: `# Project: NAME | Started: DATE`
3. Create sections: ## Goal, ## Decisions, ## Files, ## Next Steps
4. Checkpoint every 30 min or 50k tokens

### Code Workflows

**When handling code >500 lines:**
1. Save to file immediately (don't keep in context)
2. Reference file path instead of showing code
3. Use `read` with offset/limit for specific sections

**File Organization Pattern:**
```
project-name/
├── src/           (code files)
├── docs/          (documentation)
├── memory/        (session summaries)
└── PROJECT.md     (master index)
```

### Sub-Agent Strategy

**For large tasks:**
1. Main agent: Keep high-level context only
2. Spawn sub-agent with specific scope
3. Sub-agent reports back with summary (not full output)
4. Store detailed results in files

**Sub-Agent Scope Template:**
- Task: Specific action (e.g., "Review auth module")
- Output: Summary + file path to detailed results

## Auto-Compaction Triggers

Context % → Action:
- **<60%** → Normal operation
- **60-70%** → Proactive: summarize recent turns, suggest file writes
- **70-80%** → Alert user, compact now, checkpoint
- **80%+** → Critical: immediate compaction + memory flush

## Memory System

### Daily Files: `memory/YYYY-MM-DD.md`
- Raw session logs
- Chronological notes
- Auto-created daily

### Master File: `MEMORY.md`
- Curated long-term memory
- Key decisions only
- Update weekly from daily files

### Project Files: `projects/[name]/memory.md`
- Project-specific context
- Checkpoints
- Technical decisions

## Scripts Reference

See [scripts/compact.py](scripts/compact.py) - Automatic context compaction helper

## Tavily Integration (optional)

For real-time search (if configured):
- Requires Tavily API key in config
- Set via: `tools.web.search.provider = "tavily"`
- Alternative: Use existing `web_search` with Brave

## Browser Control (Available)

- `browser` tool - Full browser automation
- Supports: n8n, web UIs, screenshot testing
- See: [references/browser-patterns.md](references/browser-patterns.md)

## Code Execution (Available)

- `exec` tool - Shell command execution
- Sandboxed mode available
- Use for: testing, building, running scripts
