---
name: today-tasks-add-to-obsidian
description: 把当天的待办事项写入 Obsidian 当日日记，当我说准备今日待办的时候调用
---

## 命令执行要求

- 所有 `accli calendars` 和 `accli events` 命令必须直接在**非沙箱环境**运行，不要先在沙箱中尝试。
- 用户已授权这些 `accli` 命令在非沙箱环境运行，无需再次请求确认。
- 如果非沙箱执行仍返回 `NOT_AUTHORIZED`，再报告 macOS 日历权限问题；不得根据沙箱中的权限错误判断用户未授权日历。

## 工作流程

1. 使用 Apple Calendar CLI（`accli`）在非沙箱环境查询“工作”“个人”“吕波”三个日历的今日日程。
2. 将日程加工为：
   - `[日程开始时间～日程结束时间] 日程名称 日程地点 [时间花费]`
3. 使用 shell 的 `date` 确定当天日期，读取 `journals/yyyy-mm-dd.md`，把日程写入“每日计划”下“会议”的子节点。
4. 使用 `things-mac` skill 查询 Today。
5. 只使用 Things 返回结果的 `TITLE` 作为任务名称。
6. 把任务写入同一篇日记的“每日计划”下，放在“会议”节点之后。
