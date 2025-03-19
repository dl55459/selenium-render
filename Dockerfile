FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    MOZ_HEADLESS=1

# Install essential packages with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    firefox-esr \
    xvfb \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Install compatible GeckoDriver (0.32.0 for Firefox ESR)
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -xzf geckodriver-*.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-*.tar.gz

WORKDIR /app

# Create non-root user to avoid pip warnings
RUN useradd -m render && chown -R render:render /app
USER render

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

CMD xvfb-run python scraperMAP.py
