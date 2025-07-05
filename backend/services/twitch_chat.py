import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict

def fetch_chat_data(json_path: str) -> Dict:
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
