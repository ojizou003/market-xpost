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

# Google Chromeリポジトリを追加（安定バージョン）
RUN wget -q -O /tmp/google-chrome-stable.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    apt-get update && \
    apt-get install -y /tmp/google-chrome-stable.deb && \
    rm /tmp/google-chrome-stable.deb && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriverをインストール（Chromeバージョンに合わせる）
RUN CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | sed 's/\.[0-9]*$//') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip

# Python依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY x-market-ga.py .

# 実行権限を付与
RUN chmod +x x-market-ga.py

# コマンド
CMD ["python", "x-market-ga.py"]