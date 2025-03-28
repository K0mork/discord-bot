# ビルドステージ
FROM python:3.10-slim as builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 本番用イメージ
FROM python:3.10-slim
WORKDIR /app

# ユーザー作成 (セキュリティのためroot以外で実行)
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser && \
    chown appuser:appuser /app
USER appuser

# 依存関係をコピー
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# アプリケーションコードをコピー
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser bot.py ./


# アプリケーション実行
CMD ["python", "bot.py"]