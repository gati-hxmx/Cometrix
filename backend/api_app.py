from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as parse_twitch_chat
import os
import subprocess
import json
from pydantic import BaseModel
from services.user_service import get_user_id_by_email

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
    
from pydantic import BaseModel
from services.user_service import get_user_id_by_email

class ChatDataRequest(BaseModel):
    videoId: str
    email: str

@app.post("/api/chat-data")  # ✅ これを追加！
def get_chat_data_post(data: ChatDataRequest):
    user_id = get_user_id_by_email(data.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    return fetch_youtube_chat_data(video_id=data.videoId, user_id=user_id)


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

class TwitchChatRequest(BaseModel):
    videoId: str
    email: str

@app.post("/api/analyze/twitch")
def analyze_twitch_post(data: TwitchChatRequest):
    os.makedirs(CHAT_DATA_DIR, exist_ok=True)

    video_id = data.videoId
    email = data.email

    try:
        user_id = get_user_id_by_email(email)
        if user_id is None:
            raise ValueError("ユーザーが見つかりません")
    except Exception:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    # CLI出力の生ファイル
    raw_path = os.path.join(CHAT_DATA_DIR, f"{video_id}.json")

    # ✅ 生ファイルがなければ CLI で取得
    if not os.path.exists(raw_path):
        try:
            subprocess.run([
                "./TwitchDownloaderCLI/TwitchDownloaderCLI", "chatdownload",
                "--id", video_id,
                "--output", raw_path
            ], check=True)
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"チャット取得に失敗しました: {e}")

    # ✅ 整形・保存・ログ記録
    try:
        return parse_twitch_chat(raw_path, video_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSONパース失敗: {e}")
    

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy_db import get_db
from services.user_service import get_user_id_by_email
from services.delete_service import delete_user_account
from pydantic import BaseModel

class DeleteRequest(BaseModel):
    email: str

@app.post("/api/delete-account")
def delete_account(data: DeleteRequest, db: Session = Depends(get_db)):
    try:
        user_id = get_user_id_by_email(data.email)
        if not user_id:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        delete_user_account(db=db, user_id=user_id)
        return {"message": "アカウントを削除しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"退会処理に失敗しました: {str(e)}")

# api_app.py（または routes/account.py 等）

from fastapi import FastAPI, HTTPException
from services.stripe_service import cancel_stripe_subscription_immediately

@app.post("/api/test-cancel-stripe")
def test_cancel_stripe(email: str):
    try:
        cancel_stripe_subscription_immediately(email)
        return {"message": f"{email} のサブスクリプションを即時キャンセルしました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャンセル失敗: {str(e)}")
