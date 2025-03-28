import uvicorn
from fastapi import FastAPI
import asyncio
import threading
import logging
import discord  # discordをインポート
from typing import Optional  # Optionalをインポート
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

        intents = discord.Intents.default() # Intentsを定義
        # 必要に応じてIntentsを有効化
        # intents.message_content = True
        # intents.members = True

        bot_client = DodgersBot(intents=intents) # intentsを渡す
        # start_bot関数がトークンとボットインスタンスを受け取るように修正が必要な場合がある
        # loop.run_until_complete(start_bot(token, bot_client)) # start_botの実装に依存
        # もしstart_botがトークンのみを受け取るなら以下
        loop.run_until_complete(bot_client.start(token)) # bot_client.startを使用
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

@app.get("/") # エンドポイントを / に変更
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
    # config.PORTではなく、直接8000番ポートを指定するか、
    # Koyebの環境変数 PORT を利用する
    port = config.PORT if config.PORT else 8000 # 環境変数PORTがあればそれを使う、なければ8000
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port, # ポートを指定
        log_level="info"
    )