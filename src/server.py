import uvicorn
from fastapi import FastAPI
import asyncio
import threading
import logging
from src.config import config
from src.bot.core import start_bot, DodgersBot

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Dodgers Discord Bot API",
    description="ドジャースの試合情報を提供するDiscordボットの管理API",
    version="1.0.0"
)

# Discordボットクライアントのインスタンス
bot_client: Optional[DodgersBot] = None

def run_bot_in_thread() -> None:
    """Discordボットを別スレッドで実行する"""
    global bot_client
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 設定からトークンを取得
        token = config.DISCORD_BOT_TOKEN
        if not token:
            logger.error("DISCORD_BOT_TOKENが設定されていません")
            return
            
        bot_client = DodgersBot(intents=discord.Intents.default())
        loop.run_until_complete(start_bot(token))
    except Exception as e:
        logger.error(f"ボットの実行中にエラーが発生しました: {e}")

@app.on_event("startup")
async def startup_event() -> None:
    """FastAPIサーバー起動時にDiscordボットを起動する"""
    logger.info("FastAPIサーバーを起動します")
    
    # ボットを別スレッドで起動
    bot_thread = threading.Thread(
        target=run_bot_in_thread,
        daemon=True,
        name="DiscordBotThread"
    )
    bot_thread.start()
    logger.info("Discordボットのスレッドを開始しました")

@app.get("/health")
async def health_check() -> dict:
    """ヘルスチェックエンドポイント
    
    Returns:
        dict: アプリケーションの状態情報
    """
    status = {
        "status": "ok",
        "api": "running",
        "discord_bot": "disconnected"
    }
    
    if bot_client and bot_client.is_ready():
        status["discord_bot"] = "connected"
    
    return status

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        log_level="info"
    )