import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_twitch_access_token(client_id: str, client_secret: str) -> str:
    url = "https://id.twitch.tv/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def get_twitch_thumbnail_url(video_id: str, client_id: str, access_token: str) -> str:
    url = f"https://api.twitch.tv/helix/videos?id={video_id}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    try:
        raw_url = data["data"][0]["thumbnail_url"]
        # 👇 TwitchのテンプレURLを実サイズに変換
        return raw_url.replace("%{width}", "640").replace("%{height}", "360")
    except (IndexError, KeyError):
        return None

