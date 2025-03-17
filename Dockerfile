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
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1) \
    && wget -N https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION \
    && CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE_$CHROME_MAJOR_VERSION) \
    && wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver \
    && mv -f chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip LATEST_RELEASE_$CHROME_MAJOR_VERSION

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["python", "app.py"]
