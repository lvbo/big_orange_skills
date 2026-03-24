#!/usr/bin/env python3
"""
每周五电影提醒脚本
检查最近7天观影记录，如果没看过，去豆瓣搜索推荐
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
NOTION_KEY = Path("~/.config/notion/api_key").expanduser().read_text().strip()
DATA_SOURCE_ID = "ee6db789-2242-49a6-9587-32e43b76522e"
USER_WECHAT = "o9cq803ZIgR6kKdW5J6Y0Q8Yz1DI@im.wechat"

def notion_query(data_source_id, filter_data=None, sorts=None, page_size=100):
    """查询 Notion 数据库"""
    import urllib.request
    import urllib.error
    
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
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
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"Notion API 错误: {e}")
        return {"results": []}

def get_recent_movies(days=7):
    """获取最近N天的观影记录"""
    seven_days_ago = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    filter_data = {
        "and": [
            {
                "property": "看完日期",
                "date": {"on_or_after": seven_days_ago}
            },
            {
                "property": "Status",
                "select": {"equals": "已看"}
            }
        ]
    }
    
    sorts = [{"property": "看完日期", "direction": "descending"}]
    
    return notion_query(DATA_SOURCE_ID, filter_data, sorts)

def get_all_watched_movies():
    """获取所有已看电影"""
    filter_data = {
        "property": "Status",
        "select": {"equals": "已看"}
    }
    return notion_query(DATA_SOURCE_ID, filter_data, page_size=100)

def analyze_favorite_tags(movies):
    """分析最喜欢的电影类型"""
    from collections import Counter
    
    tags = []
    for movie in movies.get("results", []):
        tag_list = movie.get("properties", {}).get("Tags", {}).get("multi_select", [])
        for tag in tag_list:
            tags.append(tag.get("name", ""))
    
    if not tags:
        return ["科幻", "国产电影", "纪录片"]
    
    counter = Counter(tags)
    return [tag for tag, _ in counter.most_common(3)]

def search_douban_movies(tag):
    """搜索豆瓣电影推荐"""
    queries = [
        f"豆瓣 {tag} 电影推荐 2024 2025",
        f"{tag} 高分电影 豆瓣 近期上映"
    ]
    
    results = []
    for query in queries[:1]:  # 只搜索第一个，避免太多请求
        try:
            # 使用 kimi_search 工具
            result = subprocess.run(
                ["python3", "-c", f"""
import sys
sys.path.insert(0, '/usr/lib/node_modules/openclaw')
from tools import kimi_search
result = kimi_search('{query}', limit=5)
print(json.dumps(result))
"""],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                results.append(result.stdout)
        except Exception as e:
            print(f"搜索错误: {e}")
    
    return results

def send_message(message):
    """发送微信消息"""
    print(message)
    # 这里可以通过 OpenClaw 的 API 发送消息
    # 实际发送由调用者处理

def main():
    print(f"检查时间范围: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} 至 {datetime.now().strftime('%Y-%m-%d')}")
    
    # 检查最近7天观影
    recent = get_recent_movies(7)
    movie_count = len(recent.get("results", []))
    print(f"最近7天观影数量: {movie_count}")
    
    if movie_count > 0:
        # 看过电影
        latest = recent["results"][0]
        title = latest.get("properties", {}).get("名称", {}).get("title", [{}])[0].get("plain_text", "未知")
        date = latest.get("properties", {}).get("看完日期", {}).get("date", {}).get("start", "未知")
        
        message = f"""🎬 本周观影检查

✅ 不错哦！最近7天你看过 {movie_count} 部电影。
🎥 最新一部是《{title}》({date})

劳逸结合做得很好，继续保持！"""
        
        print(message)
        return
    
    # 没看过电影，分析喜欢的类型
    all_movies = get_all_watched_movies()
    top_tags = analyze_favorite_tags(all_movies)
    
    print(f"喜欢的电影类型: {', '.join(top_tags)}")
    
    favorite_tag = top_tags[0] if top_tags else "科幻"
    
    # 构建提醒消息
    message = f"""🎬 本周观影提醒

⚠️ 最近7天你没有记录任何观影活动哦~

📊 根据你的观影历史，你最喜欢的类型是：{favorite_tag}

🎥 去豆瓣看看这些{type}类型的近期电影吧：
   • 打开豆瓣电影 APP/网站
   • 搜索：{favorite_tag} 2024 2025
   • 或搜索：{favorite_tag} 高分榜

💡 劳逸结合才能更好工作！挑一部放松一下吧~"""
    
    print(message)

if __name__ == "__main__":
    main()
