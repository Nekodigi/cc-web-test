FROM python:3.11-slim

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションをコピー
COPY app.py .

# Streamlit設定
RUN mkdir -p ~/.streamlit
RUN echo "[server]\nheadless = true\nport = 8080\nenableXsrfProtection = false\n" > ~/.streamlit/config.toml

# ポート公開
EXPOSE 8080

# アプリケーション実行
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
