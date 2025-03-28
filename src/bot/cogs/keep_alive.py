import discord
from discord.ext import commands, tasks
import logging

logger = logging.getLogger(__name__)

class KeepAliveCog(commands.Cog):
    """Koyebのスリープを防ぐための定期実行タスクを管理するCog"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.keep_alive.add_exception_type(discord.DiscordException)
        logger.info("KeepAliveCog が初期化されました。")
        # Cogロード時にタスクを開始するのではなく、on_ready後に開始するようにする
        # self.keep_alive.start() # ここでは開始しない

    def cog_unload(self):
        """Cogがアンロードされるときにタスクをキャンセルする"""
        self.keep_alive.cancel()
        logger.info("KeepAliveCog がアンロードされ、keep_alive タスクがキャンセルされました。")

    @tasks.loop(minutes=30)
    async def keep_alive(self):
        """Koyebのスリープを防ぐための定期実行タスク"""
        try:
            # 軽量なAPIコールを実行 (例: ボット自身の情報を取得)
            if self.bot.is_ready(): # ボットが準備完了しているか確認
                user = await self.bot.fetch_user(self.bot.user.id)
                logger.info(f"Keep-alive: Fetched user info for {user.name}")
            else:
                logger.warning("Keep-alive: Bot is not ready yet, skipping API call.")
        except Exception as e:
            logger.error(f"Keep-alive タスク中にエラーが発生しました: {e}", exc_info=True)

    @keep_alive.before_loop
    async def before_keep_alive(self):
        """keep_aliveループが開始される前に実行される"""
        logger.info("Keep-alive: Waiting until bot is ready...")
        await self.bot.wait_until_ready()
        logger.info("Keep-alive: Bot is ready, starting loop.")

    @commands.Cog.listener()
    async def on_ready(self):
        """ボットの準備完了時にタスクを開始する"""
        if not self.keep_alive.is_running():
            self.keep_alive.start()
            logger.info("KeepAliveCog: keep_alive タスクを開始しました (on_ready)。")


async def setup(bot: commands.Bot):
    """Cogをボットに登録するためのセットアップ関数"""
    await bot.add_cog(KeepAliveCog(bot))
    logger.info("KeepAliveCog がボットに登録されました。")