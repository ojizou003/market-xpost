# Python 3.11-slimベース
FROM python:3.11-slim

# 環境変数設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 作業ディレクトリ
WORKDIR /app

# Chromeをインストールするための依存関係
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    python3 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Google Chromeリポジトリを追加（最新の方法）
RUN wget -q -O /tmp/google-chrome-stable.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    apt-get update && \
    apt-get install -y /tmp/google-chrome-stable.deb && \
    rm /tmp/google-chrome-stable.deb && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriverをインストール（安定した方法）
RUN LATEST_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_stable") && \
    wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${LATEST_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Python依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY x-market-ga.py .

# 実行権限を付与
RUN chmod +x x-market-ga.py

# コマンド
CMD ["python", "x-market-ga.py"]