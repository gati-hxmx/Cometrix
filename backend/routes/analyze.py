# routes/analyze.py （FastAPIバージョン）
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tasks.chat_tasks import analyze_youtube_chat
from services.user_service import get_user_id_by_email
from celery.result import AsyncResult
from celery_app import celery_app

router = APIRouter()

class AnalyzeRequest(BaseModel):
    videoId: str
    email: str

@router.post("/youtube/async")
def analyze_youtube_async(data: AnalyzeRequest):
    user_id = get_user_id_by_email(data.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    task = analyze_youtube_chat.delay(data.videoId, user_id)
    return {
        "message": "分析ジョブをキューに登録しました",
        "task_id": task.id
    }

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
