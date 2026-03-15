#!/usr/bin/env python3
"""
Apple Calendar (iCloud) 日历获取脚本
通过 CalDAV 协议获取日历事件
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from caldav import DAVClient
from caldav.elements import dav

# iCloud CalDAV 配置
ICLOUD_URL = "https://caldav.icloud.com"

# 只获取这些日历的事件
TARGET_CALENDARS = ["个人", "家庭", "工作", "Personal", "Family", "Work", "personal", "family", "work"]

def get_calendar_events(target_date, username=None, password=None):
    """
    获取指定日期的日历事件
    
    需要环境变量:
    - ICLOUD_USERNAME: Apple ID
    - ICLOUD_APP_PASSWORD: App 专用密码 (不是 Apple ID 密码)
    
    如何生成 App 专用密码:
    1. 访问 https://appleid.apple.com
    2. 登录后点击"App 专用密码"
    3. 点击"生成密码"
    4. 复制生成的密码
    """
    
    if not username:
        username = os.environ.get('ICLOUD_USERNAME', '')
    if not password:
        password = os.environ.get('ICLOUD_APP_PASSWORD', '')
    
    if not username or not password:
        return None, "未配置 iCloud 凭据。请设置环境变量 ICLOUD_USERNAME 和 ICLOUD_APP_PASSWORD"
    
    try:
        # 连接 CalDAV 服务器
        client = DAVClient(ICLOUD_URL, username=username, password=password)
        principal = client.principal()
        
        # 获取所有日历
        calendars = principal.calendars()
        
        if not calendars:
            return [], None
        
        # 设置时间范围（当天的开始和结束）
        tz = timezone(timedelta(hours=8))  # 东八区
        start = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=tz)
        end = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=tz)
        
        all_events = []
        
        for calendar in calendars:
            try:
                # 只获取个人和家庭日历
                calendar_name = calendar.name
                if not any(target in calendar_name for target in TARGET_CALENDARS):
                    continue
                
                # 获取指定日期范围内的事件
                events = calendar.date_search(start=start, end=end)
                
                for event in events:
                    try:
                        vevent = event.instance.vevent
                        summary = str(vevent.summary.value) if hasattr(vevent, 'summary') else '无标题'
                        
                        # 获取开始和结束时间
                        start_time = None
                        end_time = None
                        is_all_day = False
                        
                        if hasattr(vevent, 'dtstart'):
                            dtstart = vevent.dtstart.value
                            if isinstance(dtstart, datetime):
                                start_time = dtstart.astimezone(tz) if dtstart.tzinfo else dtstart
                            else:
                                # 全天事件
                                is_all_day = True
                                start_time = datetime.combine(dtstart, datetime.min.time(), tzinfo=tz)
                        
                        if hasattr(vevent, 'dtend'):
                            dtend = vevent.dtend.value
                            if isinstance(dtend, datetime):
                                end_time = dtend.astimezone(tz) if dtend.tzinfo else dtend
                            else:
                                end_time = datetime.combine(dtend, datetime.min.time(), tzinfo=tz)
                        
                        # 获取地点
                        location = None
                        if hasattr(vevent, 'location'):
                            location = str(vevent.location.value)
                        
                        # 获取描述
                        description = None
                        if hasattr(vevent, 'description'):
                            description = str(vevent.description.value)
                        
                        all_events.append({
                            'summary': summary,
                            'start_time': start_time,
                            'end_time': end_time,
                            'is_all_day': is_all_day,
                            'location': location,
                            'description': description,
                            'calendar': calendar.name
                        })
                    except Exception as e:
                        continue
            except Exception as e:
                continue
        
        # 按开始时间排序
        all_events.sort(key=lambda x: x['start_time'] or datetime.min.replace(tzinfo=tz))
        
        return all_events, None
        
    except Exception as e:
        return None, f"获取日历失败: {str(e)}"

def format_events(events):
    """格式化日历事件输出"""
    if not events:
        return "**🗓️ 今日会议**: 无\n"
    
    lines = [f"**🗓️ 今日会议 ({len(events)}场)**\n"]
    
    for event in events:
        summary = event['summary']
        start = event['start_time']
        end = event['end_time']
        is_all_day = event['is_all_day']
        location = event['location']
        calendar_name = event.get('calendar', '默认')
        
        # 时间格式化
        if is_all_day:
            time_str = "全天"
        elif start:
            if end:
                time_str = f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}"
            else:
                time_str = f"{start.strftime('%H:%M')}"
        else:
            time_str = "时间未定"
        
        # 地点和日历
        loc_str = f" @ {location}" if location else ""
        cal_str = f" [{calendar_name}]" if calendar_name else ""
        
        lines.append(f"📅 {time_str} | {summary}{loc_str}{cal_str}")
    
    lines.append("")
    return "\n".join(lines)

def main():
    # 解析参数
    if len(sys.argv) < 2:
        target_date = datetime.now(timezone(timedelta(hours=8))).date()
    else:
        arg = sys.argv[1]
        if arg in ['today', '今天']:
            target_date = datetime.now(timezone(timedelta(hours=8))).date()
        elif arg in ['yesterday', '昨天']:
            target_date = (datetime.now(timezone(timedelta(hours=8))) - timedelta(days=1)).date()
        else:
            try:
                target_date = datetime.strptime(arg, '%Y-%m-%d').date()
            except:
                target_date = datetime.now(timezone(timedelta(hours=8))).date()
    
    events, error = get_calendar_events(target_date)
    
    if error:
        print(f"⚠️ {error}")
        print("\n**设置方法**:")
        print("1. 访问 https://appleid.apple.com")
        print("2. 生成 App 专用密码")
        print("3. 设置环境变量:")
        print("   export ICLOUD_USERNAME='your_apple_id'")
        print("   export ICLOUD_APP_PASSWORD='your_app_password'")
        sys.exit(1)
    
    print(format_events(events))

if __name__ == "__main__":
    main()
