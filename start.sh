#!/bin/bash

# Download and extract Google Chrome binary (No sudo required)
mkdir -p /opt/google/chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > /opt/google/chrome/google-chrome.deb

# Install ChromeDriver (Hardcoded latest version to avoid 404 errors)
CHROMEDRIVER_VERSION=124.0.6367.0
wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/

# Run Streamlit app on Render (use port 10000 to avoid Render conflicts)
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
