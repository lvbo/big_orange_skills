#!/bin/bash
# Todoist 每日任务推送 - 带重试机制
# 推送今日待办到 Telegram

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"

# 重试配置
MAX_RETRIES=3
RETRY_DELAY=30  # 秒

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 获取今日任务并推送到 Telegram
push_today_tasks() {
    local attempt=$1
    
    log "尝试 $attempt/$MAX_RETRIES: 获取今日任务..."
    
    # 获取今日任务
    TASKS=$(python3 "$SCRIPT_DIR/get_today.py" 2>&1)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
        log "获取任务失败: $TASKS"
        return 1
    fi
    
    # 检查是否成功获取（不包含错误信息）
    if echo "$TASKS" | grep -q "❌"; then
        log "API 返回错误"
        return 1
    fi
    
    # 推送到 Telegram
    log "推送到 Telegram..."
    
    # 使用 Telegram bot API
    BOT_TOKEN="8330851580:AAH16Qw6BCAENYqbKA4OnyJd6o6Bg0AS1Fc"
    CHAT_ID="2183158614"  # 需要替换为实际的 chat_id
    
    MESSAGE="📋 *Todoist 今日待办*\n\n$(echo "$TASKS" | sed 's/\\n/%0A/g' | sed 's/\*/\\*/g')"
    
    RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "text=${MESSAGE}" \
        -d "parse_mode=Markdown" \
        --max-time 30 2>&1)
    
    if echo "$RESPONSE" | grep -q '"ok":true'; then
        log "推送成功"
        return 0
    else
        log "推送失败: $RESPONSE"
        return 1
    fi
}

# 主逻辑
main() {
    log "===== Todoist 每日推送开始 ====="
    
    for i in $(seq 1 $MAX_RETRIES); do
        if push_today_tasks $i; then
            log "任务完成"
            exit 0
        fi
        
        if [ $i -lt $MAX_RETRIES ]; then
            log "等待 ${RETRY_DELAY} 秒后重试..."
            sleep $RETRY_DELAY
        fi
    done
    
    log "所有重试均失败"
    exit 1
}

main "$@"
