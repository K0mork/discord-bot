import uvicorn
from fastapi import FastAPI
import asyncio
import threading
import os
from dotenv import load_dotenv

# bot.py からボット起動関数をインポート (後で bot.py を修正します)
from bot import start_bot, client as discord_client

# .envファイルから環境変数を読み込む (bot.py と重複するが、サーバー単体起動のためにも記述)
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# FastAPIアプリケーションの初期化
app = FastAPI()

# Discordボットを別スレッドで実行するための関数
def run_bot_in_thread():
    if TOKEN:
        # 新しいイベントループを作成して設定
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # start_bot を実行
        loop.run_until_complete(start_bot(TOKEN))
    else:
        print("エラー: DISCORD_BOT_TOKENが設定されていません。")

@app.on_event("startup")
async def startup_event():
    """
    FastAPIサーバー起動時にDiscordボットを別スレッドで起動する
    """
    print("FastAPIサーバーが起動しました。")
    # スレッドを作成してボットを実行
    bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
    bot_thread.start()
    print("Discordボットのスレッドを開始しました。")

@app.get("/health")
async def health_check():
    """
    ヘルスチェック用エンドポイント
    Koyebなどのプラットフォームがアプリケーションの生存確認に使用
    """
    # Discordクライアントが接続されているかを確認 (より詳細なチェックも可能)
    if discord_client and discord_client.is_ready():
        return {"status": "ok", "discord_bot": "connected"}
    else:
        # ボットがまだ準備中か、接続に失敗している可能性
        return {"status": "ok", "discord_bot": "initializing_or_disconnected"}

# Uvicornサーバーを直接実行する場合 (ローカルテスト用)
if __name__ == "__main__":
    # ポートは環境変数から取得するか、デフォルトで8000を使用
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)