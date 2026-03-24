#!/bin/bash
# OpenClaw 定时任务恢复脚本
# 机器重启后运行此脚本恢复 cron 任务

echo "恢复 OpenClaw 定时任务..."

# 方法1：从备份恢复用户 crontab
if [ -f /root/.openclaw/workspace/config/crontab.backup ]; then
    crontab /root/.openclaw/workspace/config/crontab.backup
    echo "✅ 用户 crontab 已恢复"
fi

# 方法2：确保系统级 cron 文件存在
if [ ! -f /etc/cron.d/openclaw-tasks ]; then
    cat > /etc/cron.d/openclaw-tasks << 'EOF'
# OpenClaw 定时任务
19 9 * * * root /root/.openclaw/workspace/scripts/todoist_daily_with_retry.sh >> /root/.openclaw/workspace/logs/todoist_cron.log 2>&1
13 22 * * * root /root/.openclaw/workspace/scripts/daily_review.sh >> /root/.openclaw/workspace/logs/todoist_review.log 2>&1
7 20 * * 5 root /root/.openclaw/workspace/scripts/movie_friday_check.sh >> /root/.openclaw/workspace/logs/movie_reminder.log 2>&1
EOF
    chmod 644 /etc/cron.d/openclaw-tasks
    echo "✅ 系统级 cron 文件已创建"
fi

# 重启 cron 服务
systemctl restart cron 2>/dev/null || service cron restart 2>/dev/null

echo "✅ 定时任务恢复完成"
echo ""
echo "当前定时任务:"
crontab -l 2>/dev/null || echo "(用户 crontab 为空)"
echo ""
echo "系统级定时任务:"
cat /etc/cron.d/openclaw-tasks 2>/dev/null || echo "(无)"
