---
name: todoist-tl
description: Manages Todoist tasks and daily reviews. Use when user sends "TL", "今日待办", "今天任务" for today's tasks, or "TL done", "昨天完成的任务" for completed tasks. Also triggers on daily automated reports.
metadata:
  author: Claude Assistant
  version: 2.0.0
  category: productivity
  tags: [todoist, task-management, productivity, daily-review]
---

# Todoist TL

Quick access to Todoist tasks and automated daily reviews with pomodoro tracking.

## When to Use

- User sends `TL`, `tl`, `今日待办`, `今天任务`, or `今天待办` → Show today's due tasks
- User asks about completed tasks (`TL done`, `昨天完成的任务`, `今天完成的任务`, `本周完成的任务`) → Show completed tasks
- Daily automated runs at 9:00 AM and 10:00 PM

## Instructions

### Query Today's Tasks

When user sends trigger phrases (TL, 今日待办, 今天任务, 今天待办):

1. Run the today task script:
   ```bash
   python3 /root/.openclaw/skills/todoist-tl/scripts/get_today.py
   ```

2. Return output directly to user following the exact format specified in "Output Format" section:
   - Priority prefix directly attached: `(P1)任务名称`
   - Overdue tasks marked with `[逾期]`
   - Flat list (no priority grouping)
   - Include final 💡 **建议** section

3. If no tasks: return "✅ 今天没有到期的任务"

### Query Completed Tasks

When user asks for completed tasks:

1. Determine time range from user query:
   - `yesterday` / `昨天` → yesterday
   - `today` / `今天` → today
   - `week` / `本周` → last 7 days
   - Number (N) → last N days

2. Run completed task script:
   ```bash
   python3 /root/.openclaw/skills/todoist-tl/scripts/get_completed.py [time_range]
   ```

3. Return output directly

### Daily Review Generation

For automated daily reviews (10:00 PM), pushed to Telegram:

1. Run yesterday's review:
   ```bash
   bash /root/.openclaw/skills/todoist-tl/scripts/run_daily_review.sh
   ```

2. Report is automatically sent to Telegram

## Configuration

**Required Environment Variable:**
```bash
export TODOIST_API_TOKEN='your_api_token_here'
```

**Get Token:**
1. Open Todoist → Settings → Integrations → API Token
2. Copy token and set as environment variable

## Output Format

### Today's Tasks Format Requirements

When outputting today's tasks, follow these exact formatting rules:

```
**今日待办 (N项)**

- (P1)任务名称A
- (P2)任务名称B [逾期]
- (P4)任务名称C [逾期]

💡 **建议**: [context-aware suggestion]
```

**Formatting Rules:**
1. **Priority Prefix**: Must be directly attached to task name
   - `(P1)` = Highest priority (Todoist priority 4)
   - `(P2)` = High priority (Todoist priority 3)
   - `(P3)` = Medium priority (Todoist priority 2)
   - `(P4)` = Lowest/no priority (Todoist priority 1)
   - Format: `(P1)任务名称` (no space between priority and task)

2. **Overdue Marking**: Show `[逾期]` suffix for overdue tasks
   - Format: `(P2)任务名称 [逾期]`

3. **No Categorization**: Do NOT group by priority levels. List all tasks in a single flat list, sorted by priority (P1 first, P4 last).

4. **Final Suggestion**: Always end with a 💡 **建议** section that includes:
   - Count of overdue tasks if any
   - Count of high priority (P1/P2) tasks
   - Context-aware recommendation

