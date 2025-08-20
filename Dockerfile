FROM python:3.9-bullseye

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies including those needed for Playwright and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    wget \
    git \
    ca-certificates \
    fonts-liberation \
    fonts-unifont \
    fonts-dejavu-core \
    fonts-freefont-ttf \
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
    # Additional packages for browser dependencies
    libgdk-pixbuf-2.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libjpeg62-turbo \
    libwebp6 \
    libenchant-2-2 \
    libicu67 \
    libvpx6 \
    # Dependencies for Pillow
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements first
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright with browser
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir playwright && \
    playwright install chromium --with-deps

# Now copy the rest of your application code
COPY . /code/

EXPOSE 8000