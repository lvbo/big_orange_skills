#!/usr/bin/env python3
"""
在 Spotify 创建木推瓜推荐歌单
使用新的 Authorization Code
"""

import requests
import json
import base64

CLIENT_ID = "12f74695ce834e8a829d0035beaddcc6"
CLIENT_SECRET = "2155b3bb4e84447096215af508166f91"
REDIRECT_URI = "https://example.com/callback"
AUTH_CODE = "AQDhTj9nCehFHTGW9CIS6STk0ddx8xrkbmSuppiZiAuzMR3aUf7taa7P9wcHdPVOWMkDO6AIsUBeWXveEdJwtf65haeWOTRjVi5AMrTsN6WYdEMRy9qc0Ev_nOouImmKobwx11YDJQ9hg7VBQnRkADOawAbuhF2z_8XXmVivkqydl8MvfVBj2jh6RJeyKG6o5m8Mj4dq3kYxsJZ52dUF3K-vylnecv4X8Oq5Wc0A2ITpPhcHK5P8Egl9Rc7WbfjiRLb1bRyWzI-b_wlxT6KSNjxWiDZJqqozbqYkk5DbiMDuvDlOJqtQ9VtJJ03L"

def get_access_token_from_code():
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
        result = response.json()
        # 保存新的 refresh token
        with open("/root/.openclaw/workspace/config/spotify_token.json", "w") as f:
            json.dump(result, f, indent=2)
        return result["access_token"]
    else:
        print(f"获取 Token 失败: {response.status_code}")
        print(response.text)
        return None

def get_user_id(token):
    """获取用户 ID"""
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"获取用户 ID 失败: {response.status_code}")
        return None

def create_playlist(token, user_id, name, description=""):
    """创建歌单"""
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "description": description,
        "public": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"创建歌单失败: {response.status_code}")
        print(response.text)
        return None

def search_track(token, query):
    """搜索歌曲"""
    url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get("tracks", {}).get("items", [])
        if items:
            return items[0]["uri"]
    return None

def add_tracks_to_playlist(token, playlist_id, track_uris):
    """添加歌曲到歌单"""
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"uris": track_uris}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201

def main():
    print("🎵 正在创建木推瓜推荐歌单...")
    
    # 用新 code 获取 Token
    token = get_access_token_from_code()
    if not token:
        return
    
    print(f"✅ Token 获取成功")
    
    # 获取用户 ID
    user_id = get_user_id(token)
    if not user_id:
        return
    
    print(f"👤 用户: {user_id}")
    
    # 创建歌单
    playlist_id = create_playlist(
        token, user_id, 
        "木推瓜推荐", 
        "大橘子推荐：木推瓜精选曲目"
    )
    if not playlist_id:
        return
    
    print(f"✅ 歌单已创建")
    
    # 搜索木推瓜的歌曲
    tracks_to_search = [
        "木推瓜 孔雀东南飞",
        "木推瓜 石敢当",
        "木推瓜 泰山石敢当",
        "木推瓜 鸟人",
        "木推瓜 哆嗦哆",
        "木推瓜 悲剧的诞生",
        "木推瓜 点醒",
        "木推瓜 钢铁是怎样没有炼成的"
    ]
    
    track_uris = []
    print("\n🔍 搜索歌曲...")
    for track in tracks_to_search:
        uri = search_track(token, track)
        if uri:
            track_uris.append(uri)
            print(f"  ✓ {track}")
        else:
            print(f"  ✗ {track} (未找到)")
    
    # 添加歌曲
    if track_uris:
        if add_tracks_to_playlist(token, playlist_id, track_uris):
            print(f"\n✅ 已添加 {len(track_uris)} 首歌曲")
            print(f"🔗 歌单链接: https://open.spotify.com/playlist/{playlist_id}")
        else:
            print("❌ 添加歌曲失败")
    else:
        print("❌ 未找到任何歌曲")

if __name__ == "__main__":
    main()
