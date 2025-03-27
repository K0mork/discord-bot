import requests
from typing import Dict, Optional
from datetime import date
from dataclasses import dataclass

@dataclass
class GameInfo:
    """試合情報を保持するデータクラス"""
    date: str
    status: str
    home_team: str
    away_team: str
    venue: str
    game_time_utc: str
    home_score: Optional[str] = None
    away_score: Optional[str] = None

MLB_API_ENDPOINT = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&date={date}"

async def fetch_dodgers_game() -> Optional[GameInfo]:
    """ドジャースの試合情報を取得する
    
    Returns:
        Optional[GameInfo]: 試合情報 (試合がない場合はNone)
    """
    try:
        today = date.today().strftime('%Y-%m-%d')
        api_url = MLB_API_ENDPOINT.format(date=today)
        
        response = requests.get(api_url)
        response.raise_for_status()
        schedule_data = response.json()
        
        if not schedule_data['dates'] or not schedule_data['dates'][0]['games']:
            return None
        
        game = schedule_data['dates'][0]['games'][0]
        return GameInfo(
            date=today,
            status=game['status']['detailedState'],
            home_team=game['teams']['home']['team']['name'],
            away_team=game['teams']['away']['team']['name'],
            venue=game['venue']['name'],
            game_time_utc=game['gameDate'],
            home_score=game['teams']['home'].get('score'),
            away_score=game['teams']['away'].get('score')
        )
    
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"データ解析エラー: {e}")
        raise