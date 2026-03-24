#!/bin/bash
# 电影提醒完整工作流
# 每周五 20:07 执行

set -e

cd /root/.openclaw/workspace

# 配置
NOTION_KEY=$(cat ~/.config/notion/api_key 2>/dev/null || echo "")
DATA_SOURCE_ID="ee6db789-2242-49a6-9587-32e43b76522e"
USER_WECHAT="o9cq803ZIgR6kKdW5J6Y0Q8Yz1DI@im.wechat"

if [ -z "$NOTION_KEY" ]; then
    echo "错误：Notion API Key 未配置"
    exit 1
fi

# 获取7天前的日期
SEVEN_DAYS_AGO=$(date -d "7 days ago" +%Y-%m-%d)

echo "检查时间: $SEVEN_DAYS_AGO 至 $(date +%Y-%m-%d)"

# 查询最近7天的观影记录
RECENT_COUNT=$(curl -s -X POST "https://api.notion.com/v1/data_sources/${DATA_SOURCE_ID}/query" \
  -H "Authorization: Bearer ${NOTION_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{
    \"filter\": {
      \"and\": [
        {\"property\": \"看完日期\", \"date\": {\"on_or_after\": \"${SEVEN_DAYS_AGO}\"}},
        {\"property\": \"Status\", \"select\": {\"equals\": \"已看\"}}
      ]
    }
  }" | jq -r '.results | length')

echo "最近7天观影数量: $RECENT_COUNT"

if [ "$RECENT_COUNT" -gt 0 ]; then
    # 看过电影 - 输出正常状态
    echo "STATUS: WATCHED"
    exit 0
fi

# 没看过电影 - 分析喜欢的类型
TOP_TAG=$(curl -s -X POST "https://api.notion.com/v1/data_sources/${DATA_SOURCE_ID}/query" \
  -H "Authorization: Bearer ${NOTION_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "已看"}},
    "page_size": 100
  }' | jq -r '.results[].properties.Tags.multi_select[].name' 2>/dev/null | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')

if [ -z "$TOP_TAG" ]; then
    TOP_TAG="科幻"
fi

echo "STATUS: NEED_SEARCH"
echo "FAVORITE_TAG: $TOP_TAG"

# 输出需要搜索的标记，供外部处理
echo ""
echo "=== MOVIE_RECOMMENDATION_REQUEST ==="
echo "user: $USER_WECHAT"
echo "tag: $TOP_TAG"
echo "message: 最近7天没有观影记录，请搜索${TOP_TAG}类型的近期豆瓣电影推荐"
echo "====================================="
