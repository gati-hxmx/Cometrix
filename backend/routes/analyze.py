# backend/routes/analyze.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from tasks.chat_tasks import analyze_youtube_chat_task, analyze_twitch_chat_task
from celery.result import AsyncResult
from celery_app import celery_app
from services.user_service import get_user_id_by_email
from auth_dependency import get_current_email

router = APIRouter()

class AnalyzeRequest(BaseModel):
    videoId: str


@router.post("/youtube/async")
def analyze_youtube_async(request: AnalyzeRequest, email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    full_url = f"https://www.youtube.com/watch?v={request.videoId}"  # ←ここで組み立てる
    task = analyze_youtube_chat_task.delay(full_url, user_id)
    return {"task_id": task.id}



@router.get("/task-status/{task_id}")
def get_task_status(task_id: str, email: str = Depends(get_current_email)):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

class AnalyzeTwitchRequest(BaseModel):
    videoId: str


@router.post("/twitch/async")
def analyze_twitch_chat_async(request: AnalyzeTwitchRequest, email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    task = analyze_twitch_chat_task.delay(request.videoId, user_id)
    return {"task_id": task.id}

# @router.post("/twitch/async")
# async def analyze_twitch_chat_async(request: AnalyzeTwitchRequest):
#     user_id = get_user_id_by_email(request.email)
#     if user_id is None:
#         raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

#     task = analyze_twitch_chat_task.delay(
#         json_path=request.json_path,
#         video_id=request.video_id,
#         user_id=user_id
#     )
#     return {"task_id": task.id}
