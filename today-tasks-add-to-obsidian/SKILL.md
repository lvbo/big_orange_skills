---
name: today-tasks-add-to-obsidian
description: 把当天的待办事项写入 Obsidian 当日日记，当我说准备今日待办的时候调用
---

## 工作流程
1. 使用 Apple Calendar CLI (accli) skill 查询"工作"、"个人"、"吕波"三个日历的今日日程
2. 返回结果做如下加工
  - [日程开始时间～日程结束时间] 日程名称 日程地点 [时间花费]
3. 返回结果写入日记的"每日计划"下面，\- 会议 的子节点下
  - 查询当日是哪天，使用shell脚本的`date`
  - 在`journals`目录下读取对应日期的日记，日记文件的命名格式`yyyy-mm-dd`
3. 使用 thins-mac skill 查询 Today
4. 返回结果只使用 TITLE 做为任务名称
5. 返回结果写入日记的"每日计划"下面，\- 会议 的后面
  - 查询当日是哪天，使用shell脚本的`date`
  - 在`journals`目录下读取对应日期的日记，日记文件的命名格式`yyyy-mm-dd`