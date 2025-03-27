# 開発ガイド

## プロジェクト構造
```
discord-bot/
├── src/
│   ├── bot/            # ボットコア機能
│   │   ├── api_client.py  # MLB APIクライアント
│   │   ├── core.py     # メインロジック
│   │   └── utils.py    # ユーティリティ関数
│   ├── config.py       # 設定管理
│   └── server.py       # Webサーバー
├── tests/              # テストコード
└── docs/               # ドキュメント
```

## 開発環境設定
1. 開発用依存関係をインストール:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. テストを実行:
   ```bash
   pytest tests/
   ```

## コーディング規約
- PEP 8に準拠
- 型ヒントを使用
- 公開APIにはdocstringを記述
- テストカバレッジ80%以上を目標

## 新しい機能の追加手順
1. 機能ブランチを作成:
   ```bash
   git checkout -b feature/new-feature
   ```

2. テストを書きながら実装

3. 変更をコミット:
   ```bash
   git commit -m "feat: add new feature"
   ```

4. プルリクエストを作成

## デバッグ
- デバッグモードで起動:
  ```bash
  python src/bot.py --debug
  ```

- ログは`logs/`ディレクトリに出力されます

[APIリファレンス](api_reference.md) | [設定リファレンス](configuration.md)