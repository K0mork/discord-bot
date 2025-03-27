# インストールガイド

## 前提条件
- Python 3.8以上
- pip 最新版
- Docker（オプション）

## 手動インストール
1. リポジトリをクローン:
   ```bash
   git clone https://github.com/your-repo/discord-bot.git
   cd discord-bot
   ```

2. 仮想環境を作成（推奨）:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # または venv\Scripts\activate (Windows)
   ```

3. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

4. 環境変数を設定:
   ```bash
   cp .env.example .env
   # .envファイルを編集して必要な設定を追加
   ```

## Dockerを使用する場合
```bash
docker build -t discord-bot .
docker run -d --env-file .env discord-bot
```

## 初期設定の確認
ボットが正しく動作するかテスト:
```bash
python src/bot.py --test
```

[設定の詳細](configuration.md) | [APIリファレンス](api_reference.md)