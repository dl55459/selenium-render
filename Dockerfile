# Use the official Selenium Chrome standalone image
FROM selenium/standalone-chrome:4.11.0-20230801

# Switch to root user to install Python and dependencies
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Switch back to the seluser for security (optional, adjust as needed)
USER 1200

# Run the application
CMD ["python3", "scraperMAP.py"]
