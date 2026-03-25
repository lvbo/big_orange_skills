#!/usr/bin/env python3
"""
Spotify 用户授权流程
"""

CLIENT_ID = "12f74695ce834e8a829d0035beaddcc6"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPES = "user-read-recently-played user-top-read user-library-read playlist-read-private"

auth_url = (
    f"https://accounts.spotify.com/authorize"
    f"?client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPES.replace(' ', '%20')}"
)

print("🔗 复制以下链接到浏览器打开：")
print()
print(auth_url)
print()
print("授权后，把浏览器地址栏的完整 URL 发给我")
print()
print("需要在 Spotify Dashboard 里配置 Redirect URI:")
print(f"   {REDIRECT_URI}")
