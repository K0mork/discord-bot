import os
from typing import Optional
from dotenv import load_dotenv

class Config:
    """アプリケーション設定を管理するクラス"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """環境変数を読み込む"""
        load_dotenv()
        
        # Discord Bot設定
        self.DISCORD_BOT_TOKEN: Optional[str] = os.getenv('DISCORD_BOT_TOKEN')
        if not self.DISCORD_BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKENが設定されていません")
        
        # サーバー設定
        self.PORT: int = int(os.getenv('PORT', '8000'))
        
        # MLB API設定
        self.MLB_API_ENDPOINT: str = os.getenv(
            'MLB_API_ENDPOINT',
            'https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&date={date}'
        )
    
    @property
    def is_valid(self) -> bool:
        """設定が有効かどうかを確認する"""
        return all([
            self.DISCORD_BOT_TOKEN is not None,
            isinstance(self.PORT, int),
            self.MLB_API_ENDPOINT is not None
        ])

# 設定インスタンスをグローバルに公開
config = Config()