FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99

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
    && rm -rf /var/lib/apt/lists/*

RUN GECKODRIVER_VERSION=0.33.0 && \
    wget https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver*.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver*.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "rm -f /tmp/.X99-lock && Xvfb $DISPLAY -screen 0 1920x1080x24 -ac +extension GLX +render -noreset & python scraperMAP.py"
