#!/bin/bash
# 电影提醒主脚本
# 先检查观影状态，如需要搜索则触发搜索任务

set -e

cd /root/.openclaw/workspace

# 运行检测脚本
if python3 scripts/movie_check.py; then
    # 返回0表示看过电影，直接退出
    exit 0
fi

# 返回1表示没看电影，需要搜索
# 读取搜索需求
TAG=$(cat /tmp/movie_reminder_status | python3 -c "import sys,json; print(json.load(sys.stdin).get('tag','科幻'))")

echo ""
echo "🎥 为你在豆瓣搜索 '${TAG}' 类型的近期电影推荐："
echo ""

# 使用 kimi-search 搜索豆瓣
# 注意：这里通过 OpenClaw 的消息机制来触发搜索
# 实际搜索由 agent 处理

echo "【SEARCH_REQUEST】tag=${TAG}"
