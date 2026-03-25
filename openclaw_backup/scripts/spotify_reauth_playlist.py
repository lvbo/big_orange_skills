#!/usr/bin/env python3
"""
Spotify 重新授权 - 包含创建歌单权限
"""

CLIENT_ID = "12f74695ce834e8a829d0035beaddcc6"
REDIRECT_URI = "https://example.com/callback"

# 增加创建歌单的权限
SCOPES = (
    "user-read-recently-played "
    "user-top-read "
    "user-library-read "
    "playlist-read-private "
    "playlist-modify-private"  # 新增：创建私人歌单
)

auth_url = (
    f"https://accounts.spotify.com/authorize"
    f"?client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPES.replace(' ', '%20')}"
)

print("🔗 需要重新授权以创建歌单")
print()
print("复制以下链接到浏览器打开：")
print()
print(auth_url)
print()
print("授权后，把浏览器地址栏里的完整 URL 发给我")
