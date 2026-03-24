#!/bin/bash
# Todoist 每日回顾 - 带 Telegram 推送
# 每晚 22:13 执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"
export ICLOUD_USERNAME="lvbo09@icloud.com"
export ICLOUD_APP_PASSWORD="vzns-vduf-fofu-wgaj"

# 重试配置
MAX_RETRIES=3
RETRY_DELAY=60

LOG_FILE="/root/.openclaw/workspace/logs/todoist_daily_review.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
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
    
    return 0
}

# 主逻辑
main() {
    log "启动每日回顾任务，最大重试次数: $MAX_RETRIES"
    
    for i in $(seq 1 $MAX_RETRIES); do
        log "尝试 $i/$MAX_RETRIES"
        
        if run_review; then
            log "任务成功完成"
            # 返回0表示成功，但 Telegram 推送由 OpenClaw 处理
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
