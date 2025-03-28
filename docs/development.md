# 開発ガイド

## プロジェクト構造
```
discord-bot/
├── src/
│   ├── bot/            # ボットコア機能
│   │   ├── cogs/       # ボットの機能別モジュール (Cog)
│   │   ├── api_client.py  # MLB APIクライアント
│   │   ├── core.py     # ボットの基本クラス
│   │   └── utils.py    # ユーティリティ関数
│   ├── config.py       # 設定管理
│   └── server.py       # FastAPIサーバー & ボット起動エントリーポイント
├── tests/              # テストコード
└── docs/               # ドキュメント
```

## 開発環境設定
1. 依存関係をインストール (開発用ツールも含む):
   ```bash
   pip install -r requirements.txt
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

2. 新しいコマンドやイベントリスナーは `src/bot/cogs/` 以下に新しい Cog ファイルを作成するか、既存の Cog に追加します。
   - Cog の詳細については `discord.py` のドキュメントを参照してください。

3. テストを書きながら実装します。

4. 変更をコミット:
   ```bash
   git commit -m "feat: add new feature"
   ```

5. プルリクエストを作成します。

## デバッグ
- 開発サーバーを起動 (FastAPIとボット):
  ```bash
  uvicorn src.server:app --reload
  ```
- ログはコンソール (標準出力/エラー) に出力されます。ログレベルは `src/server.py` の `logging.basicConfig` で設定されています。

[APIリファレンス](api_reference.md) | [設定リファレンス](configuration.md)