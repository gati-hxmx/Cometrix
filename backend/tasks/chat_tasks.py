from celery import Celery
from services.yt_chat import analyze_youtube_chat
import os
# from services.twitch_chat import analyze_twitch_chat  # 将来用

celery_app = Celery(
    "cometrix",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def analyze_youtube_chat_task(video_url: str, user_id: str = None):
    print("🔍 現在の作業ディレクトリ:", os.getcwd())
    result = analyze_youtube_chat(video_url, user_id=user_id)
    return result

# @celery_app.task
# def analyze_twitch_chat_task(video_url: str, user_id: str = None):
#     result = analyze_twitch_chat(video_url, user_id=user_id)
#     return result
