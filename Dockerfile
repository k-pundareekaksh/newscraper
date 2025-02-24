# Use Python 3.12 as base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y wget curl unzip xvfb libnss3 libasound2 fonts-liberation \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libappindicator3-1 \
    libdbusmenu-glib4 libdbusmenu-gtk3-4 libxrandr2 libgbm1 libpango-1.0-0 libatk1.0-0 libcups2 \
    ca-certificates gnupg

# Add Google Chrome’s official repository and install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Verify Chrome installation
RUN google-chrome --version

# Set ChromeDriver version
ENV CHROMEDRIVER_VERSION=114.0.5735.16

# Install ChromeDriver (matching version)
RUN wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
