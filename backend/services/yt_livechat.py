# services/yt_livechat.py

import yt_dlp
import json
import os

def extract_live_chat(video_url: str):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'subtitleslangs': ['live_chat'],
        'outtmpl': '%(id)s',  # 出力ファイル名を動画IDベースに固定
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_id = info.get('id')

    filename = f"{video_id}.live_chat.json"
    if not os.path.exists(filename):
        print("📁 現在のディレクトリ内ファイル一覧:")
        print(os.listdir('.'))
        raise FileNotFoundError(f"{filename} が生成されませんでした")

    with open(filename, 'r', encoding='utf-8') as f:
        chat_data = json.load(f)

    # チャットからメッセージのみ抽出
    comments = []
    for entry in chat_data.get('events', []):
        msg = entry.get('message')
        if msg:
            comments.append({
                'author': entry.get('author', 'unknown'),
                'message': msg,
                'timestamp': entry.get('timestamp'),
            })

    # 終了後ファイルを削除
    os.remove(filename)

    return comments
