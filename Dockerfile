# Use official Selenium Chrome image
FROM selenium/standalone-chrome:4.15.0-20231127

# Switch to root for package installation
USER root

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Add health check
HEALTHCHECK --interval=5s --timeout=30s --retries=3 \
    CMD curl --fail http://localhost:4444/wd/hub/status || exit 1

# Switch back to selenium user
USER 1200

# Start Selenium server and run script
CMD (./wait-for-selenium.sh && python3 scraperMAP.py) &
    /opt/bin/entry_point.sh
