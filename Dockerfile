FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    MOZ_HEADLESS=1 \
    MOZ_ENABLE_WAYLAND=0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    firefox-esr \
    xvfb \
    xauth \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxt6 \
    libasound2 \
    libnss3 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libxss1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

# Install specific compatible GeckoDriver version
RUN GECKODRIVER_VERSION=0.34.0 && \
    wget https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -xzf geckodriver-*.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-*.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24 -ac" python scraperMAP.py
