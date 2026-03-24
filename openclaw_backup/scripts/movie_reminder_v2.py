#!/usr/bin/env python3
"""
电影推荐助手 - 每周五运行
检测观影状态，如果没看过电影，搜索豆瓣推荐
"""

import json
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

NOTION_KEY = Path("~/.config/notion/api_key").expanduser().read_text().strip()
DATA_SOURCE_ID = "ee6db789-2242-49a6-9587-32e43b76522e"

def notion_query(filter_data=None, sorts=None, page_size=100):
    url = f"https://api.notion.com/v1/data_sources/{DATA_SOURCE_ID}/query"
    data = {"page_size": page_size}
    if filter_data:
        data["filter"] = filter_data
    if sorts:
        data["sorts"] = sorts
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {NOTION_KEY}",
            "Notion-Version": "2025-09-03",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Notion API 错误: {e}")
        return {"results": []}

def main():
    # 检查最近7天观影
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    recent = notion_query(
        filter_data={
            "and": [
                {"property": "看完日期", "date": {"on_or_after": seven_days_ago}},
                {"property": "Status", "select": {"equals": "已看"}}
            ]
        },
        sorts=[{"property": "看完日期", "direction": "descending"}]
    )
    
    movie_count = len(recent.get("results", []))
    
    if movie_count > 0:
        latest = recent["results"][0]
        title = latest.get("properties", {}).get("名称", {}).get("title", [{}])[0].get("plain_text", "未知")
        date = latest.get("properties", {}).get("看完日期", {}).get("date", {}).get("start", "未知")
        
        print(f"""🎬 本周观影检查

✅ 不错哦！最近7天你看过 {movie_count} 部电影。
🎥 最新一部是《{title}》({date})

劳逸结合做得很好，继续保持！""")
        return
    
    # 没看过电影，分析类型
    all_movies = notion_query(
        filter_data={"property": "Status", "select": {"equals": "已看"}},
        page_size=100
    )
    
    tags = []
    for movie in all_movies.get("results", []):
        for tag in movie.get("properties", {}).get("Tags", {}).get("multi_select", []):
            if tag.get("name"):
                tags.append(tag["name"])
    
    top_tags = Counter(tags).most_common(3)
    favorite_tag = top_tags[0][0] if top_tags else "科幻"
    
    print(f"""🎬 本周观影提醒

⚠️ 最近7天你没有记录任何观影活动哦~

📊 根据你的观影历史，你最喜欢的类型是：{favorite_tag}

---""")
    
    # 标记需要搜索（外部 agent 会捕获这个标记并执行搜索）
    print(f"\n[SEARCH_REQUEST] tag={favorite_tag}")

if __name__ == "__main__":
    main()
