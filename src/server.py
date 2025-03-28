import uvicorn
from fastapi import FastAPI
import asyncio
import threading
import logging
import discord
from typing import Optional
from src.config import config
# start_bot は不要になるため削除 (DodgersBotは必要)
from src.bot.core import DodgersBot

# ロギング設定 (レベルをDEBUGに変更)
logging.basicConfig(
    level=logging.DEBUG, # INFOからDEBUGに変更
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

async def run_bot_async(token: str) -> None:
    """Discordボットを非同期で実行するコルーチン"""
    global bot_client
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        bot_client = DodgersBot(intents=intents)
        logger.info("Discordボットクライアントを作成しました。")
        await bot_client.start(token)
    except Exception as e:
        logger.exception("Discordボットの実行中にエラーが発生しました") # logger.exceptionに変更
    finally:
        if bot_client and not bot_client.is_closed():
            await bot_client.close()
            logger.info("Discordボットクライアントをクローズしました。")

def run_bot_in_thread() -> None:
    """Discordボットを別スレッドで実行する"""
    logger.info("Discordボットスレッドを開始します。")
    token = config.DISCORD_BOT_TOKEN
    if not token:
        logger.error("DISCORD_BOT_TOKENが設定されていません。ボットを起動できません。")
        return

    # asyncio.run() を使用して新しいイベントループでボットを実行
    try:
        asyncio.run(run_bot_async(token))
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt を検知しました。ボットスレッドを終了します。")
    except Exception as e:
        logger.exception("ボットスレッドの実行中に予期せぬエラーが発生しました")

@app.on_event("startup")
async def startup_event() -> None:
    """FastAPIサーバー起動時にDiscordボットを起動する"""
    logger.info("FastAPIサーバーを起動します")

    # ボットを別スレッドで起動
    bot_thread = threading.Thread(
        target=run_bot_in_thread,
        daemon=True, # デーモンスレッドに設定
        name="DiscordBotThread"
    )
    bot_thread.start()
    logger.info("Discordボットのスレッドを開始しました (startup_event)") # ログを明確化

@app.get("/")
async def health_check() -> dict:
    """ヘルスチェックエンドポイント"""
    status = {
        "status": "ok",
        "api": "running",
        "discord_bot": "disconnected"
    }
    # bot_client が None でないこと、かつ is_ready() であることを確認
    if bot_client and bot_client.is_ready():
        status["discord_bot"] = "connected"
        logger.debug("Health Check: Bot is connected.")
    else:
        logger.debug(f"Health Check: Bot status - bot_client is None: {bot_client is None}, is_ready: {bot_client.is_ready() if bot_client else 'N/A'}")

    return status

if __name__ == "__main__":
    port = config.PORT if config.PORT else 8000
    logger.info(f"Uvicornサーバーをポート {port} で起動します...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info" # uvicorn自体のログレベルはinfoのままにする場合が多い
    )