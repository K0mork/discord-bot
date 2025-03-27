import discord
import os
import requests
import datetime
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Discordクライアントの初期化
intents = discord.Intents.default()
intents.message_content = True # メッセージ内容の取得を有効にする
client = discord.Client(intents=intents)

# MLB Stats APIのエンドポイント (ドジャースのチームIDは119)
MLB_API_ENDPOINT = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&date={date}"

@client.event
async def on_ready():
    """Botが起動したときに呼び出されるイベントハンドラ"""
    print(f'{client.user} としてログインしました')

@client.event
async def on_message(message):
    """メッセージを受信したときに呼び出されるイベントハンドラ"""
    # Bot自身のメッセージは無視する
    if message.author == client.user:
        return

    # '!dodgers' コマンドが送信された場合
    if message.content.startswith('!dodgers'):
        try:
            # 今日の日付を取得 (YYYY-MM-DD形式)
            today = datetime.date.today().strftime('%Y-%m-%d')
            api_url = MLB_API_ENDPOINT.format(date=today)

            # MLB Stats APIから試合情報を取得
            response = requests.get(api_url)
            response.raise_for_status() # エラーがあれば例外を発生させる
            schedule_data = response.json()

            if not schedule_data['dates'] or not schedule_data['dates'][0]['games']:
                await message.channel.send(f"{today} にドジャースの試合はありません。")
                return

            # その日の最初の試合を取得 (ダブルヘッダーの場合、最初の試合のみ表示)
            game = schedule_data['dates'][0]['games'][0]
            game_status = game['status']['detailedState']
            home_team = game['teams']['home']['team']['name']
            away_team = game['teams']['away']['team']['name']
            venue = game['venue']['name']

            # 試合開始時刻 (UTC) を取得し、日本時間 (JST) に変換
            game_time_utc_str = game['gameDate']
            # ISO 8601形式の文字列をdatetimeオブジェクトに変換
            game_time_utc = datetime.datetime.fromisoformat(game_time_utc_str.replace('Z', '+00:00'))
            game_time_jst = game_time_utc.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
            game_time_jst_str = game_time_jst.strftime('%Y年%m月%d日 %H:%M')


            # スコア情報 (試合中の場合)
            score_info = ""
            # 'In Progress', 'Final', 'Game Over' などの状態を考慮
            if game_status not in ("Scheduled", "Pre-Game", "Warmup", "Preview"):
                 try:
                     home_score = game['teams']['home'].get('score', '?') # スコアがない場合は '?'
                     away_score = game['teams']['away'].get('score', '?') # スコアがない場合は '?'
                     score_info = f" ({away_team} {away_score} - {home_score} {home_team})"
                 except KeyError:
                     # スコア情報がない場合（試合開始直後など）
                     pass


            # メッセージを作成して送信
            reply_message = (
                f"⚾ **今日のドジャースの試合 ({today})** ⚾\n"
                f"対戦: {away_team} @ {home_team}\n"
                f"球場: {venue}\n"
                f"状態: {game_status}{score_info}\n"
                f"開始時刻 (日本時間): {game_time_jst_str}"
            )
            await message.channel.send(reply_message)

        except requests.exceptions.RequestException as e:
            print(f"APIリクエストエラー: {e}")
            await message.channel.send("試合情報の取得中にエラーが発生しました。MLB Stats APIにアクセスできない可能性があります。")
        except Exception as e:
            print(f"予期せぬエラー: {e}")
            await message.channel.send("処理中に予期せぬエラーが発生しました。")

# サーバーから呼び出されるボット起動関数
async def start_bot(token: str):
    """Discord Botを起動する"""
    try:
        await client.start(token)
    except Exception as e:
        print(f"ボットの起動中にエラーが発生しました: {e}")
    finally:
        # ボットが停止した場合のクリーンアップ処理など (必要であれば)
        await client.close()
        print("ボットクライアントをクローズしました。")

# スクリプトとして直接実行された場合の処理は削除 (server.pyから起動するため)
# if __name__ == "__main__":
#     if TOKEN:
#         print("Botを直接起動します...") # server.pyから起動するのが基本
#         client.run(TOKEN)
#     else:
#         print("エラー: DISCORD_BOT_TOKENが設定されていません。")