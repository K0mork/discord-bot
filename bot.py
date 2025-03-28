import asyncio
import logging
import os
from src.config import config  # 設定を読み込む
from src.bot.core import start_bot

# ロギング設定 (src/server.pyと同様)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """ボットを起動するメイン関数"""
    token = config.DISCORD_BOT_TOKEN
    if not token:
        logger.error("DISCORD_BOT_TOKENが設定されていません。環境変数を確認してください。")
        return

    logger.info("Discordボットを起動します...")
    # start_bot内でDodgersBotインスタンスが作成され、起動される
    await start_bot(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("ボットを手動で停止しました。")
    except Exception as e:
        logger.error(f"ボットの実行中に予期せぬエラーが発生しました: {e}", exc_info=True)