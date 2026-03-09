#!/usr/bin/env python3
"""
Todoist 今日任务获取脚本 (REST API v1 + 分页)
获取今天到期的 Todoist 任务
"""

import requests
import os
from datetime import datetime

# Todoist API Token
API_TOKEN = os.environ.get('TODOIST_API_TOKEN', '')

if not API_TOKEN:
    print("❌ 未配置 Todoist API Token")
    print("请设置环境变量: export TODOIST_API_TOKEN='your_token'")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# 获取所有任务（处理分页）
all_tasks = []
next_cursor = None

while True:
    params = {}
    if next_cursor:
        params['cursor'] = next_cursor
    
    try:
        response = requests.get(
            "https://api.todoist.com/api/v1/tasks",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        tasks = data.get('results', [])
        all_tasks.extend(tasks)
        
        next_cursor = data.get('next_cursor')
        if not next_cursor:
            break
    except Exception as e:
        print(f"❌ 获取任务失败: {e}")
        exit(1)

# 获取今天的日期
today = datetime.now().date()
today_str = today.strftime('%Y-%m-%d')

# 过滤今天到期的任务（排除子任务）
today_tasks = []
for task in all_tasks:
    # 排除已完成任务 (is_completed 可能是 None 或 False)
    if task.get('is_completed'):
        continue
    
    # 排除子任务（有 parent_id 的任务）
    if task.get('parent_id'):
        continue
    
    # 检查截止日期
    due = task.get('due')
    if not due:
        continue
    
    due_date = due.get('date', '')
    if due_date:
        try:
            task_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            if task_date <= today:  # 包括今天和逾期的
                today_tasks.append(task)
        except:
            continue

# 按优先级排序 (priority: 1=最低, 4=最高)
today_tasks.sort(key=lambda x: x.get('priority', 1), reverse=True)

# 输出结果
if not today_tasks:
    print("✅ 今天没有到期的任务")
else:
    print(f"**今日待办 ({len(today_tasks)}项)**\n")
    
    for task in today_tasks:
        priority = task.get('priority', 1)
        content = task.get('content', '无标题')
        due = task.get('due', {})
        due_date = due.get('date', '')
        
        # 优先级文本前缀 (Todoist: 4=P1, 3=P2, 2=P3, 1=P4)
        if priority == 4:
            priority_prefix = "(P1) "
        elif priority == 3:
            priority_prefix = "(P2) "
        elif priority == 2:
            priority_prefix = "(P3) "
        else:
            priority_prefix = "(P4) "
        
        # 检查是否逾期
        overdue_mark = ""
        if due_date:
            try:
                task_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                if task_date < today:
                    overdue_mark = " [逾期]"
            except:
                pass
        
        print(f"- {priority_prefix}{content}{overdue_mark}")