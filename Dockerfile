FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MOZ_HEADLESS=1
ENV DISPLAY=:99

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    firefox-esr \
    xvfb \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxt6 \
    fonts-liberation \
    libasound2 \
    libnss3 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Install specific GeckoDriver version (match Firefox ESR version)
RUN GECKODRIVER_VERSION=0.33.0 && \
    wget https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver*.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver*.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start Xvfb and run script
CMD xvfb-run --server-args="-screen 0 1024x768x24 -ac" python scraperMAP.py
