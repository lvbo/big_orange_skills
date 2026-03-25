#!/usr/bin/env python3
"""
Spotify 音乐品味分析
获取用户的听歌数据
"""

import requests
import base64
import json

CLIENT_ID = "12f74695ce834e8a829d0035beaddcc6"
CLIENT_SECRET = "2155b3bb4e84447096215af508166f91"

def get_access_token():
    """获取 Spotify Access Token"""
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"获取 Token 失败: {response.status_code}")
        print(response.text)
        return None

def get_new_releases(token):
    """获取最新发行"""
    url = "https://api.spotify.com/v1/browse/new-releases?limit=10"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    token = get_access_token()
    if not token:
        print("无法获取 Token")
        return
    
    print("✅ Spotify 连接成功！")
    print(f"Token: {token[:20]}...")
    
    # 获取最新发行
    releases = get_new_releases(token)
    print("\n🎵 最新发行:")
    for album in releases.get('albums', {}).get('items', []):
        print(f"  - {album['name']} by {album['artists'][0]['name']}")

if __name__ == "__main__":
    main()
