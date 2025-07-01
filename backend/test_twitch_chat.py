import os
import tempfile
import json
import subprocess
from datetime import timedelta

# 対象のTwitch URL
twitch_url = "https://www.twitch.tv/videos/2492994298"

# 一時ディレクトリで作業
with tempfile.TemporaryDirectory() as temp_dir:
    print("[DEBUG] temp dir:", temp_dir)

    # yt-dlpでコメント取得（--write-comments）
    subprocess.run([
        "yt-dlp",
        "--skip-download",
        "--write-comments",
        "--no-warnings",
        "-P", temp_dir,
        twitch_url
    ], check=True)

    # 出力された .comments.json ファイルを探す
    comment_file = None
    for fname in os.listdir(temp_dir):
        if fname.endswith(".comments.json"):
            comment_file = os.path.join(temp_dir, fname)
            break

    if not comment_file:
        raise FileNotFoundError("コメントファイルが見つかりませんでした。")

    print("[DEBUG] found:", comment_file)

    # コメントファイル読み込み
    with open(comment_file, "r", encoding="utf-8") as f:
        comments_raw = json.load(f)

    # 整形して出力
    formatted = []
    for c in comments_raw:
        seconds = int(c.get("timestamp", 0))
        formatted.append({
            "time": seconds,
            "timestamp_hhmmss": str(timedelta(seconds=seconds)),
            "author": c.get("author", ""),
            "text": c.get("message", "")
        })

    print(f"取得コメント数: {len(formatted)}")
    print("最初の5件:")
    for item in formatted[:5]:
        print(item)
