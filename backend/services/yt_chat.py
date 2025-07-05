# backend/services/yt_chat.py

import subprocess
import tempfile
import os
import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict

def fetch_chat_data(video_id: str) -> Dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        command = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={video_id}",
            "--skip-download",
            "--write-subs",
            "--sub-langs", "live_chat",
            "--output", "%(id)s",
            "--no-warnings",
            "--quiet"
        ]
        subprocess.run(command, check=True, cwd=tmpdir)

        json_path = os.path.join(tmpdir, f"{video_id}.live_chat.json")
        comments = []

        with open(json_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    raw = json.loads(line)
                    video_offset_ms = raw.get("replayChatItemAction", {}).get("videoOffsetTimeMsec")
                    if not video_offset_ms:
                        continue

                    offset_sec = int(video_offset_ms) / 1000
                    video_time_str = str(timedelta(seconds=int(offset_sec)))

                    actions = raw.get("replayChatItemAction", {}).get("actions", [])
                    for act in actions:
                        renderer = (
                            act.get("addChatItemAction", {})
                            .get("item", {})
                            .get("liveChatTextMessageRenderer", {})
                        )
                        if not renderer:
                            continue

                        runs = renderer.get("message", {}).get("runs", [])
                        text = "".join([r.get("text", "") for r in runs])
                        author = renderer.get("authorName", {}).get("simpleText", "")

                        if not (author and text):
                            continue

                        comments.append({
                            "author": author,
                            "text": text,
                            "timestamp": round(offset_sec, 2),
                            "time_str": video_time_str
                        })

                except Exception as e:
                    print(f"[WARN] Skipped one line: {e}")

        volume_per_30s = compute_volume_per_30s(comments)

        # ✅ 整形後のコメントを保存する
        os.makedirs("backend/chat_data", exist_ok=True)
        save_path = os.path.join("backend/chat_data", f"youtube_{video_id}.json")
        with open(save_path, "w", encoding="utf-8") as f_out:
            json.dump({
                "videoId": video_id,
                "comments": comments,
                "volume_per_30s": volume_per_30s
            }, f_out, ensure_ascii=False, indent=2)

        return {
            "videoId": video_id,
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
            "start": k,  # 例: 0, 30, 60...
            "start_str": format_hhmmss(k),  # 例: "00:00:00", "00:00:30"
            "count": v
        }
        for k, v in sorted(bins.items())
    ]
