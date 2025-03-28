# Discord Bot プロジェクトドキュメント

## プロジェクト概要
このプロジェクトはDiscord用のカスタムボットを実装したものです。以下の主要機能を含みます：
- Discord APIとの統合
- カスタムコマンド処理
- 拡張可能なモジュールアーキテクチャ

## ディレクトリ構造
```
.
├── src/               # メインソースコード
│   ├── bot/           # ボットコア機能
│   │   ├── cogs/      # ボットの機能別モジュール (Cog)
│   │   ├── api_client.py # 外部APIクライアント
│   │   ├── core.py    # ボットの基本クラス
│   │   └── utils.py   # ユーティリティ関数
│   ├── config.py      # 設定管理
│   └── server.py      # FastAPIサーバー & ボット起動エントリーポイント
├── tests/             # テストコード
└── docs/              # ドキュメント
```

## クイックスタート
1. 必要な依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```
2. 設定ファイルを準備:
   ```bash
   cp .env.example .env
   # .env ファイルに必要なトークンなどを設定
   ```
3. 開発サーバーを起動 (FastAPIサーバーとボットが起動します):
   ```bash
   uvicorn src.server:app --reload
   ```

[詳細なインストールガイド](installation.md) | [設定リファレンス](configuration.md)