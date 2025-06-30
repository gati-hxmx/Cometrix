# services/yt_test_livechat.py

from yt_livechat import extract_live_chat

comments = extract_live_chat("https://www.youtube.com/watch?v=a9sarHdoFYc")

print(f"取得コメント数: {len(comments)}")
for c in comments[:5]:
    print(f"{c['timestamp']}: {c['author']} - {c['message']}")
