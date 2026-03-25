#!/usr/bin/env python3
"""
Spotify 获取用户音乐品味
"""

import requests
import base64
import json

CLIENT_ID = "12f74695ce834e8a829d0035beaddcc6"
CLIENT_SECRET = "2155b3bb4e84447096215af508166f91"
REDIRECT_URI = "https://example.com/callback"
AUTH_CODE = "AQBdNE0ttkz83GG2Cd2Sib6fW53hvniTFc2MCd3V3pDAq21UXVU3WcANAGJ_jSzJqCATElD2oMEfzYdsZsPlgHdTB6pgSeBrOhSj_gKEOB7T4-CiEhSuPDRpIHjZiAO5DZEYHmzwFVaF2c3shTkH_rr2fw4cN5ur3COK9ZVk-8_EM41fgomBzselNyLUmhekOWw_ICydOjtHiIWIegPYaeRIKW_TRz_OeXPI8Aa-ipe-dvRs1cZQekOYRsb6aSSOGWvBdYg4j3txoQi4VjqE5oNKSqo"

def get_access_token():
    """用 Authorization Code 换 Access Token"""
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取 Token 失败: {response.status_code}")
        print(response.text)
        return None

def get_top_tracks(token, limit=10):
    """获取最常听的歌曲"""
    url = f"https://api.spotify.com/v1/me/top/tracks?limit={limit}&time_range=short_term"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_top_artists(token, limit=10):
    """获取最常听的艺人"""
    url = f"https://api.spotify.com/v1/me/top/artists?limit={limit}&time_range=short_term"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_recently_played(token, limit=10):
    """获取最近播放"""
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    print("🎵 正在连接 Spotify...")
    
    # 获取 Token
    token_data = get_access_token()
    if not token_data:
        return
    
    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token", "")
    
    print(f"✅ 连接成功！")
    print(f"   Access Token: {access_token[:20]}...")
    print(f"   Refresh Token: {refresh_token[:20]}..." if refresh_token else "   Refresh Token: None")
    print()
    
    # 保存 Token 供以后使用
    with open("/root/.openclaw/workspace/config/spotify_token.json", "w") as f:
        json.dump(token_data, f, indent=2)
    print("💾 Token 已保存到 config/spotify_token.json")
    print()
    
    # 获取最常听的歌曲
    print("🎧 最近常听的歌曲 (Top 10):")
    top_tracks = get_top_tracks(access_token)
    for i, track in enumerate(top_tracks.get('items', []), 1):
        artists = ", ".join([a['name'] for a in track['artists']])
        print(f"   {i}. {track['name']} - {artists}")
    print()
    
    # 获取最常听的艺人
    print("🎤 最近常听的艺人 (Top 10):")
    top_artists = get_top_artists(access_token)
    for i, artist in enumerate(top_artists.get('items', []), 1):
        genres = ", ".join(artist.get('genres', [])[:3])
        print(f"   {i}. {artist['name']}")
        if genres:
            print(f"      风格: {genres}")
    print()
    
    # 获取最近播放
    print("⏮️ 最近播放:")
    recent = get_recently_played(access_token)
    for i, item in enumerate(recent.get('items', [])[:5], 1):
        track = item['track']
        artists = ", ".join([a['name'] for a in track['artists']])
        played_at = item.get('played_at', '')[:10]
        print(f"   {i}. {track['name']} - {artists} ({played_at})")

if __name__ == "__main__":
    main()
