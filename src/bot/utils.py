from datetime import datetime, timezone, timedelta
from typing import Optional
from .api_client import GameInfo

def utc_to_jst(utc_time_str: str) -> str:
    """UTC時間文字列を日本時間(JST)に変換する
    
    Args:
        utc_time_str: ISO 8601形式のUTC時間文字列 (例: "2023-05-01T12:00:00Z")
    
    Returns:
        str: "YYYY年MM月DD日 HH:MM"形式の日本時間文字列
    """
    try:
        # ISO 8601形式の文字列をdatetimeオブジェクトに変換
        utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        # JST (UTC+9) に変換
        jst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
        return jst_time.strftime('%Y年%m月%d日 %H:%M')
    except ValueError as e:
        print(f"時間変換エラー: {e}")
        return "時間情報なし"

def format_score(game: GameInfo) -> str:
    """試合のスコア情報をフォーマットする
    
    Args:
        game: 試合情報
    
    Returns:
        str: フォーマットされたスコア情報 (スコアがない場合は空文字列)
    """
    if game.status in ("Scheduled", "Pre-Game", "Warmup", "Preview"):
        return ""
    
    home_score = game.home_score or "?"
    away_score = game.away_score or "?"
    return f" ({game.away_team} {away_score} - {home_score} {game.home_team})"

def format_game_info(game: GameInfo) -> str:
    """試合情報をDiscordメッセージ用にフォーマットする
    
    Args:
        game: 試合情報
    
    Returns:
        str: フォーマットされたメッセージ
    """
    score_info = format_score(game)
    game_time = utc_to_jst(game.game_time_utc)
    
    return (
        f"⚾ **今日のドジャースの試合 ({game.date})** ⚾\n"
        f"対戦: {game.away_team} @ {game.home_team}\n"
        f"球場: {game.venue}\n"
        f"状態: {game.status}{score_info}\n"
        f"開始時刻 (日本時間): {game_time}"
    )