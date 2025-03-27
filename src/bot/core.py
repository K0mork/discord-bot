import discord
from typing import Optional
from datetime import datetime
from .api_client import fetch_dodgers_game
from .utils import format_game_info

class DodgersBot(discord.Client):
    """ドジャースの試合情報を提供するDiscordボット"""
    
    async def on_ready(self) -> None:
        """Botが起動したときに呼び出されるイベントハンドラ"""
        print(f'{self.user} としてログインしました')
    
    async def on_message(self, message: discord.Message) -> None:
        """メッセージを受信したときに呼び出されるイベントハンドラ"""
        if message.author == self.user:
            return
        
        if message.content.startswith('!dodgers'):
            await self.handle_dodgers_command(message)
    
    async def handle_dodgers_command(self, message: discord.Message) -> None:
        """!dodgersコマンドを処理する"""
        try:
            game_info = await fetch_dodgers_game()
            if game_info:
                reply = format_game_info(game_info)
                await message.channel.send(reply)
            else:
                await message.channel.send("今日のドジャースの試合情報が見つかりませんでした。")
        
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            await message.channel.send("試合情報の取得中にエラーが発生しました。")

async def start_bot(token: str) -> None:
    """Discord Botを起動する"""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DodgersBot(intents=intents)
    
    try:
        await bot.start(token)
    except Exception as e:
        print(f"ボットの起動中にエラーが発生しました: {e}")
    finally:
        await bot.close()
        print("ボットクライアントをクローズしました。")