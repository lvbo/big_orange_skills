---
name: llm-wiki
description: 维护 Obsidian 中从 raw/ 到 wiki/ 的 LLM Wiki 编译层，并基于 wiki 做有出处的知识问答或健康检查。用户要求处理/摄取 raw 原始资料、更新 wiki 摘要/概念/实体/索引、基于知识库回答问题，或检查 wiki 的断链、重复概念和内容健康度时使用；普通日记、计划、周月回顾和仅编辑 pages-ai 的任务不要触发。
---

# LLM Wiki

把 `raw/` 视为只读源数据，把 `wiki/` 视为可重复生成和增量维护的知识编译层。使用 PARA 页面作为关联上下文，但不要把本 Skill 扩展成通用 Obsidian 编辑器。

## 边界与不变量

- `raw/` 只读：不得修改、移动、重命名、删除其中的文件，也不得向原文补 frontmatter。
- `wiki/` 由 LLM 维护：允许创建和更新摘要、概念、实体、索引与 `wiki/log.md`。
- `outputs/qa/`、`outputs/health/` 只在对应模式明确要求落盘时写入。
- `pages-ai/` 是混合维护区：可以读取并从 wiki 页面链接到已有页面；只有用户明确要求时才修改 `pages-ai/`。
- 所有事实都应能追溯到 `raw/` 中的来源。不能从来源确认的内容标记为“待验证”，不要写成确定事实。

## 模式选择

先根据用户意图选择一种模式；不要因为“每周”到了就自动执行任何任务。

1. **Ingest（摄取）**：用户要求处理 `raw/` 中一个或多个文件、编译新资料或更新 wiki。
2. **Query（问答）**：用户要求基于自己的 wiki/资料回答问题。默认只读回答；只有用户明确说“保存、沉淀、写入”时才写 `outputs/qa/` 或日志。
3. **Lint（健康检查）**：用户明确要求检查、诊断或修复 wiki。Lint 不具备自动调度能力，“每周检查”只是用户可另行安排的触发方式。

若意图不明确，优先执行无写入的 Query；不要擅自把普通笔记编辑转换成 Ingest。

## 来源身份与命名

### 稳定来源 ID

- `source_id` 使用原文件相对 Vault 根目录的 POSIX 路径，例如 `raw/articles/example.md`。
- 同一文件重复摄取始终使用相同 `source_id`。文件内容变化不改变 ID。
- URL、标题、作者只能作为元数据，不能替代本地来源的 `source_id`。
- 若用户提供的是 `raw/` 下多个同名文件，依靠完整相对路径区分。

### 文件名

- 摘要文件优先使用 `{来源类型}-{原文件名去扩展名}.md`，例如 `articles-example.md`。
- 如果该名称已被不同 `source_id` 占用，在文件名后追加 `sha256(source_id 的 UTF-8 字节)` 的前 8 位小写十六进制。后续重跑通过 frontmatter 中的 `source_id` 定位原页面，不再次改名。
- 概念和实体文件使用最常用、最明确的规范名称；中文名称保留中文，英文名称使用通行大小写，不强制全部 kebab-case。
- 文件名中的 `/ : * ? " < > |` 替换为 `-`，压缩重复空格与连字符。

## 页面规范

### 摘要页 `wiki/summaries/`

```yaml
---
title: "文章原标题"
source_id: "raw/articles/example.md"
source_url: "原始 URL（如有）"
author: "作者（如有）"
published: "YYYY-MM-DD（如能确认）"
ingested: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
description: "一句话描述"
tags:
  - source
  - 领域标签
---
```

```markdown
## 核心结论

1-3 条核心观点。

## 关键证据

- 证据，以及它支持的结论。

## 重要概念

- [[概念名]]

## 相关实体

- [[实体名]]

## 疑点与待验证

- 无则写“暂无”。

## 相关来源

- [[其他摘要]]
```

### 概念页 `wiki/concepts/`

```yaml
---
title: "概念名"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - concept
sources:
  - "raw/articles/example.md"
aliases: []
---
```

```markdown
## 定义

## 关键特征

## 证据与例子

每条证据注明来源摘要链接。

## 相关概念

## 相关项目与领域

仅链接已存在的 `pages-ai/01-projects/` 或 `pages-ai/02-areas/` 页面。

## 矛盾与争议
```

### 实体页 `wiki/entities/`

```yaml
---
title: "实体名"
type: "person|company|product|book|tool|other"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - entity
  - 类型标签
sources:
  - "raw/articles/example.md"
aliases: []
---
```

