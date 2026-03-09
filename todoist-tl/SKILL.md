---
name: todoist-tl
description: 当用户发送 "TL" 或 "tl" 时，自动获取今天到期的 Todoist 任务，并以 Markdown 列表形式返回。触发词：TL、tl、今日待办、今天任务。
---

# Todoist TL - 今日任务快捷指令

## 触发条件

用户发送以下任一内容时触发：
- `TL`
- `tl`
- `今日待办`
- `今天任务`

## 配置

需要设置 Todoist API Token：

```bash
export TODOIST_API_TOKEN='your_api_token_here'
```

获取 Token：
1. 打开 Todoist → 设置 → 整合 → API Token
2. 复制 Token 并设置环境变量

## 执行流程

1. 运行脚本获取今日到期任务：
   ```bash
   python3 /root/.openclaw/skills/todoist-tl/scripts/get_today.py
   ```

2. 将脚本输出直接返回给用户

## 输出格式示例

```
**今日待办 (6项)**

- (P1) 紧急任务A [逾期]
- (P2) 普通任务B
- (P4) 低优先级任务C
```

优先级说明：
- (P1) 最高优先级
- (P2) 高优先级
- (P3) 中优先级
- (P4) 最低/无优先级

## 注意事项

- 如果今天没有到期任务，返回：✅ 今天没有到期的任务
- 不需要询问确认，直接执行并返回结果
- **自动排除**：
  - 已完成任务
  - 子任务（有父任务的任务）
  - 无截止日期(due_date)的任务
- 逾期任务会标记「逾期」

## 技术实现

- 使用 Todoist REST API v1 (`/api/v1/tasks`)
- 支持分页获取（处理超过 50 个任务的情况）
- 脚本路径：`/root/.openclaw/skills/todoist-tl/scripts/get_today.py`