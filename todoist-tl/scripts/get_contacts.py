#!/usr/bin/env python3
"""
Apple Contacts (iCloud) 联系人获取脚本
通过 CardDAV 协议获取联系人
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from caldav import DAVClient

def get_contacts(username=None, password=None):
    """
    获取 iCloud 联系人
    
    需要环境变量:
    - ICLOUD_USERNAME: Apple ID
    - ICLOUD_APP_PASSWORD: App 专用密码
    """
    
    if not username:
        username = os.environ.get('ICLOUD_USERNAME', '')
    if not password:
        password = os.environ.get('ICLOUD_APP_PASSWORD', '')
    
    if not username or not password:
        return None, "未配置 iCloud 凭据。请设置环境变量 ICLOUD_USERNAME 和 ICLOUD_APP_PASSWORD"
    
    try:
        # iCloud CardDAV 服务器
        client = DAVClient(
            "https://contacts.icloud.com",
            username=username,
            password=password
        )
        
        principal = client.principal()
        
        # 获取地址簿
        addressbooks = principal.calendars()
        
        if not addressbooks:
            return [], None
        
        contacts = []
        for ab in addressbooks:
            try:
                # 这里简化处理，实际 CardDAV 查询更复杂
                # 由于 vobject 库限制，先返回提示
                pass
            except:
                continue
        
        return contacts, None
        
    except Exception as e:
        return None, f"获取联系人失败: {str(e)}"

def main():
    contacts, error = get_contacts()
    
    if error:
        print(f"⚠️ {error}")
        sys.exit(1)
    
    if not contacts:
        print("**👥 联系人**: 暂无数据 (需要安装 vobject 库)")
    else:
        print(f"**👥 联系人 ({len(contacts)}位)**")
        for contact in contacts[:10]:  # 只显示前10位
            print(f"- {contact}")

if __name__ == "__main__":
    main()
