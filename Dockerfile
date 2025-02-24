# Use the official Python 3.12 image as the base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y wget curl unzip xvfb libnss3 libasound2 fonts-liberation \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libappindicator3-1 \
    libdbusmenu-glib4 libdbusmenu-gtk3-4 libxrandr2 libgbm1 libpango-1.0-0 libatk1.0-0 libcups2

# Install Google Chrome (specific version)
RUN wget -qO- https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb > /tmp/chrome.deb && \
    apt-get install -y ./tmp/chrome.deb && rm /tmp/chrome.deb

# Verify Chrome installation
RUN google-chrome --version

# Set ChromeDriver version
ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Install ChromeDriver (matching version)
RUN wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Copy the application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
