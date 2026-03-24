#!/bin/bash
# Todoist 每日回顾
# 每晚 22:13 执行，推送到 Telegram

set -e

export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"
export ICLOUD_USERNAME="lvbo09@icloud.com"
export ICLOUD_APP_PASSWORD="vzns-vduf-fofu-wgaj"

MAX_RETRIES=3
RETRY_DELAY=60

LOG_FILE="/root/.openclaw/workspace/logs/todoist_review.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Telegram 配置
BOT_TOKEN="8330851580:AAH16Qw6BCAENYqbKA4OnyJd6o6Bg0AS1Fc"
CHAT_ID="387275549"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 发送 Telegram 消息
send_telegram() {
    local message="$1"
    local retry=0
    
    while [ $retry -lt 3 ]; do
        RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -H "Content-Type: application/json" \
            -d "{\"chat_id\":\"${CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"Markdown\"}" \
            --max-time 30 2>&1)
        
        if echo "$RESPONSE" | grep -q '"ok":true'; then
            log "Telegram 发送成功"
            return 0
        fi
        
        retry=$((retry + 1))
        log "Telegram 发送失败，重试 $retry/3..."
        sleep 5
    done
    
    log "Telegram 发送最终失败"
    return 1
}

main() {
    log "启动每日回顾"
    
    for i in $(seq 1 $MAX_RETRIES); do
        log "尝试 $i/$MAX_RETRIES"
        
        OUTPUT=$(python3 /root/.openclaw/skills/todoist-tl/scripts/daily_review.py yesterday 2>&1)
        
        if [ $? -eq 0 ]; then
            log "成功生成回顾"
            echo "$OUTPUT" | tee -a "$LOG_FILE"
            
            # 发送到 Telegram
            # 转义特殊字符
            MSG=$(echo "$OUTPUT" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
            send_telegram "$MSG"
            
            exit 0
        fi
        
        log "失败，等待重试..."
        sleep $RETRY_DELAY
    done
    
    log "全部失败"
    exit 1
}

main
