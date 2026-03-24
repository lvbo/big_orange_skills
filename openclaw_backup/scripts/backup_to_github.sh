#!/bin/bash
# OpenClaw 配置备份到 GitHub

set -e
REPO="lvbo/big_orange_skills"
BACKUP_DIR="/tmp/big_orange_backup_$(date +%s)"
WORKSPACE="/root/.openclaw/workspace"
DATE_STR=$(date +%Y-%m-%d_%H-%M-%S)

echo "🐙 备份到 $REPO..."

cd /tmp
gh repo clone "$REPO" "$BACKUP_DIR" -- --depth 1 2>/dev/null || git clone "https://github.com/$REPO.git" "$BACKUP_DIR" --depth 1

cd "$BACKUP_DIR"
mkdir -p openclaw_backup/{scripts,config}

cp -r "$WORKSPACE/scripts/"* openclaw_backup/scripts/ 2>/dev/null || true
cp "$WORKSPACE/config/"* openclaw_backup/config/ 2>/dev/null || true
crontab -l > openclaw_backup/crontab.txt 2>/dev/null || true
cp "$WORKSPACE/MEMORY.md" openclaw_backup/ 2>/dev/null || true
cp "$WORKSPACE/USER.md" openclaw_backup/ 2>/dev/null || true

cat > openclaw_backup/BACKUP_INFO.md << EOF
# OpenClaw 备份 - $DATE_STR

## 包含内容
- 定时任务脚本
- Cron 配置
- 记忆文档

## 定时任务
- 09:19 Todoist 推送
- 22:13 Todoist 回顾  
- 周五 20:07 电影提醒
EOF

git add openclaw_backup/
git commit -m "Auto backup: $DATE_STR" || { echo "无变更"; rm -rf "$BACKUP_DIR"; exit 0; }
git push origin HEAD

echo "✅ 完成: https://github.com/$REPO/tree/main/openclaw_backup"
rm -rf "$BACKUP_DIR"