```markdown
## 简介

用来源可支持的事实说明该实体是什么。

## 关键信息

- 事实 — [[来源摘要]]

## 与我的知识库的关系

- [[相关概念]]、[[相关项目或领域]]

## 争议与待验证

- 无则写“暂无”。

## 来源

- [[来源摘要]]
```

### 索引页 `wiki/indexes/`

索引至少包含 `title`、`updated` frontmatter。索引项只保留一个规范 wikilink；新增时判重，删除失效链接，排序规则保持文件原有风格。不要把同一页面的别名链接重复列入。

## Ingest 工作流

1. 解析用户指定范围，只读取 `raw/` 中目标文件及其明确引用的 `assets/` 附件。未指定范围时先列出候选，不要默认重编整个 `raw/`。
2. 为每个来源计算 `source_id`，检索 `wiki/summaries/` 中相同 `source_id` 的页面；存在则原位更新，不存在才创建。兼容旧页面时，只有能通过旧摘要中的唯一原始路径或 URL 明确映射到一个 `source_id` 时才补写该字段；多个候选时停止并报告，不创建第二份或猜测迁移。
3. 生成或更新摘要。保留 `ingested` 初次日期；只有正文或其他实质元数据发生变化时才更新 `updated`，完全相同的重跑保持文件字节不变。没有证据的元数据留空，不猜测。
4. 提取真正值得复用的概念与实体。先按标题、aliases 和语义检查是否已有页面，避免同义词分裂成重复页面。
5. 更新概念/实体时：
   - `sources` 按 `source_id` 去重；
   - 证据按“事实 + 来源摘要”去重；
   - 保留已有来源仍支持的内容；若新旧来源冲突，记录到“矛盾与争议”，不要静默覆盖。
6. 更新 `All-Sources.md`、`All-Concepts.md`、`All-Entities.md`。只添加缺失链接，不重复追加。
7. 仅当持久化内容确实改变时，在 `wiki/log.md` 追加一次操作记录。记录 `source_id`、新增/更新页面和关键变化；完全相同的重跑不追加日志。
8. 复读所有写入文件，验证 YAML 可读、内部链接目标合理、`source_id` 正确、索引无重复、`raw/` 未变化。失败时修正后再汇报。

## Query 工作流

1. 先检索 `wiki/indexes/`，再读取相关摘要、概念和实体；必要时回到对应 `raw/` 原文核对。
2. 基于实际读到的内容回答，使用 `[[页面名]]` 标出知识库依据；证据不足时明确说明缺口。
3. 默认不写文件、不更新日志。只有用户明确授权“保存/沉淀本次回答”时才落盘。规范化问题文本时依次执行 Unicode NFC、去除首尾空白、把连续空白折叠为一个 ASCII 空格；`question_id` 为该 UTF-8 文本的 SHA-256 前 12 位小写十六进制。
4. 写入前先扫描 `outputs/qa/` frontmatter 中的 `question_id`：已有唯一匹配时原位更新该文件；没有匹配时才创建 `outputs/qa/YYYY-MM-DD-{question_id}.md`。自动正文放在 `<!-- llm-wiki:qa:{question_id}:start -->` 与对应 `end` 之间，不覆盖标记外用户内容。单边标记或多个同 ID 文件时停止并报告；写后复读验证。

## Lint 工作流

1. 用户明确要求后，扫描 `wiki/summaries/`、`wiki/concepts/`、`wiki/entities/` 和索引。
2. 检查：缺失/重复 `source_id`、YAML 字段、同义重复概念、无来源断言、断链、索引重复或遗漏、孤立页面、相互矛盾的定义，以及长期未更新且确有新来源的页面。
3. 将诊断报告写入 `outputs/health/YYYY-MM-DD-report.md`。自动生成内容放在 `<!-- llm-wiki:health:YYYY-MM-DD:start -->` 与对应 `end` 之间；同日重跑只替换该区块，保留标记外用户内容。旧版同日报告存在但没有标记时，只有能唯一识别完整的自动诊断章节边界时才原位升级；边界不明、单边标记或存在多个同日报告时停止并报告。报告列出证据、影响和建议，不把“日期较旧”本身当成错误。
4. 诊断不等于修复。只有用户明确授权修复后才改 wiki 内容；不得借修复之名修改 `raw/` 或 `pages-ai/`。
5. 修复后重新扫描受影响页面，确认问题已消除，并在内容实际变化时记录一次日志。

## 完成汇报

简要报告所选模式、读取范围、新增/更新/未变化的文件、重要发现和未解决问题。Query 未获写入授权时明确说明“未写入文件”。
