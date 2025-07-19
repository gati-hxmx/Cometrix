# backend/services/yt_chat.py

import subprocess
import tempfile
import os
import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict
from services.log_service import save_analysis_log
import models

def fetch_chat_data(video_id: str, user_id: int) -> Dict:
    from subprocess import check_output

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    save_path = os.path.join("chat_data", f"youtube_{video_id}.json")

    # ✅ 整形済みファイルがあれば再利用＆ログ保存だけ行う
    if os.path.exists(save_path):
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            save_analysis_log(
                user_id=user_id,
                video_url=video_url,
                video_title=data.get("title", ""),
                platform="youtube",
                duration_sec=data.get("duration_sec", 0),
                comment_count=len(data.get("comments", [])),
                result_path=save_path
            )

            print("[INFO] 整形済みファイルを再利用してログ保存✅")
            return {
                **data,
                "video_url": video_url,
                "thumbnail_url": thumbnail_url
            }
        except Exception as e:
            print(f"[WARN] 整形済みファイル読み込みエラー: {e}")
            # 続行して再取得

    # ✅ 新しく取得する処理
    try:
        title = check_output(["yt-dlp", "--get-title", video_url], text=True).strip()
        duration_str = check_output(["yt-dlp", "--get-duration", video_url], text=True).strip()
        hms = [int(p) for p in duration_str.split(":")]
        while len(hms) < 3:
            hms.insert(0, 0)
        h, m, s = hms
        duration_sec = h * 3600 + m * 60 + s
    except Exception as e:
        print("🟥 メタ情報取得失敗:", e)
        title, duration_sec = "", 0

    with tempfile.TemporaryDirectory() as tmpdir:
        command = [
            "yt-dlp",
            video_url,
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
                        if author and text:
                            comments.append({
                                "author": author,
                                "text": text,
                                "timestamp": round(offset_sec, 2),
                                "time_str": video_time_str
                            })
                except Exception as e:
                    print(f"[WARN] Skipped one line: {e}")

        volume_per_30s = compute_volume_per_30s(comments)

        os.makedirs("chat_data", exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f_out:
            json.dump({
                "videoId": video_id,
                "title": title,
                "duration_sec": duration_sec,
                "comments": comments,
                "volume_per_30s": volume_per_30s
            }, f_out, ensure_ascii=False, indent=2)

        save_analysis_log(
            user_id=user_id,
            video_url=video_url,
            video_title=title,
            platform="youtube",
            duration_sec=duration_sec,
            comment_count=len(comments),
            result_path=save_path
        )

        return {
            "videoId": video_id,
            "video_url": video_url,
            "title": title,
            "duration_sec": duration_sec,
            "thumbnail_url": thumbnail_url,
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
