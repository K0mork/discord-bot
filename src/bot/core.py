import discord
from typing import Optional
from datetime import datetime
import logging  # logging モジュールをインポート
from .api_client import fetch_dodgers_game
from .utils import format_game_info

# ロギング設定 (基本的な設定)
# src/server.py で設定済みであれば、重複を避けることも可能
# ただし、このファイル単体で実行する場合も考慮して設定しておく
logging.basicConfig(
    level=logging.INFO, # DEBUGからINFOに戻す
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__) # ロガーを取得

class DodgersBot(discord.Client):
    """ドジャースの試合情報を提供するDiscordボット"""

    async def on_ready(self) -> None:
        """Botが起動したときに呼び出されるイベントハンドラ"""
        logger.info(f'{self.user} としてログインしました')

    async def on_message(self, message: discord.Message) -> None:
        """メッセージを受信したときに呼び出されるイベントハンドラ"""
        # 自分自身のメッセージは無視
        if message.author == self.user:
            return

        # logger.debug(f"メッセージ受信: author='{message.author}', content='{message.content}'") # DEBUGログ削除

        # コマンドプレフィックスで始まるかチェック
        if message.content.startswith('!dodgers'):
            logger.info(f"!dodgers コマンドを検出: author='{message.author}'") # コマンド検出ログ
            await self.handle_dodgers_command(message)

    async def handle_dodgers_command(self, message: discord.Message) -> None:
        """!dodgersコマンドを処理する"""
        logger.info(f"handle_dodgers_command を実行: author='{message.author}'") # ハンドラ実行ログ
        try:
            logger.info("ドジャースの試合情報を取得開始...") # API呼び出し前ログ
            game_info = await fetch_dodgers_game()
            logger.info(f"試合情報取得完了: {game_info}") # API呼び出し後ログ

            if game_info:
                reply = format_game_info(game_info)
                logger.info(f"返信メッセージ生成: '{reply}'") # 返信生成ログ
                await message.channel.send(reply)
                logger.info(f"返信を送信しました: channel='{message.channel}'") # 返信送信後ログ
            else:
                logger.info("今日の試合情報が見つかりませんでした。") # 試合なしログ
                await message.channel.send("今日のドジャースの試合情報が見つかりませんでした。")

        except Exception as e:
            # スタックトレースを含むエラーログを出力
            logger.exception(f"!dodgers コマンド処理中にエラーが発生しました: author='{message.author}'")
            try:
                await message.channel.send("試合情報の取得中にエラーが発生しました。")
            except discord.HTTPException:
                logger.error("エラーメッセージの送信に失敗しました。")

async def start_bot(token: str) -> None:
    """Discord Botを起動する"""
    # src/server.py で Intents が設定されているため、ここでは不要
    # intents = discord.Intents.default()
    # intents.message_content = True
    # bot = DodgersBot(intents=intents)
    # logger.info("DodgersBot インスタンスを作成しました。") # インスタンス作成ログは server.py 側で

    # この関数は server.py から呼び出される想定のため、
    # botインスタンスの作成と起動は server.py に任せるのが自然
    # もしこのファイル単体で起動するケースがあるなら、以下のコードが必要
    # intents = discord.Intents.default()
    # intents.message_content = True
    # bot = DodgersBot(intents=intents)
    # try:
    #     logger.info("ボットを起動します...")
    #     await bot.start(token)
    # except Exception as e:
    #     logger.exception("ボットの起動中にエラーが発生しました")
    # finally:
    #     if bot and not bot.is_closed():
    #         await bot.close()
    #         logger.info("ボットクライアントをクローズしました。")
    pass # server.py で起動処理を行うため、ここでは何もしない

# このファイルが直接実行された場合の処理 (デバッグ用など)
# if __name__ == '__main__':
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()
#     token = os.getenv("DISCORD_BOT_TOKEN")
#     if token:
#         asyncio.run(start_bot(token)) # start_bot の実装を戻す必要あり
#     else:
#         logger.error("DISCORD_BOT_TOKEN が .env ファイルに見つかりません。")