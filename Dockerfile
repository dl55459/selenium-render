FROM selenium/standalone-firefox:4.15.0

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files with proper permissions
COPY . .
RUN chmod +x wait-for-selenium.sh && \
    chown -R seluser:seluser /app

# Configure Render-specific settings
ENV SE_NODE_PORT=4444
ENV SE_NODE_OVERRIDE_MAX_SESSIONS=true
ENV SE_NODE_MAX_SESSIONS=1

# Expose required ports
EXPOSE 4444 7900

USER 1200

CMD (./wait-for-selenium.sh && python3 scraperMAP.py) & \
    /opt/bin/entry_point.sh
