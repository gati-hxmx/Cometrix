# Cometrix

YouTube Live / Twitch配信のチャットログを取得し、コメント数の推移や内容を分析・可視化するWebアプリケーションです。Googleアカウントでログインし、動画URLを入力するとチャットを非同期で解析、再生位置と連動したグラフ・チャット一覧で確認できます。

## 主な機能

- Google OAuthによるログイン/新規登録
- YouTube Live / Twitch アーカイブのチャットログ取得・分析(非同期ジョブ)
- 30秒単位のコメント数推移グラフ(クリックでその時刻の動画再生位置にシーク)
- キーワード/ユーザー名によるチャットフィルタ
- 分析履歴の保存・閲覧
- Stripeによるサブスクリプション課金(Checkout / Webhook連携)

## 技術スタック

| レイヤ | 技術 |
|---|---|
| フロントエンド | Vue 3 (Composition API) / Vite / Pinia / Vue Router / Tailwind CSS / Chart.js |
| バックエンド(認証・決済) | Flask / Flask-Login / Flask-Dance(Google OAuth) / Stripe |
| バックエンド(分析API) | FastAPI |
| 非同期ジョブ | Celery + Redis |
| データベース | PostgreSQL(SQLAlchemy ORM) |
| チャット取得 | yt-dlp(YouTube) / TwitchDownloaderCLI(Twitch) |

## アーキテクチャ

役割ごとにバックエンドプロセスが分かれており、フロントエンドから各ポートに直接アクセスします。

```
frontend (Vite, :5173)
   ├─→ auth_app.py   (Flask, :5000)  … Google OAuth / ユーザー・サブスク情報
   ├─→ stripe_app.py (Flask, :5001)  … Stripe Checkout / Webhook
   └─→ api_app.py    (FastAPI, :8000) … チャット分析ジョブの発行・履歴取得
                              │
                              ▼
                     Celery worker ── Redis(ジョブキュー) ── PostgreSQL
```

フロントの参照先URLは `frontend/.env`(`VITE_AUTH_API_URL` など)で環境ごとに切り替えられます。詳細は `frontend/.env.example` を参照してください。

## セットアップ

### 前提条件

- Node.js / npm
- Python 3.12 系
- Docker(PostgreSQL・Redisをコンテナで起動する場合)

### 1. インフラ起動(PostgreSQL / Redis)

```bash
docker compose up -d
```

### 2. バックエンド

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 値を埋める(Google OAuth / Stripe / DB 等)
```

`.env` の各項目の取得元は `.env.example` のコメントを参照してください。

DBテーブルの作成:

```bash
python -c "from sqlalchemy_db import Base, engine; import models; from models import billing_history; Base.metadata.create_all(bind=engine)"
```

サーバー起動(3プロセスをまとめて起動):

```bash
npm run dev
```

Celeryワーカー(別ターミナルで起動):

```bash
source .venv/bin/activate
celery -A celery_app worker --loglevel=info
```

### 3. フロントエンド

```bash
cd frontend
npm install
cp .env.example .env   # ローカルのままでよければ変更不要
npm run dev
```

`http://localhost:5173` にアクセスして動作確認できます。

## テスト

```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

`backend/.env` のDB接続情報を使って実際にPostgreSQLへ書き込み・検証を行います。

## ディレクトリ構成(抜粋)

```
backend/
  auth_app.py        Flask: Google OAuth / ユーザー・サブスク管理
  stripe_app.py       Flask: Stripe決済
  api_app.py           FastAPI: チャット分析API
  celery_app.py       Celeryアプリ定義
  tasks/chat_tasks.py  非同期タスク本体
  services/            YouTube/Twitchチャット取得・分析ロジック
  models/              SQLAlchemyモデル
  routes/              FastAPIルーター
  tests/               pytest

frontend/
  src/views/           画面(ログイン・分析・マイページ・請求関連 など)
  src/components/      分析画面の各パーツ(グラフ・チャット一覧・プレイヤー等)
  src/stores/           Piniaストア(ユーザー状態・チャットデータ)
  src/config/api.js     バックエンドAPIのベースURL設定
```
