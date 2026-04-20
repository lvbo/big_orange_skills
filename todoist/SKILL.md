---
name: todoist
description: Manage tasks and projects in Todoist. Use when user asks about tasks, to-dos, reminders, or productivity.
homepage: https://todoist.com
metadata:
  clawdbot:
    emoji: "✅"
    requires:
      bins: ["todoist"]
      env: ["TODOIST_API_TOKEN"]
---

# Todoist CLI

CLI for Todoist task management, built on the official TypeScript SDK.

## Installation

```bash
# Requires todoist-ts-cli >= 0.2.0 (for --top / --order)
npm install -g todoist-ts-cli@^0.2.0
```

## Setup

1. Get API token from https://todoist.com/app/settings/integrations/developer
2. Either:
   ```bash
   todoist auth <your-token>
   # or
   export TODOIST_API_TOKEN="your-token"
   ```

## Output Format

When querying tasks, use TL-style format:

**Step 1:** Get tasks in JSON format
```bash
todoist tasks --json
# or
todoist today --json
```

**Step 2:** Format output as TL-style

Parse the JSON and output in this format:
```
**今日待办 (N项)**

- (P1)任务名称A
- (P2)任务名称B [逾期]
- (P4)任务名称C

💡 **建议**: 有 X 项任务已逾期，建议优先处理。共有 Y 项高优先级(P1/P2)任务待完成。
```

**Formatting Rules:**
1. **Priority Prefix**: Map Todoist priority to TL format
   - Todoist priority 4 → `(P1)` Highest
   - Todoist priority 3 → `(P2)` High
   - Todoist priority 2 → `(P3)` Medium
   - Todoist priority 1 → `(P4)` Lowest
   - Format: `(P1)任务名称` (no space)

2. **Overdue Marking**: Show `[逾期]` suffix for overdue tasks
   - Compare task's due.date with today's date
   - Format: `(P2)任务名称 [逾期]`

3. **Sort Order**: Sort by priority (P1 first, P4 last), then by due date

4. **Suggestion**: Always include 💡 **建议** section:
   - Count overdue tasks
   - Count high priority (P1/P2) tasks
   - Give context-aware recommendation

## Commands

### Tasks (TL Format)

When user asks for tasks, use `--json` and format output:

```bash
# Get today's tasks and format
todoist today --json | python3 -c "
import json, sys, datetime
from datetime import date

today = date.today()
data = json.load(sys.stdin)
tasks = data if isinstance(data, list) else data.get('results', [])

# Filter and process tasks
processed = []
for t in tasks:
    content = t.get('content', '').strip()
    if not content:
        continue
    
    # Map priority (4->P1, 3->P2, 2->P3, 1->P4)
    p_map = {4: 'P1', 3: 'P2', 2: 'P3', 1: 'P4'}
    priority = p_map.get(t.get('priority', 1), 'P4')
    
    # Check overdue
    due = t.get('due')
    is_overdue = False
    if due and due.get('date'):
        try:
            due_date = datetime.datetime.strptime(due['date'][:10], '%Y-%m-%d').date()
            is_overdue = due_date < today
        except:
            pass
    
    processed.append({
        'content': content,
        'priority': priority,
        'is_overdue': is_overdue
    })

# Sort by priority (P1 < P2 < P3 < P4)
p_order = {'P1': 0, 'P2': 1, 'P3': 2, 'P4': 3}
processed.sort(key=lambda x: p_order.get(x['priority'], 4))

# Output
print(f'**今日待办 ({len(processed)}项)**')
print()
for t in processed:
    overdue_mark = ' [逾期]' if t['is_overdue'] else ''
    print(f\"- ({t['priority']}){t['content']}{overdue_mark}\")

# Stats
overdue_count = sum(1 for t in processed if t['is_overdue'])
high_priority = sum(1 for t in processed if t['priority'] in ['P1', 'P2'])

print()
print(f'💡 **建议**: ', end='')
if overdue_count > 0:
    print(f'有 {overdue_count} 项任务已逾期，建议优先处理。', end='')
if high_priority > 0:
    print(f'共有 {high_priority} 项高优先级(P1/P2)任务待完成。')
"
```

### Add Tasks

```bash
todoist add "Buy groceries"
todoist add "Meeting" --due "tomorrow 10am"
todoist add "Review PR" --due "today" --priority 1 --project "Work"
todoist add "Prep slides" --project "Work" --order 3  # add at a specific position (1-based)
todoist add "Triage inbox" --project "Work" --order top  # add to top
todoist add "Call mom" -d "sunday" -l "family"  # with label
```

### Manage Tasks

```bash
todoist view <id>          # View task details
todoist done <id>          # Complete task
todoist reopen <id>        # Reopen completed task
todoist update <id> --due "next week"
todoist move <id> -p "Personal"
todoist delete <id>
```

### Search

```bash
todoist search "meeting"
```

### Projects & Labels

```bash
todoist projects           # List projects
todoist project-add "New Project"
todoist labels             # List labels
todoist label-add "urgent"
```

### Comments

```bash
todoist comments <task-id>
todoist comment <task-id> "Note about this task"
```

## Usage Examples

**User: "TL" or "今天任务" or "今日待办"**
```bash
todoist today --json | python3 -c "[format script above]"
```

**User: "todoist tasks"**
```bash
todoist tasks --json | python3 -c "[format script above]"
```

**User: "Add 'buy milk' to my tasks"**
```bash
todoist add "Buy milk" --due "today"
```

**User: "Remind me to call the dentist tomorrow"**
```bash
todoist add "Call the dentist" --due "tomorrow"
```

**User: "Mark the grocery task as done"**
```bash
todoist search "grocery"   # Find task ID
todoist done <id>
```

**User: "What's on my work project?"**
```bash
todoist tasks -p "Work" --json | python3 -c "[format script above]"
```

**User: "Show my high priority tasks"**
```bash
todoist tasks -f "p1" --json | python3 -c "[format script above]"
```

## Filter Syntax

Todoist supports powerful filter queries:
- `p1`, `p2`, `p3`, `p4` - Priority levels
- `today`, `tomorrow`, `overdue`
- `@label` - Tasks with label
- `#project` - Tasks in project
- `search: keyword` - Search

## Notes

- Task IDs are shown in task listings
- Due dates support natural language ("tomorrow", "next monday", "jan 15")
- Priority 1 is highest, 4 is lowest in Todoist API
- TL format maps: 4→P1, 3→P2, 2→P3, 1→P4
- Use `--json` for structured output that can be formatted
