# Use a minimal Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg libgl1-mesa-glx libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install Python dependencies
RUN pip install --no-cache-dir streamlit selenium chromedriver-autoinstaller

# Copy project files
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
