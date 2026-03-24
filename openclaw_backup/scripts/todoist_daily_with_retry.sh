#!/bin/bash
# 定时任务包装器 - 带重试机制
# 用于 Todoist 每日推送

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TODOIST_API_TOKEN="739db0a1f96aa15d5aae5441e8046ea73c3fa9a2"

MAX_RETRIES=3
RETRY_DELAY=60  # 失败后等待60秒再重试

LOG_FILE="/root/.openclaw/workspace/logs/todoist_daily.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 主任务
run_task() {
    log "===== 开始执行 ====="
    
    # 获取今日任务
    OUTPUT=$(python3 /root/.openclaw/skills/todoist-tl/scripts/get_today.py 2>&1)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -ne 0 ]; then
        log "错误: 脚本执行失败 (exit $EXIT_CODE)"
        log "输出: $OUTPUT"
        return 1
    fi
    
    if echo "$OUTPUT" | grep -q "❌"; then
        log "错误: API 返回错误信息"
        log "输出: $OUTPUT"
        return 1
    fi
    
    # 输出结果（会被 cron 邮件或在日志中查看）
    log "成功获取任务"
    echo "$OUTPUT"
    
    return 0
}

# 主逻辑
main() {
    log "启动定时任务，最大重试次数: $MAX_RETRIES"
    
    for i in $(seq 1 $MAX_RETRIES); do
        log "尝试 $i/$MAX_RETRIES"
        
        if run_task; then
            log "任务成功完成"
            exit 0
        fi
        
        if [ $i -lt $MAX_RETRIES ]; then
            log "将在 ${RETRY_DELAY} 秒后重试..."
            sleep $RETRY_DELAY
        fi
    done
    
    log "所有重试均失败，任务退出"
    exit 1
}

main "$@"
