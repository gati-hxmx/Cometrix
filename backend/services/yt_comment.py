# backend/services/yt_comment.py

print("🔄 yt_comment.py LOADED")

import yt_dlp

print("🔄 yt_comment.py LOADED")

def extract_comments(video_url: str, max_comments: int = 100):
    print("🟢 Step 1: extract_comments() called")

    ydl_opts = {
        'skip_download': True,
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': True,
        'extractor_args': ['youtube:comments'],
        'max_downloads': max_comments,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    print("🟢 Step 2: info received")
    print("📦 info type:", type(info))
    print("📦 info content:", str(info)[:1000])  # 最初の1000文字だけ表示

    # ✅ 安全に型チェック
    if isinstance(info, list):
        raise ValueError("動画が複数検出されたか、プレイリストURLを指定していませんか？")

    # ✅ コメントがなければ空リスト
    comments = info.get('comments', [])

    parsed = [
        {
            'author': c.get('author'),
            'text': c.get('text'),
            'like_count': c.get('like_count'),
            'time': c.get('time'),
        }
        for c in comments
    ]
    return parsed
