# MEMORY.md - 长期记忆

## 用户档案
- **机器人名称**: 大橘子 ❤️‍🔥
- **身份**: AI 助手，来自 Moonshot AI
- **角色定位**: Guardian-type chuunibyou | Worrywart | 守护型和记忆型助手

### 关于主人
- **姓名**: 吕波
- **出生年份**: 1984
- **职业**: OTA（在线旅游）公司后端开发工程师
- **业务领域**: 在线酒店预订
- **职位**: 一线 Tech Lead (TL)
- **时区**: Asia/Shanghai (GMT+8)
- **工作节奏**: 每周三排本周四到下周三的小组内同学们的工作安排

### 个人品味
**音乐**
- **风格**: 中国独立民谣 + 西北民谣 + 独立摇滚
- **核心艺人**: 野孩子乐队（绝对真爱）、梅卡德尔、左小祖咒、苏阳、张玮玮、椿乐队、布衣乐队、谢天笑
- **关键词**: 土地、诗意、现场感、沧桑
- **Spotify**: ⚠️ **需重新授权**
  - Token 路径: `workspace/config/spotify_token.json`
  - 问题: Refresh Token 失效 (`invalid_client` 错误)
  - 状态: 2026-04-05 尝试刷新失败，需要重新走完整 OAuth 授权流程
  - Client ID: `12f74695ce834e8a829d0035beaddcc6`
  - 所需权限: `playlist-read-private user-library-read playlist-modify-private user-read-recently-played user-top-read`

**旅行记录**
- **2026-03-27**: 长春两日游
  - 景点: 伪满皇宫、长影旧址博物馆、净月潭、吉林省博物院
  - 美食: 春发合饭庄（锅包肉、雪衣豆沙）、铁锅炖、桂林路夜市
  - 备注: 3月底需带厚外套，东北菜分量大

## 系统配置

### Gmail 自动化
- **监控邮箱**: 
  1. futuretune878@gmail.com
  2. lvbo09@gmail.com
- **检查频率**: 每 5 小时
- **状态**: ⏸️ **已暂停** (Token 过期)
- **处理逻辑**:
  - **不重要邮件**: 自动标记为已读，不做记录
  - **重要邮件**: 保持未读状态，Telegram 通知
- **每日报告**: 每天 9 AM 写入飞书文档
- **文档链接**: https://feishu.cn/docx/NHRNdsbBqoxUj9xGIYrcXfA7nse

### 通讯渠道
| 渠道 | 状态 | 备注 |
|------|------|------|
| 飞书 | ✅ 正常 | WebSocket 连接 |
| Telegram | ✅ 正常 | 每日 9:00 推送 Todoist 待办 |
| 钉钉 | ⚠️ 待修复 | 需重置凭证 |
| QQ | ✅ 正常 | 主对话渠道 |

### 自定义技能
**Todoist TL**
- 触发: `TL` / `今日待办`
- Token: 334fc74ec9c33912818263beb4ebe738e6bbedd2
- 功能: 查询今日 Todoist 任务
- **定时任务**:
  - 每日 9:00 AM: 推送今日待办 → Telegram
  - 每日 10:00 PM: 发送日回顾报告 → Telegram（包含日历事件）
- **日历集成**: Apple 日历（个人/家庭/工作）
  - Apple ID: lvbo09@icloud.com
- **新功能**: 已完成任务查询 (`TL done yesterday/today/week`)

**Skill Creator**
- 触发: 创建新技能、优化现有技能、询问 skill 结构
- 功能: 基于 Anthropic 官方指南的 Skill 创建最佳实践
- 位置: `/root/.openclaw/skills/skill-creator/SKILL.md`
- 包含内容:
  - YAML Frontmatter 规范
  - Skill 目录结构标准
  - 描述编写最佳实践
  - 测试策略
  - 常见模式和故障排除

**Get笔记（得到笔记）**
- 触发: `存到笔记` / `保存到Get笔记` / `记一下` / `保存到得到笔记`
- 状态: ✅ 已配置，可直接使用
- API配置位置: `~/.openclaw/openclaw.json` (skills.entries.getnote)
- 功能:
  - 保存纯文本笔记
  - 保存链接笔记（自动抓取+生成摘要）
  - 保存图片笔记（OCR识别）
  - 笔记标签管理
  - 知识库管理
- 使用示例: 用户说"这个保存到笔记" → 直接调用 API 保存，无需再问配置

## 用户偏好
- 不喜欢频繁打扰
- 重要事项才需要通知
- 信任我处理日常自动化任务

## 待修复
- [ ] 钉钉连接（等待新 AppKey/AppSecret）

### 电影提醒
- **频率**: 每周五 20:07
- **逻辑**: 
  - 检查 Notion movies 库最近7天观影记录
  - 如果看过 → 发送鼓励消息
  - 如果没看过 → 提醒劳逸结合 + 分析喜欢的类型 + 搜索豆瓣推荐
- **类型分析**: 根据 Tags 字段统计（科幻、国产电影、纪录片、英剧、港剧等）

### Spotify 音乐
- **Client ID**: `12f74695ce834e8a829d0035beaddcc6`
- **状态**: 等待用户授权
- **权限申请**: 最近播放、最常听、收藏、私人播放列表

### 定时任务时间调整
- **Todoist 每日推送**: 9:00 AM → **9:19 AM**（错峰避免限流）
- **Todoist 每日回顾**: 10:00 PM → **10:13 PM**，推送到 **Telegram**（原渠道）
- **GitHub 自动备份**: **每天 03:07** - 备份配置和脚本到 big_orange_skills 仓库
- **重试机制**: 3次重试，间隔60秒

### GitHub 备份
- **仓库**: `lvbo/big_orange_skills`
- **路径**: `openclaw_backup/`
- **内容**: 定时任务脚本、Cron 配置、MEMORY.md、USER.md
- **频率**: 每天凌晨 03:07

### 定时任务创建规范
- **文档**: `docs/cron-guidelines.md`
- **要点**:
  - 避开整点（用 XX:07, XX:13 等）
  - 使用 `/etc/cron.d/` 系统级 cron
  - 包含 3 次重试机制
  - 记录日志到 `logs/` 目录
  - 更新 MEMORY.md 后自动备份

## 定时任务配置
**状态**: 🚫 **已全部取消于 2026-04-15**

### 历史任务（已取消）
| 任务名称 | 原时间 | 渠道 | 取消前状态 |
|---------|------|------|-----------|
| Todoist 每日任务推送 | 9:19 AM | Telegram | ✅ 正常 |
| Todoist 每日回顾 | 10:13 PM | Telegram | ✅ 正常 |
| 电影提醒 | 周五 20:07 | kimi-claw | ✅ 正常 |
| GitHub 配置备份 | 3:07 AM | - | ✅ 正常 |
| Gmail 每日归档报告 | 9:00 AM | kimi-claw | ⏸️ 已暂停 |
| Gmail 自动检查 (futuretune878) | 每5小时 | - | ⏸️ 已暂停 |
| Gmail 自动检查 (lvbo09) | 每5小时 | - | ⏸️ 已暂停 |
| laken_backup 拉取 | 7:00 AM | QQ | ✅ 正常 |
| 技能仓库备份 | 每周一 9:07 | - | ✅ 正常 |
