#!/bin/bash
# Todoist 每日回顾 - 带 Telegram 推送
# 每晚 22:13 执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"
export ICLOUD_USERNAME="lvbo09@icloud.com"
export ICLOUD_APP_PASSWORD="vzns-vduf-fofu-wgaj"

# Telegram 配置
BOT_TOKEN="8330851580:AAH16Qw6BCAENYqbKA4OnyJd6o6Bg0AS1Fc"
CHAT_ID="2183158614"  # Telegram 用户/群组 ID

# 重试配置
MAX_RETRIES=3
RETRY_DELAY=60

LOG_FILE="/root/.openclaw/workspace/logs/todoist_daily_review.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 发送 Telegram 消息
send_telegram() {
    local message="$1"
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -H "Content-Type: application/json" \
            -d "{\"chat_id\":\"${CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"Markdown\"}" \
            --max-time 30 2>&1)
        
        if echo "$RESPONSE" | grep -q '"ok":true'; then
            log "Telegram 推送成功"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        log "Telegram 推送失败，重试 $retry_count/$max_retries..."
        sleep 5
    done
    
    log "Telegram 推送最终失败"
    return 1
}

# 主任务
run_review() {
    log "===== 开始生成每日回顾 ====="
    
    # 生成昨日回顾
    OUTPUT=$(python3 /root/.openclaw/skills/todoist-tl/scripts/daily_review.py yesterday 2>&1)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
        log "错误: 生成回顾失败"
        log "输出: $OUTPUT"
        return 1
    fi
    
    log "回顾生成成功"
    
    # 输出到日志
    echo "$OUTPUT" | tee -a "$LOG_FILE"
    
    # 推送到 Telegram（需要对 Markdown 特殊字符进行转义）
    # Telegram MarkdownV2 需要转义的字符: _ * [ ] ( ) ~ ` > # + - = | { } . !
    # 这里用简单方式处理，避免复杂转义问题
    ESCAPED_OUTPUT=$(echo "$OUTPUT" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/  */ /g')
    
    # 构造简洁消息
    DATE_STR=$(date -d "yesterday" "+%Y-%m-%d")
    MESSAGE="📊 *Todoist 日回顾* - ${DATE_STR}\n\n${OUTPUT}"
    
    # 由于消息可能太长，分段发送或简化
    # 这里先尝试发送完整消息
    send_telegram "$OUTPUT"
    
    return 0
}

# 主逻辑
main() {
    log "启动每日回顾任务，最大重试次数: $MAX_RETRIES"
    
    for i in $(seq 1 $MAX_RETRIES); do
        log "尝试 $i/$MAX_RETRIES"
        
        if run_review; then
            log "任务成功完成"
            exit 0
        fi
        
        if [ $i -lt $MAX_RETRIES ]; then
            log "将在 ${RETRY_DELAY} 秒后重试..."
            sleep $RETRY_DELAY
        fi
    done
    
    log "所有重试均失败"
    exit 1
}

main "$@"
