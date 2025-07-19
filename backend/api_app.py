from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import subprocess
import json

# --- Services ---
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as fetch_twitch_chat_data
from services.user_service import get_user_id_by_email
from services.delete_service import delete_user_account
from services.stripe_service import cancel_stripe_subscription_immediately

# --- DB ---
from sqlalchemy_db import get_db

# --- App Setup ---
app = FastAPI()
CHAT_DATA_DIR = "chat_data"  # 保存先パス

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class ChatDataRequest(BaseModel):
    videoId: str
    email: str

class DeleteRequest(BaseModel):
    email: str

# --- YouTube チャット取得 ---
@app.post("/api/chat-data")
def get_chat_data_post(data: ChatDataRequest):
    user_id = get_user_id_by_email(data.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return fetch_youtube_chat_data(video_id=data.videoId, user_id=user_id)

# --- Twitch チャット取得 ---
@app.post("/api/chat-data/twitch")
def get_twitch_chat_data_post(data: ChatDataRequest):
    user_id = get_user_id_by_email(data.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    os.makedirs(CHAT_DATA_DIR, exist_ok=True)
    raw_path = os.path.join(CHAT_DATA_DIR, f"{data.videoId}.json")

    if not os.path.exists(raw_path):
        subprocess.run([
            "./TwitchDownloaderCLI/TwitchDownloaderCLI", "chatdownload",
            "--id", data.videoId,
            "--output", raw_path
        ], check=True)

    return fetch_twitch_chat_data(raw_path, data.videoId, user_id)

# --- 退会処理 ---
@app.post("/api/delete-account")
def delete_account(data: DeleteRequest, db: Session = Depends(get_db)):
    user_id = get_user_id_by_email(data.email)
    if not user_id:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    try:
        delete_user_account(db=db, user_id=user_id)
        return {"message": "アカウントを削除しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"退会処理に失敗しました: {str(e)}")

# --- Stripe サブスク即時キャンセル（テスト用） ---
@app.post("/api/test-cancel-stripe")
def test_cancel_stripe(email: str):
    try:
        cancel_stripe_subscription_immediately(email)
        return {"message": f"{email} のサブスクリプションを即時キャンセルしました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"キャンセル失敗: {str(e)}")
