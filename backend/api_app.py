from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as fetch_twitch_chat_data
import os
import subprocess
import json
from pydantic import BaseModel
from services.user_service import get_user_id_by_email

app = FastAPI()
CHAT_DATA_DIR = "chat_data"  # 保存先パス

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

@app.post("/api/chat-data/twitch")
def get_twitch_chat_data_post(data: ChatDataRequest):
    user_id = get_user_id_by_email(data.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    raw_path = os.path.join(CHAT_DATA_DIR, f"{data.videoId}.json")
    if not os.path.exists(raw_path):
        subprocess.run([
            "./TwitchDownloaderCLI/TwitchDownloaderCLI", "chatdownload",
            "--id", data.videoId,
            "--output", raw_path
        ], check=True)

    return fetch_twitch_chat_data(raw_path, data.videoId, user_id)


    

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
