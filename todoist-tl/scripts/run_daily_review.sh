#!/bin/bash
# Todoist 每日回顾推送脚本

export TODOIST_API_TOKEN=739db0a1f96aa15d5aae5441e8046ea73c3fa9a2
export PYTHONPATH=/root/.openclaw/skills/todoist-tl/scripts

REPORT=$(python3 /root/.openclaw/skills/todoist-tl/scripts/daily_review.py today 2>&1)

if [ $? -eq 0 ]; then
    echo "$REPORT"
else
    echo "❌ 今日日回顾获取失败，请检查 Todoist API 连接"
    echo "错误信息: $REPORT"
fi
