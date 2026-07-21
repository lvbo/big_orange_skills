---
name: obsidian-morning-daily-note
description: Create a morning journal note from a template, normalize its daily and current-month tags, and link it from the corresponding daily note. Use when the user asks to create, prepare, or write a morning journal (晨间日记), daily morning note, or similar.
---

# Obsidian Morning Daily Note

Create a morning journal note from a template, normalize its date tags, and link it from the corresponding daily note.

## Prerequisites

- Obsidian CLI is installed and configured (`obsidian version` works)
- Template file exists at `/templates/【模板】晨间日记.md`
- Vault has `journals/` and `journals-morning/` folders

## Procedure

### 1. Compute today's date keys

```bash
# Date formats used by this skill
TODAY_YYYYMMDD=$(date +%Y%m%d)    # e.g. 20260417
TODAY_MMDD=$(date +%m%d)          # e.g. 0417
TODAY_MONTH=$(date +%-m)          # e.g. 4
TODAY_YYYYMM=$(date +%Y%m)        # e.g. 202604
TODAY_UNDERSCORE=$(date +%Y_%m_%d) # e.g. 2026_04_17
```

### 2. Check if morning journal already exists

Target file: `journals-morning/${TODAY_YYYYMMDD}.md`

If the file already exists, stop and inform the user: "今日晨间日记已存在，无需重复创建。"

### 3. Read the template

Read the file at `/templates/【模板】晨间日记.md`.

### 4. Normalize date tags

In the template's YAML frontmatter `tags` list:

- Remove every existing day tag matching `#day/NNNN`.
- Remove every existing Chinese month tag matching `N月` or `NN月`.
- Remove every existing year-month tag matching `yearAndmonth/NNNNNN`.
- Preserve all unrelated tags and their order.
- Add these three tags exactly once:

  ```yaml
  tags:
    - ...unrelated existing tags...
    - "#day/MMDD"
    - M月
    - yearAndmonth/YYYYMM
  ```

Replace `MMDD`, `M`, and `YYYYMM` with `TODAY_MMDD`, `TODAY_MONTH`, and `TODAY_YYYYMM`. For example, on 2026-07-13 add `#day/0713`, `7月`, and `yearAndmonth/202607`.

Do not copy stale month tags from the template into the generated note. Treat the execution date as the source of truth.

### 5. Write the morning journal

Write the modified content to:

```
journals-morning/${TODAY_YYYYMMDD}.md
```

### 6. Ensure the daily note exists

Target daily note: `journals/${TODAY_UNDERSCORE}.md`

If it does not exist, create it by running:

```bash
obsidian daily
```

Then read `journals/${TODAY_UNDERSCORE}.md`.

### 7. Link the morning journal in the daily note

Find the `## 晨间日记` heading in the daily note.

- If the heading exists but has no link yet, add a bullet under it:
  ```markdown
  ## 晨间日记
  - [[journals-morning/YYYYMMDD|晨间日记]]
  ```
- If the heading already contains a link to the same morning journal file, do nothing.
- If the heading does not exist, prepend it near the top of the note (after frontmatter if any) with the link:
  ```markdown
  ## 晨间日记
  - [[journals-morning/YYYYMMDD|晨间日记]]
  ```

### 8. Report to user

Summarize what was done:
- Created `journals-morning/YYYYMMDD.md`
- Normalized `#day/MMDD`, `M月`, and `yearAndmonth/YYYYMM` tags
- Updated `journals/YYYY-MM-DD.md` with a back-link
