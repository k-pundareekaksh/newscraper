# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chrome & ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    google-chrome-stable

# Download & set up ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Copy app files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Start the Streamlit app
CMD streamlit run app.py --server.port 8501 --server.address 0.0.0.0
