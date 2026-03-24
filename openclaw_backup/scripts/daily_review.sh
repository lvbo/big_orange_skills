#!/bin/bash
# Todoist 每日回顾
# 每晚 22:13 执行，输出供 OpenClaw 推送到 Telegram

set -e

export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"
export ICLOUD_USERNAME="lvbo09@icloud.com"
export ICLOUD_APP_PASSWORD="vzns-vduf-fofu-wgaj"

MAX_RETRIES=3
RETRY_DELAY=60

LOG_FILE="/root/.openclaw/workspace/logs/todoist_review.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

main() {
    log "启动每日回顾"
    
    for i in $(seq 1 $MAX_RETRIES); do
        log "尝试 $i/$MAX_RETRIES"
        
        OUTPUT=$(python3 /root/.openclaw/skills/todoist-tl/scripts/daily_review.py yesterday 2>&1)
        
        if [ $? -eq 0 ]; then
            log "成功"
            echo "$OUTPUT"
            exit 0
        fi
        
        log "失败，等待重试..."
        sleep $RETRY_DELAY
    done
    
    log "全部失败"
    exit 1
}

main
