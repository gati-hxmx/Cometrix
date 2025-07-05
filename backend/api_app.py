from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as parse_twitch_chat
import os
import subprocess

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて絞る
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/chat-data")
def get_chat_data(videoId: str):
    try:
        return fetch_youtube_chat_data(videoId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"チャットデータの取得に失敗しました: {e}")

# ✅ Twitch用エンドポイント
CHAT_DATA_DIR = "backend/chat_data"  # 保存先パス

@app.get("/api/analyze/twitch/{video_id}")
def analyze_twitch(video_id: str):
    os.makedirs(CHAT_DATA_DIR, exist_ok=True)
    json_path = os.path.join(CHAT_DATA_DIR, f"{video_id}.json")

    # ✅ JSONが未保存ならダウンロード実行
    if not os.path.exists(json_path):
        try:
            subprocess.run([
                "./TwitchDownloaderCLI/TwitchDownloaderCLI", "chatdownload",
                "--id", video_id,
                "--output", json_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"チャット取得に失敗しました: {e}")

    # ✅ パースして返す
    try:
        return parse_twitch_chat(json_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSONパース失敗: {e}")
