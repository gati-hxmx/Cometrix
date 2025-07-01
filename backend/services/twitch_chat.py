import json
import datetime
import os

def parse_twitch_comments(video_id):
    json_path = f"{video_id}.comments.json"

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} が存在しません")

    comments = []

    with open(json_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                content_offset_seconds = int(data['content_offset_seconds'])
                timestamp = str(datetime.timedelta(seconds=content_offset_seconds))
                author = data['comment']['commenter']['display_name']
                text = data['comment']['message']['body']

                comments.append({
                    "time": content_offset_seconds,
                    "timestamp_hhmmss": timestamp,
                    "author": author,
                    "text": text
                })
            except Exception as e:
                print(f"スキップされた行（エラー: {e}）")

    return comments
