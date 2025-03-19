FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

# Install system dependencies with xauth
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    firefox-esr \
    xvfb \
    xauth \
    xfonts-base \
    xfonts-75dpi \
    x11-xkb-utils \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxt6 \
    && rm -rf /var/lib/apt/lists/*

# Install specific GeckoDriver version
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
CMD sh -c "rm -f /tmp/.X99-lock && Xvfb $DISPLAY -screen 0 1024x768x24 -ac +extension GLX +render -noreset & python scraperMAP.py"
