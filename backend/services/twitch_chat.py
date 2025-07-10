import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict
import os  # ファイル保存のため
from services.log_service import save_analysis_log 
import models

def fetch_chat_data(json_path: str, video_id: str) -> Dict:
    comments = []
    with open(json_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
        raw_comments = all_data.get("comments", [])

        for c in raw_comments:
            try:
                offset_sec = float(c.get("content_offset_seconds", 0))
                author = c.get("commenter", {}).get("display_name", "")
                text = c.get("message", {}).get("body", "")

                if not (author and text):
                    continue

                comments.append({
                    "author": author,
                    "text": text,
                    "timestamp": round(offset_sec, 2),
                    "time_str": str(timedelta(seconds=int(offset_sec)))
                })

            except Exception as e:
                print(f"[WARN] Skipped one comment: {e}")

    volume_per_30s = compute_volume_per_30s(comments)

    # ✅ chat_data に保存
    save_dir = "backend/chat_data"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"twitch_{video_id}.json")

    with open(save_path, "w", encoding="utf-8") as f_out:
        json.dump({
            "comments": comments,
            "volume_per_30s": volume_per_30s
        }, f_out, ensure_ascii=False, indent=2)

    # ✅ 分析ログを保存
    duration_sec = int(max(c["timestamp"] for c in comments)) if comments else 0
    video_url = f"https://www.twitch.tv/videos/{video_id}"

    save_analysis_log(
        user_id=999,
        video_url=video_url,
        video_title="",  # メタ取得しない場合は空文字
        platform="twitch",
        duration_sec=duration_sec,
        comment_count=len(comments),
        result_path=save_path
    )

    return {
        "videoId": video_id,
        "video_url": video_url,
        "title": "",  # 任意でメタ情報取得も可能
        "duration_sec": duration_sec,
        "comments": comments,
        "volume_per_30s": volume_per_30s
    }




def format_hhmmss(seconds: int) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

def compute_volume_per_30s(comments: List[Dict]) -> List[Dict]:
    bins = defaultdict(int)
    for c in comments:
        sec = int(c["timestamp"])
        bucket = (sec // 30) * 30
        bins[bucket] += 1

    return [
        {
            "start": k,
            "start_str": format_hhmmss(k),
            "count": v
        }
        for k, v in sorted(bins.items())
    ]
