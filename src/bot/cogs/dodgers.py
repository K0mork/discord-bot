import discord
from discord.ext import commands
import logging
from ..api_client import fetch_dodgers_game
from ..utils import format_game_info

logger = logging.getLogger(__name__)

class DodgersCommandsCog(commands.Cog):
    """ドジャース関連のコマンドを管理するCog"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("DodgersCommandsCog が初期化されました。")

    @commands.command(name='dodgers', help='今日のドジャースの試合情報を表示します。')
    async def dodgers_game(self, ctx: commands.Context):
        """!dodgers コマンドの処理"""
        logger.info(f"!dodgers コマンドを受信: author='{ctx.author}'")
        try:
            logger.info("ドジャースの試合情報を取得開始...")
            game_info = await fetch_dodgers_game()
            logger.info(f"試合情報取得完了: {game_info}")

            if game_info:
                reply = format_game_info(game_info)
                logger.info(f"返信メッセージ生成: '{reply}'")
                await ctx.send(reply)
                logger.info(f"返信を送信しました: channel='{ctx.channel}'")
            else:
                logger.info("今日の試合情報が見つかりませんでした。")
                await ctx.send("今日のドジャースの試合情報が見つかりませんでした。")

        except Exception as e:
            logger.exception(f"!dodgers コマンド処理中にエラーが発生しました: author='{ctx.author}'")
            try:
                await ctx.send("試合情報の取得中にエラーが発生しました。")
            except discord.HTTPException:
                logger.error("エラーメッセージの送信に失敗しました。")

async def setup(bot: commands.Bot):
    """Cogをボットに登録するためのセットアップ関数"""
    await bot.add_cog(DodgersCommandsCog(bot))
    logger.info("DodgersCommandsCog がボットに登録されました。")