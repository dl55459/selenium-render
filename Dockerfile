# Use official Selenium Firefox image
FROM selenium/standalone-firefox:4.15.0

# Switch to root for package installation
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for downloads and set permissions
RUN mkdir -p /home/seluser/downloads && \
    chown -R seluser:seluser /app /home/seluser/downloads

# Health check for Render
HEALTHCHECK --interval=5s --timeout=30s --retries=3 \
    CMD curl --fail http://localhost:4444/wd/hub/status || exit 1

# Switch back to selenium user
USER 1200

# Start script
CMD (./wait-for-selenium.sh && python3 scraperMAP.py) & \
    /opt/bin/entry_point.sh
