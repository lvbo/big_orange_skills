---
name: llm-wiki
description: 处理我的笔记时使用。基于 LLM Wiki 模式，结合 PARA 方法论。
---

## 触发条件


## 页面模板规范

### 摘要页 (wiki/summaries/)

文件名：`{Source}-原文标题.md`

```yaml
---
title: "文章原标题"
source: "URL 或来源标识"
author: "作者名（如有）"
published: "YYYY-MM-DD（原文发布时间）"
ingested: "YYYY-MM-DD（处理时间）"
description: "一句话描述"
tags:
  - "source"
  - "领域标签"
---
```

正文结构：
```markdown
## 核心结论

1-3 条核心观点

## 关键证据

支撑结论的关键论据

## 重要概念

文中涉及的概念链接

## 疑点/待验证

存疑或需要进一步验证的内容

## 相关来源

- [[其他相关摘要]]
```

### 概念页 (wiki/concepts/)

文件名：`概念名.md`（中文概念用中文名）

```yaml
---
title: "概念名"
created: "YYYY-MM-DD（首次创建）"
updated: "YYYY-MM-DD（最后更新）"
tags:
  - "concept"
  - "领域标签"
sources:
  - "来源1"
  - "来源2"
---
```

正文结构：
```markdown
## 定义

清晰简洁的定义

## 关键特征

- 特征1
- 特征2

## 证据/例子

支持性证据或实例

## 相关概念

- [[相关概念1]]
- [[相关概念2]]

## 矛盾/争议

不同来源的冲突观点
```

### 实体页 (wiki/entities/)

文件名：`实体名.md`

```yaml
---
title: "实体名"
type: "person|company|product|book|tool|..."
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags:
  - "entity"
  - "类型标签"
sources:
  - "来源1"
---
```

### 索引页 (wiki/indexes/)

```yaml
---
title: "索引名"
updated: "YYYY-MM-DD"
---
```

---

## 工作流程

### Ingest（摄取新资料）

**触发条件**：用户添加新资料到 `raw/` 并要求处理

**执行步骤**：

1. **读取原文**
   - 读取 `raw/` 中的新文件
   - 如有图片，按需读取 `assets/` 中的相关图片

2. **生成摘要**
   - 创建/更新 `wiki/summaries/{Source}-标题.md`
   - 使用 2.1 模板格式

3. **提取概念**
   - 识别文中重要概念
   - 对每个概念：
     - 如果 `wiki/concepts/概念名.md` 不存在，创建新页面
     - 如果存在，更新页面并追加新证据
     - 更新 `updated` 字段

4. **提取实体**
   - 识别人物、公司、产品、书籍等实体
   - 在 `wiki/entities/` 中创建或更新相应页面

5. **更新索引**
   - 更新 `wiki/indexes/All-Sources.md`（添加新摘要链接）
   - 更新 `wiki/indexes/All-Concepts.md`（如有新概念）
   - 更新 `wiki/indexes/All-Entities.md`（如有新实体）

6. **记录日志**
   - 在 `wiki/log.md` 追加条目：
   ```markdown
   ## [YYYY-MM-DD] ingest | 文章标题
   - Source: raw/articles/xxx.md
   - Summary: wiki/summaries/xxx.md
   - New concepts: 概念1, 概念2
   - New entities: 实体1
   - Key insight: 一句话关键发现
   ```

7. **汇报结果**
   - 向用户汇报：新增/更新了哪些页面
   - 指出重要发现：矛盾、新连接、待验证问题

### Query（查询与问答）

**触发条件**：用户提出问题

**执行步骤**：

1. **检索相关页面**
   - 先读取 `wiki/indexes/` 找到相关页面
   - 读取相关 `wiki/summaries/`、`wiki/concepts/`、`wiki/entities/`

2. **综合回答**
   - 基于检索到的内容回答
   - 使用 [[页面名]] 格式引用来源

3. **沉淀输出（可选）**
   - 如果问题复杂或答案有价值：
     - 保存到 `outputs/qa/YYYY-MM-DD-问题摘要.md`
     - 文件内容包含：问题、回答、引用的来源链接

4. **更新日志**
   ```markdown
   ## [YYYY-MM-DD] query | 问题摘要
   - Output: outputs/qa/xxx.md（如有）
   - Sources used: [[来源1]], [[来源2]]
   ```

### Lint（健康检查）

**触发条件**：每周执行，或用户主动要求

**执行步骤**：

1. **扫描 wiki 目录**
   - 遍历 `wiki/summaries/`、`wiki/concepts/`、`wiki/entities/`

2. **检查项目**
   - **一致性**：概念定义是否矛盾，同一概念是否有多个名称
   - **完整性**：哪些概念缺少定义、例子或来源
   - **孤立页面**：入链出链均 < 2 的页面
   - **过时内容**：`updated` 日期久远且可能有新信息的页面

3. **生成报告**
   - 保存到 `outputs/health/YYYY-MM-DD-report.md`
   - 包含：发现的问题列表、建议的修复方案

4. **修复（经用户确认后）**
   - 解决概念冲突
   - 为孤立页面添加连接
   - 更新过时内容

5. **更新日志**
   ```markdown
   ## [YYYY-MM-DD] lint | 健康检查
   - Report: outputs/health/xxx.md
   - Issues found: X
   - Actions taken: XXX
   ```

---

## 与 PARA 的融合

用户同时使用 PARA 方法管理知识：

- **01-Projects**（项目）：`pages-ai/01-projects/` 中项目相关页面
- **02-Areas**（领域）：`pages-ai/02-areas/` 中领域相关页面
- **03-Resources**（资源）：`pages-ai/03-resources/` 中资源相关页面
- **04-Archives**（归档）：`pages-ai/04-archives/` 是归档资料

**融合规则**：
- 当 wiki 中的概念与某个项目/领域相关时，在概念页添加链接：
  - `相关项目：[[pages-ai/01-projects/项目名称]]`
  - `相关领域：[[pages-ai/02-areas/领域名称]]`
- 用户可以手动在 `pages-ai/01-projects/` 和 `pages-ai/02-areas/` 的项目/领域页中添加链接到 wiki

---

## 命名规范

### 文件名
- 使用 kebab-case（短横线连接）
- 中文文件名直接使用中文
- 英文统一小写

### 标签 (tags)
- `source` - 摘要来源
- `concept` - 概念
- `entity` - 实体
- `person|company|product|book|tool` - 实体类型
- 领域标签如：`ai`, `productivity`, `health` 等

### 链接格式
- 内部链接：`[[页面名]]` 或 `[[路径/页面名]]`
- 带别名链接：`[[页面名|显示文本]]`

---

## 矛盾处理

当发现新资料与已有知识矛盾时：

1. 在相关概念页的 `## 矛盾/争议` 部分记录
2. 格式：
   ```markdown
   ### 矛盾点：XXX
   - 观点A（来源：[[摘要A]]）：...
   - 观点B（来源：[[摘要B]]）：...
   - 分析：...
   ```
3. 向用户汇报矛盾，请求判断

---

## 文件操作原则

- **增量更新**：优先编辑现有文件，而非重建
- **原子操作**：一次操作完成一个完整任务
- **及时记录**：每次操作后立即更新 log.md
- **引用优先**：所有结论必须有 [[来源]] 支撑
