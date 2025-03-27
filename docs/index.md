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
│   ├── config.py      # 設定管理
│   └── server.py      # 補助サーバー
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
   ```
3. ボットを起動:
   ```bash
   python src/bot.py
   ```

[詳細なインストールガイド](installation.md) | [設定リファレンス](configuration.md)