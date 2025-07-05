from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as parse_twitch_chat
import os
import subprocess
import json

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
    os.makedirs(CHAT_DATA_DIR, exist_ok=True)
    parsed_path = os.path.join(CHAT_DATA_DIR, f"youtube_{videoId}.json")

    # ✅ 整形済みがあればそれを返す
    if os.path.exists(parsed_path):
        try:
            with open(parsed_path, "r", encoding="utf-8") as f:
                print(f"[INFO] YouTube整形済みファイルを読み込み✅")
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 整形済みファイルの読み込み失敗: {e}")
            # → 続行して再取得

    # ✅ なければ新しく取得・整形
    try:
        return fetch_youtube_chat_data(videoId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"チャットデータの取得に失敗しました: {e}")


# ✅ Twitch用エンドポイント
CHAT_DATA_DIR = "backend/chat_data"  # 保存先パス

@app.get("/api/analyze/twitch/{video_id}")
def analyze_twitch(video_id: str):
    os.makedirs(CHAT_DATA_DIR, exist_ok=True)

    # 整形済みファイル
    parsed_path = os.path.join(CHAT_DATA_DIR, f"twitch_{video_id}.json")
    # CLI出力の生ファイル
    raw_path = os.path.join(CHAT_DATA_DIR, f"{video_id}.json")

    # ✅ 1. 整形済みファイルがあればそれを返す
    if os.path.exists(parsed_path):
        try:
            with open(parsed_path, "r", encoding="utf-8") as f:
                print(f"[INFO] Twitch整形済みファイルを読み込み✅")
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 整形済みファイルの読み込み失敗: {e}")
            # → 続行して再ダウンロード＋再整形

    # ✅ 2. 生ファイルがなければCLIでダウンロード
    if not os.path.exists(raw_path):
        try:
            subprocess.run([
                "./TwitchDownloaderCLI/TwitchDownloaderCLI", "chatdownload",
                "--id", video_id,
                "--output", raw_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"チャット取得に失敗しました: {e}")

    # ✅ 3. 整形して保存 → 返却
    try:
        return parse_twitch_chat(raw_path, video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSONパース失敗: {e}")

