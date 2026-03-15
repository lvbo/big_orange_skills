#!/usr/bin/env python3
"""
Todoist 已完成任务查询脚本
获取指定日期范围内已完成的任务
"""

import requests
import os
import sys
from datetime import datetime, timedelta, timezone

# Todoist API Token
API_TOKEN = os.environ.get('TODOIST_API_TOKEN', '')

if not API_TOKEN:
    print("❌ 未配置 Todoist API Token")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# 东八区时区
CN_TIMEZONE = timezone(timedelta(hours=8))

def get_completed_tasks(since_date, until_date):
    """
    获取指定日期范围内已完成的任务
    使用 by_completion_date 端点
    """
    all_tasks = []
    next_cursor = None
    
    # 格式化时间为 ISO 8601
    since_str = since_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    until_str = until_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    while True:
        params = {
            'since': since_str,
            'until': until_str,
            'limit': 200
        }
        if next_cursor:
            params['cursor'] = next_cursor
        
        try:
            response = requests.get(
                "https://api.todoist.com/api/v1/tasks/completed/by_completion_date",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            tasks = data.get('items', [])
            all_tasks.extend(tasks)
            
            next_cursor = data.get('next_cursor')
            if not next_cursor:
                break
        except Exception as e:
            print(f"❌ 获取已完成任务失败: {e}")
            exit(1)
    
    return all_tasks

def format_tasks(tasks, date_label):
    """格式化任务输出"""
    if not tasks:
        return f"✅ {date_label} 没有完成的任务"
    
    lines = [f"**{date_label}已完成任务 ({len(tasks)}项)**\n"]
    
    # 按完成时间排序（最新的在前）
    tasks.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
    
    for task in tasks:
        priority = task.get('priority', 1)
        content = task.get('content', '无标题')
        completed_at = task.get('completed_at', '')
        
        # 优先级文本前缀
        if priority == 4:
            priority_prefix = "(P1) "
        elif priority == 3:
            priority_prefix = "(P2) "
        elif priority == 2:
            priority_prefix = "(P3) "
        else:
            priority_prefix = "(P4) "
        
        # 格式化完成时间（UTC 转东八区）
        time_str = ""
        if completed_at:
            try:
                # 解析 UTC 时间并转换为东八区
                completed_time = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                completed_time_cn = completed_time.astimezone(CN_TIMEZONE)
                time_str = f" [{completed_time_cn.strftime('%H:%M')}]"
            except:
                pass
        
        lines.append(f"- {priority_prefix}{content}{time_str}")
    
    return "\n".join(lines)

def main():
    # 解析参数
    if len(sys.argv) < 2:
        # 默认查询昨天
        target_days = 1
    else:
        arg = sys.argv[1]
        if arg in ['today', '今天']:
            target_days = 0
        elif arg in ['yesterday', '昨天']:
            target_days = 1
        elif arg in ['week', '本周']:
            target_days = 7
        else:
            try:
                target_days = int(arg)
            except:
                target_days = 1
    
    # 获取当前东八区时间
    now_cn = datetime.now(CN_TIMEZONE)
    
    if target_days == 0:
        # 今天（东八区）
        today_start = datetime(now_cn.year, now_cn.month, now_cn.day, 0, 0, 0, tzinfo=CN_TIMEZONE)
        # 转换为 UTC 用于 API 查询
        since_date = today_start.astimezone(timezone.utc).replace(tzinfo=None)
        until_date = now_cn.astimezone(timezone.utc).replace(tzinfo=None)
        date_label = "今天"
    elif target_days == 1:
        # 昨天（东八区）
        yesterday = now_cn - timedelta(days=1)
        yesterday_start = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0, tzinfo=CN_TIMEZONE)
        yesterday_end = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, tzinfo=CN_TIMEZONE)
        # 转换为 UTC 用于 API 查询
        since_date = yesterday_start.astimezone(timezone.utc).replace(tzinfo=None)
        until_date = yesterday_end.astimezone(timezone.utc).replace(tzinfo=None)
        date_label = "昨天"
    else:
        # 最近 N 天
        since_date = (now_cn - timedelta(days=target_days)).astimezone(timezone.utc).replace(tzinfo=None)
        until_date = now_cn.astimezone(timezone.utc).replace(tzinfo=None)
        date_label = f"最近{target_days}天"
    
    tasks = get_completed_tasks(since_date, until_date)
    print(format_tasks(tasks, date_label))

if __name__ == "__main__":
    main()
