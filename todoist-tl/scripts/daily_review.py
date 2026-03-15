#!/usr/bin/env python3
"""
Todoist 昨日回顾脚本
生成指定日期的任务回顾报告
"""

import requests
import os
import sys
from datetime import datetime, timedelta, timezone

API_TOKEN = os.environ.get('TODOIST_API_TOKEN', '')
if not API_TOKEN:
    print("❌ 未配置 Todoist API Token")
    exit(1)

headers = {"Authorization": f"Bearer {API_TOKEN}"}
CN_TIMEZONE = timezone(timedelta(hours=8))

def get_completed_tasks_by_date(target_date):
    """获取指定日期已完成的任务"""
    since = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=CN_TIMEZONE).astimezone(timezone.utc)
    until = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=CN_TIMEZONE).astimezone(timezone.utc)
    
    all_tasks = []
    next_cursor = None
    
    while True:
        params = {
            'since': since.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'until': until.strftime('%Y-%m-%dT%H:%M:%SZ'),
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
            all_tasks.extend(data.get('items', []))
            next_cursor = data.get('next_cursor')
            if not next_cursor:
                break
        except Exception as e:
            print(f"❌ 获取已完成任务失败: {e}")
            break
    
    return all_tasks

def get_tasks_by_due_date(target_date):
    """获取截止日期为指定日期的任务（包括已完成和未完成）"""
    all_tasks = []
    next_cursor = None
    
    while True:
        params = {'limit': 200}
        if next_cursor:
            params['cursor'] = next_cursor
        
        try:
            response = requests.get("https://api.todoist.com/api/v1/tasks", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_tasks.extend(data.get('results', []))
            next_cursor = data.get('next_cursor')
            if not next_cursor:
                break
        except Exception as e:
            print(f"❌ 获取任务失败: {e}")
            break
    
    # 筛选截止日期为 target_date 的任务
    target_date_str = target_date.strftime('%Y-%m-%d')
    result = []
    
    for task in all_tasks:
        if task.get('parent_id'):
            continue
        
        due = task.get('due')
        if not due:
            continue
        
        due_date = due.get('date', '')
        if not due_date:
            continue
        
        # 处理带时间的日期格式
        if 'T' in due_date:
            due_date = due_date.split('T')[0]
        
        if due_date == target_date_str:
            result.append(task)
    
    return result

def parse_pomodoro(content):
    """解析番茄钟符号"""
    tomato_est = content.count('🍅')
    melon_est = content.count('🍉')
    tomato_done = content.count('🥔')
    melon_done = content.count('🍠')
    
    estimated = tomato_est * 25 + melon_est * 15
    actual = tomato_done * 25 + melon_done * 15
    is_completed = tomato_done > 0 or melon_done > 0
    
    return {
        'estimated': estimated,
        'actual': actual,
        'is_completed': is_completed,
        'tomato_est': tomato_est,
        'tomato_done': tomato_done,
        'melon_est': melon_est,
        'melon_done': melon_done
    }

def format_duration(mins):
    """格式化分钟数"""
    if mins == 0:
        return "0分钟"
    hours = mins // 60
    mins = mins % 60
    if hours > 0 and mins > 0:
        return f"{hours}小时{mins}分钟"
    elif hours > 0:
        return f"{hours}小时"
    return f"{mins}分钟"

def get_weekday_cn(date):
    """获取中文星期"""
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    return weekdays[date.weekday()]

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from get_calendar import get_calendar_events, format_events

def main():
    # 解析参数，默认昨天
    if len(sys.argv) < 2:
        target_date = (datetime.now(CN_TIMEZONE) - timedelta(days=1)).date()
    else:
        arg = sys.argv[1]
        if arg in ['today', '今天']:
            target_date = datetime.now(CN_TIMEZONE).date()
        elif arg in ['yesterday', '昨天']:
            target_date = (datetime.now(CN_TIMEZONE) - timedelta(days=1)).date()
        else:
            try:
                target_date = datetime.strptime(arg, '%Y-%m-%d').date()
            except:
                target_date = (datetime.now(CN_TIMEZONE) - timedelta(days=1)).date()
    
    # 获取数据
    completed_tasks = get_completed_tasks_by_date(target_date)
    due_tasks = get_tasks_by_due_date(target_date)
    calendar_events, calendar_error = get_calendar_events(target_date)
    
    # 解析番茄钟数据
    completed_with_pomo = []
    for task in completed_tasks:
        content = task.get('content', '')
        p = parse_pomodoro(content)
        completed_time = task.get('completed_at', '')
        completed_hour = ""
        if completed_time:
            try:
                ct = datetime.fromisoformat(completed_time.replace('Z', '+00:00'))
                ct_cn = ct.astimezone(CN_TIMEZONE)
                completed_hour = ct_cn.strftime('%H:%M')
            except:
                pass
        
        completed_with_pomo.append({
            'content': content,
            'pomodoro': p,
            'completed_at': completed_hour,
            'priority': task.get('priority', 1)
        })
    
    # 计算统计数据
    completed_count = len(completed_with_pomo)
    total_actual = sum(t['pomodoro']['actual'] for t in completed_with_pomo)
    total_estimated = sum(t['pomodoro']['estimated'] for t in completed_with_pomo)
    
    # 截止日期为目标日期的任务数
    due_count = len(due_tasks)
    
    # 计算未完成的任务数（截止日期为目标日期但未完成）
    due_task_contents = {t.get('content', '') for t in due_tasks}
    completed_contents = {t['content'] for t in completed_with_pomo}
    incomplete_count = len(due_task_contents - completed_contents)
    
    # 生成报告
    weekday = get_weekday_cn(target_date)
    print(f"📊 **{target_date.strftime('%Y-%m-%d')} (周{weekday}) 日回顾**\n")
    
    # 今日会议
    if calendar_error:
        print(f"**🗓️ 今日会议**: ⚠️ 未配置日历 (如需显示会议，请设置 ICLOUD_USERNAME 和 ICLOUD_APP_PASSWORD)\n")
    else:
        print(format_events(calendar_events))
    
    # 总体统计
    print("**📈 总体情况**")
    print(f"- 截止日期任务: {due_count} 个")
    print(f"- 实际完成: {completed_count} 个")
    if due_count > 0:
        completion_rate = round(completed_count / due_count * 100, 1)
        print(f"- 完成率: {completion_rate}%")
    print(f"- 实际用时: {format_duration(total_actual)}")
    if total_estimated > 0:
        print(f"- 预估用时: {format_duration(total_estimated)}")
        diff = total_actual - total_estimated
        if diff > 0:
            print(f"- 偏差: +{format_duration(diff)} ⬆️")
        elif diff < 0:
            print(f"- 偏差: -{format_duration(abs(diff))} ⬇️")
        else:
            print(f"- 偏差: 准时 ✅")
    print()
    
    # 已完成任务详情
    if completed_count > 0:
        print(f"**✅ 已完成任务 ({completed_count}项)**\n")
        # 按完成时间排序
        completed_with_pomo.sort(key=lambda x: x['completed_at'])
        
        for task in completed_with_pomo:
            p = task['pomodoro']
            time_str = f" [{task['completed_at']}]" if task['completed_at'] else ""
            
            # 优先级
            priority = task['priority']
            if priority == 4:
                p_tag = "(P1) "
            elif priority == 3:
                p_tag = "(P2) "
            elif priority == 2:
                p_tag = "(P3) "
            else:
                p_tag = "(P4) "
            
            print(f"✅ {p_tag}{task['content']}{time_str}")
            print(f"   🍅 预估: {format_duration(p['estimated'])} | 🥔 实际: {format_duration(p['actual'])}")
            
            if p['estimated'] > 0:
                diff = p['actual'] - p['estimated']
                if diff > 0:
                    print(f"   ⚠️ 超时: +{format_duration(diff)}")
                elif diff < 0:
                    print(f"   ✨ 提前: -{format_duration(abs(diff))}")
            print()
    else:
        print("**✅ 已完成任务**: 无\n")
    
    # 未完成任务（如果截止日期是目标日期且未完成）
    if incomplete_count > 0:
        print(f"**⬜ 未完成/逾期任务 ({incomplete_count}项)**\n")
        for task in due_tasks:
            content = task.get('content', '')
            # 检查这个任务是否在 completed 列表中
            if content not in completed_contents:
                p = parse_pomodoro(content)
                print(f"⬜ {content}")
                if p['estimated'] > 0:
                    print(f"   预估: {format_duration(p['estimated'])}")
                print()
    
    print(f"📅 生成时间: {datetime.now(CN_TIMEZONE).strftime('%H:%M')}")

if __name__ == "__main__":
    main()
