# 設定リファレンス

## 必須設定

### DISCORD_BOT_TOKEN
Discordボットの認証トークン。Discord Developer Portalで取得可能。

```env
DISCORD_BOT_TOKEN=your_bot_token_here
```

## オプション設定

### PORT
Webサーバーのポート番号。デフォルトは8000。

```env
PORT=8000
```

### MLB_API_ENDPOINT
MLB APIのエンドポイントURL。デフォルトは以下：
```
https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&date={date}
```

## 設定例

```env
# 最低限必要な設定
DISCORD_BOT_TOKEN=your_bot_token_here

# オプション設定
PORT=8080
MLB_API_ENDPOINT=https://statsapi.mlb.com/api/v1/custom_endpoint
```

## 注意事項
- 設定変更後はボットを再起動してください
- トークンは秘密情報として扱い、バージョン管理システムにコミットしないでください
- 本番環境では.envファイルではなく、環境変数を使用することを推奨します

[インストールガイド](installation.md) | [APIリファレンス](api_reference.md)