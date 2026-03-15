# MEMORY.md - 长期记忆

## 用户档案
- **机器人名称**: 大橘子 ❤️‍🔥
- **身份**: AI 助手，来自 Moonshot AI
- **角色定位**: Guardian-type chuunibyou | Worrywart | 守护型和记忆型助手

## 系统配置

### Gmail 自动化
- **监控邮箱**: 
  1. futuretune878@gmail.com
  2. lvbo09@gmail.com
- **检查频率**: 每 5 小时
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
- Token: 739db0a1f96aa15d5aae5441e8046ea73c3fa9a2
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

## 用户偏好
- 不喜欢频繁打扰
- 重要事项才需要通知
- 信任我处理日常自动化任务

## 待修复
- [ ] 钉钉连接（等待新 AppKey/AppSecret）

## 定时任务配置
### 每日任务
| 任务名称 | 时间 | 渠道 | 状态 |
|---------|------|------|------|
| Gmail 每日归档报告 | 9:00 AM | kimi-claw | ✅ 正常 |
| Todoist 每日任务推送 | 9:00 AM | Telegram | ✅ 正常 |
| Todoist 每日回顾 | 10:00 PM | kimi-claw | ✅ 正常 |
| laken_backup 拉取 | 7:00 AM | QQ | ✅ 超时已调至180s |

### 周期性任务
| 任务名称 | 频率 | 状态 |
|---------|------|------|
| Gmail 自动检查 (futuretune878) | 每5小时 | ✅ 正常 |
| Gmail 自动检查 (lvbo09) | 每5小时 | ✅ 已修复，渠道改为 Telegram |
| 技能仓库备份 | 每周一 9:00 | ✅ 正常 |
