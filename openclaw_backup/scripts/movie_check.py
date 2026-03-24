#!/usr/bin/env python3
"""
每周五电影提醒脚本 - 完整版
检查最近7天观影记录，如果没看过，输出搜索请求
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# 配置
NOTION_KEY = Path("~/.config/notion/api_key").expanduser().read_text().strip()
DATA_SOURCE_ID = "ee6db789-2242-49a6-9587-32e43b76522e"

def notion_query(filter_data=None, sorts=None, page_size=100):
    """查询 Notion 数据库"""
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
        print(f"Notion API 错误: {e}", file=sys.stderr)
        return {"results": []}

def get_recent_movies(days=7):
    """获取最近N天的观影记录"""
    seven_days_ago = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    filter_data = {
        "and": [
            {"property": "看完日期", "date": {"on_or_after": seven_days_ago}},
            {"property": "Status", "select": {"equals": "已看"}}
        ]
    }
    sorts = [{"property": "看完日期", "direction": "descending"}]
    
    return notion_query(filter_data, sorts)

def get_all_watched_movies():
    """获取所有已看电影"""
    filter_data = {"property": "Status", "select": {"equals": "已看"}}
    return notion_query(filter_data, page_size=100)

def analyze_favorite_tags(movies):
    """分析最喜欢的电影类型"""
    tags = []
    for movie in movies.get("results", []):
        tag_list = movie.get("properties", {}).get("Tags", {}).get("multi_select", [])
        for tag in tag_list:
            name = tag.get("name", "")
            if name:
                tags.append(name)
    
    if not tags:
        return ["科幻", "国产电影", "纪录片"]
    
    counter = Counter(tags)
    return [tag for tag, _ in counter.most_common(3)]

def extract_movie_title(movie):
    """提取电影标题"""
    try:
        return movie["properties"]["名称"]["title"][0]["plain_text"]
    except (KeyError, IndexError):
        return "未知"

def extract_watch_date(movie):
    """提取观看日期"""
    try:
        return movie["properties"]["看完日期"]["date"]["start"]
    except (KeyError, TypeError):
        return "未知"

def main():
    # 检查最近7天观影
    recent = get_recent_movies(7)
    movie_count = len(recent.get("results", []))
    
    if movie_count > 0:
        # 看过电影 - 输出正常消息
        latest = recent["results"][0]
        title = extract_movie_title(latest)
        date = extract_watch_date(latest)
        
        print(f"""🎬 本周观影检查

✅ 不错哦！最近7天你看过 {movie_count} 部电影。
🎥 最新一部是《{title}》({date})

劳逸结合做得很好，继续保持！""")
        
        # 写入状态文件表示不需要搜索
        Path("/tmp/movie_reminder_status").write_text("watched")
        return 0
    
    # 没看过电影 - 分析类型并触发搜索
    all_movies = get_all_watched_movies()
    top_tags = analyze_favorite_tags(all_movies)
    favorite_tag = top_tags[0] if top_tags else "科幻"
    
    print(f"""🎬 本周观影提醒

⚠️ 最近7天你没有记录任何观影活动哦~

📊 根据你的观影历史，你最喜欢的类型是：{favorite_tag}

🔍 正在为你搜索{favorite_tag}类型的近期好片...""")
    
    # 写入状态文件，标记需要搜索
    status_data = {
        "need_search": True,
        "tag": favorite_tag,
        "tags": top_tags
    }
    Path("/tmp/movie_reminder_status").write_text(json.dumps(status_data))
    
    return 1  # 返回1表示需要搜索

if __name__ == "__main__":
    sys.exit(main())
