import discord
from discord.ext import commands, tasks # commands をインポート
from typing import Optional
from datetime import datetime
import logging
import os # Cogロードのために追加
from .api_client import fetch_dodgers_game
from .utils import format_game_info

# ロガーを取得 (basicConfigはserver.pyで行う)
logger = logging.getLogger(__name__)

class DodgersBot(commands.Bot):
    """ドジャースの試合情報を提供するDiscordボット (commands.Botベース)"""

    def __init__(self, *, intents: discord.Intents):
        # コマンドプレフィックスを設定 (例: '!')
        super().__init__(command_prefix='!', intents=intents)
        # Cogをロードするための初期化処理は setup_hook で行う

    async def setup_hook(self) -> None:
        """ボットが内部セットアップを完了した後に呼び出される"""
        logger.info("ボットのセットアップを開始します (setup_hook)...")

        # Cogファイルをロード
        cogs_dir = "src/bot/cogs"
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_name = f"src.bot.cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    logger.info(f"Cog '{cog_name}' をロードしました。")
                except commands.ExtensionError as e:
                    logger.exception(f"Cog '{cog_name}' のロードに失敗しました。", exc_info=e)

        logger.info("ボットのセットアップが完了しました (setup_hook)。")


    async def on_ready(self) -> None:
        """Botが起動し、準備が完了したときに呼び出されるイベントハンドラ"""
        logger.info(f'{self.user} としてログインしました (on_ready)')
        # Cog内のタスクはCog側で開始されるため、ここでのタスク開始は不要

    # on_message は commands.Bot がコマンドを処理するため、通常は不要
    # もしコマンド以外のメッセージにも反応したい場合は、以下のように実装し、
    # 最後に await self.process_commands(message) を呼び出す
    # async def on_message(self, message: discord.Message) -> None:
    #     if message.author == self.user:
    #         return
    #     # 何か特別な処理...
    #     await self.process_commands(message) # コマンド処理を実行

    # handle_dodgers_command は Cog に移動
    # keep_alive タスクも Cog に移動

# start_bot 関数は server.py で直接 Bot インスタンスを作成・実行するため不要

# このファイルが直接実行された場合の処理も不要 (server.pyがエントリーポイント)