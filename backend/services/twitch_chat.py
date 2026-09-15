import json
from datetime import timedelta
from typing import List, Dict
from collections import defaultdict
import os
import subprocess

from services.log_service import save_analysis_log
import models

from dotenv import load_dotenv
from services.twitch_api import (
    get_twitch_access_token,
    get_twitch_thumbnail_url,
    get_twitch_video_title,  # ✅ タイトル取得を追加
)

load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "chat_data"))
CLI_EXECUTABLE = os.path.abspath(
    os.path.join(BASE_DIR, "..", "TwitchDownloaderCLI", "TwitchDownloaderCLI")
)

os.makedirs(CHAT_DATA_DIR, exist_ok=True)


def fetch_chat_data(json_path: str, video_id: str, user_id: int) -> Dict:

    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        raise RuntimeError("Twitch の認証情報が未設定です")

    access_token = get_twitch_access_token(
        TWITCH_CLIENT_ID,
        TWITCH_CLIENT_SECRET,
    )
    # ✅ JSONファイルが存在しない場合、CLIで取得
    if not os.path.exists(json_path):
        try:
            subprocess.run(
                [
                    CLI_EXECUTABLE,
                    "chatdownload",
                    "--id",
                    video_id,
                    "--output",
                    json_path,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"TwitchDownloaderCLIの実行に失敗: {e}")
        except FileNotFoundError as e:
            raise RuntimeError(f"TwitchDownloaderCLIが見つかりません: {e}")

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

                comments.append(
                    {
                        "author": author,
                        "text": text,
                        "timestamp": round(offset_sec, 2),
                        "time_str": str(timedelta(seconds=int(offset_sec))),
                    }
                )
            except Exception as e:
                print(f"[WARN] コメントスキップ: {e}")

    volume_per_30s = compute_volume_per_30s(comments)

    # ✅ chat_data に保存
    save_path = os.path.join(CHAT_DATA_DIR, f"twitch_{video_id}.json")
    with open(save_path, "w", encoding="utf-8") as f_out:
        json.dump(
            {"comments": comments, "volume_per_30s": volume_per_30s},
            f_out,
            ensure_ascii=False,
            indent=2,
        )

    # ✅ タイトル・サムネ取得
    title = get_twitch_video_title(video_id, TWITCH_CLIENT_ID, access_token)
    thumbnail_url = get_twitch_thumbnail_url(
        video_id, TWITCH_CLIENT_ID, access_token
    )
    video_url = f"https://www.twitch.tv/videos/{video_id}"
    duration_sec = int(max(c["timestamp"] for c in comments)) if comments else 0

    # ✅ 分析ログ保存
    save_analysis_log(
        user_id=user_id,
        video_url=video_url,
        video_title=title,
        platform="twitch",
        duration_sec=duration_sec,
        comment_count=len(comments),
        result_path=save_path,
        thumbnail_url=thumbnail_url,
    )

    return {
        "videoId": video_id,
        "video_url": video_url,
        "title": title,
        "duration_sec": duration_sec,
        "comments": comments,
        "volume_per_30s": volume_per_30s,
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
        {"start": k, "start_str": format_hhmmss(k), "count": v}
        for k, v in sorted(bins.items())
    ]
