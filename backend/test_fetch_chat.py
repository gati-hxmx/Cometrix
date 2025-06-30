from services.yt_chat import fetch_chat_data

video_id = "a9sarHdoFYc"
result = fetch_chat_data(video_id)

print(f"取得コメント数: {len(result['comments'])}")
print("最初の5コメント:")
for c in result["comments"][:5]:
    print(f"{c['time_str']} | {c['author']}: {c['text']}")

print("\n棒グラフ用データ（volume_per_30s）:")
for v in result["volume_per_30s"][:5]:
    print(f"{v['start_str']} | {v['count']}件")