**Example Output:**
```
**今日待办 (10项)**

- (P1)继续沟通AI研发出题的事情
- (P2)没有FR的需求补一下FR流程🍅 #01-Projects（工作） [逾期]
- (P2)AI研发大赛出题-正式版🍅🍅🍅🍅
- (P4)B：基础信息相关文档登记 🍉 [逾期]
- (P4)取消规则/权益库存等DB一致性监控-调研一下🍅🍅🍅 [逾期]
- (P4)酒店研发业务架构图-改下位置的事情-和梁老师沟通一下🍅
- (P4)搭建测试账号使用看板🍅🍅 [逾期]
- (P4)开启资源调节器看一下什么事情🍅 [逾期]
- (P4)和贤姐、阳姐他们聊一下第一阶段-QA阶段可以做的事情🍉 [逾期]
- (P4)酒店风控组加入AI研发的事情🍉 [逾期]

💡 **建议**: 有 7 项任务已逾期，建议优先处理。共有 3 项高优先级(P1/P2)任务待完成。
```

### Daily Review
```
📊 **2026-03-09 (周一) 日回顾**

📈 总体情况
- 截止日期任务: 2 个
- 实际完成: 1 个
- 完成率: 50.0%
- 实际用时: 1小时15分钟
- 预估用时: 1小时40分钟
- 偏差: -25分钟 ⬇️

✅ 已完成任务 (1项)
✅ (P1) AI Coding大赛出题-初版 [17:48]
   🍅 预估: 1小时40分钟 | 🥔 实际: 1小时15分钟
   ✨ 提前: -25分钟

⬜ 未完成/逾期任务 (1项)
⬜ 取消规则/权益库存等DB一致性监控-调研一下
   预估: 25分钟
```

## Pomodoro Symbols

| Symbol | Meaning | Time |
|--------|---------|------|
| 🍅 | Estimated work | 25 min |
| 🍉 | Estimated work | 15 min |
| 🥔 | Completed | 25 min |
| 🍠 | Completed | 15 min |

## Examples

### Example 1: Today's Tasks
**User:** "TL"

**Action:**
1. Run `get_today.py`
2. Return formatted task list

**Result:** Shows all tasks due today, sorted by priority

### Example 2: Yesterday's Completed Tasks
**User:** "昨天完成的任务"

**Action:**
1. Parse as "yesterday"
2. Run `get_completed.py yesterday`
3. Return completed tasks with timestamps

**Result:**
```
**昨天已完成任务 (3项)**
- (P1) Task A [11:30]
- (P2) Task B [10:15]
```

### Example 3: Daily Review
**Automated at 22:00**

**Action:**
1. Run `yesterday_review.py yesterday`
2. Include calendar events (if configured)
3. Send full report

**Result:** Complete daily summary with stats

## Important Notes

**CRITICAL:** 
- Auto-exclude completed tasks, subtasks, and tasks without due dates
- Mark overdue tasks with 「逾期」
- Use Beijing timezone (UTC+8) for all date calculations
- For recurring tasks: API may not return all completed instances

## Error Handling

### API Token Missing
**Error:** "❌ 未配置 Todoist API Token"

**Solution:**
1. Verify environment variable is set
2. Check token validity in Todoist settings

### No Tasks Found
**Behavior:** Return "✅ 今天没有到期的任务"

### API Connection Failed
**Behavior:** Return error message with suggestion to check network/token

## Technical Details

**API Endpoints:**
- Today's tasks: `GET /api/v1/tasks`
- Completed tasks: `GET /api/v1/tasks/completed/by_completion_date`

**Scripts:**
- `get_today.py` - Today's due tasks
- `get_completed.py` - Completed tasks by date
- `daily_review.py` - Full daily review with calendar (optional)
- `get_calendar.py` - Apple Calendar integration (optional)

**Features:**
- Automatic pagination (handles 200+ tasks)
- Timezone-aware (Asia/Shanghai)
- Pomodoro time tracking
- Calendar integration (optional, requires ICLOUD_USERNAME and ICLOUD_APP_PASSWORD)

## Scheduled Tasks

- **9:00 AM Daily:** Push today's tasks to Telegram
- **10:00 PM Daily:** Send daily review report to Telegram

Configure via cron jobs with skill scripts.
