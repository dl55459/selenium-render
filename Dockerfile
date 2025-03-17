# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub > /etc/apt/keyrings/google-chrome-key.pub \
    && echo "deb [signed-by=/etc/apt/keyrings/google-chrome-key.pub] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable=114.0.5735.198-1

# Install ChromeDriver for Chrome 114
RUN wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver \
    && mv -f chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["python", "scraperMAP.py"]
