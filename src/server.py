import uvicorn
from fastapi import FastAPI
import asyncio
import threading
import logging
import discord
from typing import Optional
from src.config import config
from src.bot.core import DodgersBot

# ロギング設定 (レベルをINFOに戻す)
logging.basicConfig(
    level=logging.INFO, # DEBUGからINFOに戻す
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# discordライブラリのロガーレベル設定を削除 (basicConfigに従う)
# discord_logger = logging.getLogger('discord')
# discord_logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__) # このモジュールのロガー

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
    logger.info("run_bot_async: コルーチン開始")
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        # logger.debug(f"run_bot_async: Intents設定完了 - message_content={intents.message_content}") # DEBUGログ削除
        bot_client = DodgersBot(intents=intents)
        logger.info("run_bot_async: Discordボットクライアントを作成しました。")
        logger.info("run_bot_async: bot.start(token) を呼び出します...")
        await bot_client.start(token)
        logger.info("run_bot_async: bot.start(token) が完了しました (ボットが停止しました)。")
    except discord.LoginFailure:
        logger.exception("run_bot_async: Discordへのログインに失敗しました。トークンが不正な可能性があります。")
    except discord.PrivilegedIntentsRequired:
        logger.exception("run_bot_async: Privileged Intents (message_contentなど) が有効になっていません。Discord Developer Portalを確認してください。")
    except Exception as e:
        logger.exception("run_bot_async: Discordボットの実行中に予期せぬエラーが発生しました")
    finally:
        logger.info("run_bot_async: finallyブロックに入りました。")
        if bot_client and not bot_client.is_closed():
            logger.info("run_bot_async: bot.close() を呼び出します...")
            await bot_client.close()
            logger.info("run_bot_async: Discordボットクライアントをクローズしました。")
        else:
            logger.info("run_bot_async: ボットクライアントが存在しないか、既にクローズされています。")

def run_bot_in_thread() -> None:
    """Discordボットを別スレッドで実行する"""
    logger.info("Discordボットスレッドを開始します。")
    token = config.DISCORD_BOT_TOKEN
    if not token:
        logger.error("DISCORD_BOT_TOKENが設定されていません。ボットを起動できません。")
        return

    logger.info("run_bot_in_thread: asyncio.run(run_bot_async(token)) を呼び出します...")
    try:
        asyncio.run(run_bot_async(token))
        logger.info("run_bot_in_thread: asyncio.run() が正常に完了しました。")
    except KeyboardInterrupt:
        logger.info("run_bot_in_thread: KeyboardInterrupt を検知しました。ボットスレッドを終了します。")
    except Exception as e:
        logger.exception("run_bot_in_thread: ボットスレッドの実行中に予期せぬエラーが発生しました")
    finally:
        logger.info("run_bot_in_thread: スレッドの処理が終了します。")


@app.on_event("startup")
async def startup_event() -> None:
    """FastAPIサーバー起動時にDiscordボットを起動する"""
    logger.info("FastAPIサーバーを起動します (startup_event)")

    # ボットを別スレッドで起動
    bot_thread = threading.Thread(
        target=run_bot_in_thread,
        daemon=True,
        name="DiscordBotThread"
    )
    bot_thread.start()
    logger.info("Discordボットのスレッドを開始しました (startup_event)")

@app.get("/")
async def health_check() -> dict:
    """ヘルスチェックエンドポイント"""
    status = {
        "status": "ok",
        "api": "running",
        "discord_bot": "disconnected"
    }
    if bot_client and bot_client.is_ready():
        status["discord_bot"] = "connected"
        # logger.debug("Health Check: Bot is connected.") # DEBUGログ削除
    # else: # DEBUGログ削除
        # logger.debug(f"Health Check: Bot status - bot_client is None: {bot_client is None}, is_ready: {bot_client.is_ready() if bot_client else 'N/A'}")

    return status

if __name__ == "__main__":
    port = config.PORT if config.PORT else 8000
    logger.info(f"Uvicornサーバーをポート {port} で起動します...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )