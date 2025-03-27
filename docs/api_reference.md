# APIリファレンス

## 概要
このボットはMLB公式APIを使用してロサンゼルス・ドジャースの試合情報を取得します。

## データ構造

### GameInfo
試合情報を保持するデータクラス。

| フィールド | 型 | 説明 |
|-----------|----|------|
| date | str | 試合日 (YYYY-MM-DD形式) |
| status | str | 試合状態 (例: "Scheduled", "In Progress") |
| home_team | str | ホームチーム名 |
| away_team | str | アウェイチーム名 |
| venue | str | 開催球場名 |
| game_time_utc | str | 試合開始時刻 (UTC) |
| home_score | Optional[str] | ホームチーム得点 (試合中/終了時のみ) |
| away_score | Optional[str] | アウェイチーム得点 (試合中/終了時のみ) |

## 利用可能な関数

### fetch_dodgers_game()
```python
async def fetch_dodgers_game() -> Optional[GameInfo]
```
最新のドジャース試合情報を取得します。

**戻り値**:
- 試合情報 (`GameInfo`) - 試合がある場合
- `None` - 試合がない場合

**例外**:
- `requests.exceptions.RequestException` - APIリクエスト失敗時
- `KeyError`, `ValueError` - データ解析失敗時

## 使用例
```python
from bot.api_client import fetch_dodgers_game

game_info = await fetch_dodgers_game()
if game_info:
    print(f"今日の試合: {game_info.away_team} vs {game_info.home_team}")
```

[設定リファレンス](configuration.md) | [開発ガイド](development.md)