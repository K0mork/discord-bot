# ベースイメージとして公式のPythonイメージを使用 (適切なバージョンを選択)
FROM python:3.10-slim

# 環境変数設定 (Pythonのバッファリングを無効化し、ログがすぐに見えるようにする)
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt requirements.txt

# 依存関係をインストール
# --no-cache-dir オプションでキャッシュを使用せず、イメージサイズを削減
# --upgrade pip でpip自体を最新に更新
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションコードを作業ディレクトリにコピー
COPY . .

# アプリケーションがリッスンするポートを公開 (Koyebは$PORT環境変数を参照するため、必須ではないが記述しておく)
# EXPOSE 8000 # Koyebでは$PORTが使われるため、固定ポートの公開は必須ではない

# アプリケーションを実行するコマンド (shell形式を使用し、環境変数 $PORT を展開)
# Koyebは$PORT環境変数を設定するので、それにバインドする
# $PORTが未設定の場合のフォールバックとして8000を使う
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}