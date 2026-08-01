---
name: today-tasks-add-to-obsidian
description: 初次准备 Obsidian 当日日记中的“每日计划”：调用统一同步流程写入 Calendar 日程、Things Today 待办并刷新 9 小时容量提醒。当用户说“准备今日待办”“把今天日程和待办写入日记”时使用；之后的刷新、增量更新或外部任务变更同步直接使用 sync-today-plan-to-obsidian。
---

# 准备今日待办

本 Skill 是初次准备入口。Calendar、Things、判重、格式、写入验证和容量提醒都以 `sync-today-plan-to-obsidian` 为唯一规范，不在这里维护第二套实现。

## 工作流程

1. 使用本机 `date +%Y-%m-%d` 定位 `journals/YYYY-MM-DD.md`。
2. 如果当日日记不存在，停止并建议先使用 `obsidian-morning-daily-note` 或 `start-today` 创建；不要自行复制模板。
3. 调用 `sync-today-plan-to-obsidian` 完成一次完整同步。Things 数据由该 Skill 统一通过 `things` CLI/Skill 读取。
4. 确认同步流程即使没有新增项目，也已重新计算计划工时并刷新受管容量提醒。
5. 透传同步结果，并把“首次新增”和“原本已同步”区分报告。

若同步流程报告 Calendar/Things 权限、命令、日记结构或写后验证错误，原样保留失败状态，不要把部分完成包装成完整成功。重复执行应为 no-op，且不得产生重复日程、待办或提醒。
