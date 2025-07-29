FROM python:3.9-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies including those needed for Playwright
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    wget \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    # Additional dependencies for Playwright
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements first
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright with browser
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install playwright && \
    playwright install chromium && \
    playwright install-deps chromium

# Now copy the rest of your application code
COPY . /code/

EXPOSE 8000