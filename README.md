# Dodgers Discord Bot

ドジャースの試合情報を提供するDiscordボット

## 機能

- `!dodgers` コマンドで今日の試合情報を表示
  - 対戦カード
  - 試合開始時間 (日本時間)
  - 試合状況
  - スコア (試合中の場合)

## 技術スタック

- Python 3.10
- Discord.py
- FastAPI
- Docker

## 環境構築

1. リポジトリをクローン
```bash
git clone https://github.com/your-repo/dodgers-bot.git
cd dodgers-bot
```

2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. 開発サーバーの起動
```bash
uvicorn src.server:app --reload
```

## Dockerでの実行

```bash
docker build -t dodgers-bot .
docker run -p 8000:8000 --env-file .env dodgers-bot
```

## デプロイ (Koyeb)

1. Koyebに新しいアプリを作成
2. GitHubリポジトリを選択
3. 環境変数を設定
4. デプロイ

## 開発

```bash
# テストの実行
pytest

# コードフォーマット
black .
isort .
```

## ライセンス

MIT