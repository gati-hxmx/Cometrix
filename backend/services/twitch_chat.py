import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict
import os  # ファイル保存のため

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

    return {
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
