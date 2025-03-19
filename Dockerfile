FROM selenium/standalone-firefox:4.15.0

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Set proper permissions
RUN chmod +x wait-for-selenium.sh && \
    chown -R seluser:seluser /app

# Environment variables for Render
ENV SE_NODE_PORT=4444
ENV SE_NODE_OVERRIDE_MAX_SESSIONS=true
ENV SE_NODE_MAX_SESSIONS=1

EXPOSE 4444

USER 1200

CMD (./wait-for-selenium.sh && python3 scraperMAP.py) & \
    /opt/bin/entry_point.sh
