---
name: obsidian-morning-daily-note
description: 从模板创建当天的晨间日记，规范化日期标签，并在对应的 Obsidian 当日日记中添加双向链接。当用户要求创建、准备或撰写晨间日记、每日晨记，或开始当天记录时使用。
---

# Obsidian 晨间日记

从模板创建当天的晨间日记，规范化日期标签，并将其链接到对应的当日日记。整个流程直接读写文件，不自动打开 Obsidian 或新创建的文档。

## 前置条件

- 晨间日记模板存在：`templates/【模板】晨间日记.md`
- 当日日记模板存在：`templates/【模板】Habit Tracker - 上午.md`
- Vault 中存在 `journals/` 和 `journals-morning/` 目录

## 操作流程

### 1. 计算今天所需的日期格式

```bash
# 此技能使用的日期格式
TODAY_YYYYMMDD=$(date +%Y%m%d)     # 例如 20260417
TODAY_MMDD=$(date +%m%d)           # 例如 0417
TODAY_MONTH=$(date +%-m)           # 例如 4
TODAY_YYYYMM=$(date +%Y%m)         # 例如 202604
TODAY_DATE=$(date +%Y-%m-%d)       # 例如 2026-04-17
```

### 2. 检查晨间日记是否已存在

目标文件：`journals-morning/${TODAY_YYYYMMDD}.md`

如果文件已经存在，停止创建并告知用户：“今日晨间日记已存在，无需重复创建。”

### 3. 读取晨间日记模板

读取 `templates/【模板】晨间日记.md`。

### 4. 规范化日期标签

在模板 YAML frontmatter 的 `tags` 列表中：

- 删除所有匹配 `#day/NNNN` 的已有日期标签。
- 删除所有匹配 `N月` 或 `NN月` 的已有月份标签。
- 删除所有匹配 `yearAndmonth/NNNNNN` 的已有年月标签。
- 保留其他无关标签及其原有顺序。
- 将以下三个标签各添加一次：

  ```yaml
  tags:
    - ...其他原有标签...
    - "#day/MMDD"
    - M月
    - yearAndmonth/YYYYMM
  ```

将 `MMDD`、`M` 和 `YYYYMM` 分别替换为 `TODAY_MMDD`、`TODAY_MONTH` 和 `TODAY_YYYYMM`。例如，在 2026-07-13 添加 `#day/0713`、`7月` 和 `yearAndmonth/202607`。

执行日期是唯一可信的日期来源，不要把模板中过期的日期或月份标签复制到新笔记。

### 5. 写入晨间日记

将规范化后的模板内容写入：

```text
journals-morning/${TODAY_YYYYMMDD}.md
```

### 6. 确保当日日记存在

目标文件：`journals/${TODAY_DATE}.md`

如果目标文件不存在，读取 `templates/【模板】Habit Tracker - 上午.md`，并将模板内容直接写入目标文件。

不要运行 `obsidian daily`、`obsidian open`、`open` 或其他会启动 Obsidian、切换界面、自动打开新建文档的命令。此技能只在文件系统中创建和修改笔记。

创建或确认文件存在后，读取 `journals/${TODAY_DATE}.md`。

### 7. 在当日日记中链接晨间日记

查找当日日记中的 `## 晨间日记` 标题。

- 如果标题存在但下面还没有链接，添加：

  ```markdown
  ## 晨间日记
  - [[journals-morning/YYYYMMDD|晨间日记]]
  ```

- 如果标题下已经有指向同一晨间日记的链接，不做修改。
- 如果标题不存在，在笔记顶部附近添加标题和链接；如有 frontmatter，则放在 frontmatter 之后：

  ```markdown
  ## 晨间日记
  - [[journals-morning/YYYYMMDD|晨间日记]]
  ```

### 8. 向用户报告结果

简要说明：

- 已创建 `journals-morning/YYYYMMDD.md`
- 已规范化 `#day/MMDD`、`M月` 和 `yearAndmonth/YYYYMM` 标签
- 已创建或确认 `journals/YYYY-MM-DD.md` 存在
- 已在当日日记中添加晨间日记链接
- 整个过程未自动打开 Obsidian 文档
