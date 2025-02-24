# Install dependencies
RUN apt-get update && apt-get install -y wget curl unzip xvfb libnss3 libasound2 fonts-liberation \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libappindicator3-1 \
    libdbusmenu-glib4 libdbusmenu-gtk3-4 libxrandr2 libgbm1 libpango-1.0-0 libatk1.0-0 libcups2

# Install Google Chrome
RUN wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > /tmp/chrome.deb && \
    apt-get install -y ./tmp/chrome.deb && rm /tmp/chrome.deb

# Verify Chrome installation
RUN google-chrome --version

# Set ChromeDriver Version (Check official site for latest version)
ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip
