FROM python:3.12-slim

WORKDIR /app

COPY rag_backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install required system dependencies manually
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-xcb1 \
    libxcb1 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium browser only
RUN playwright install chromium

COPY rag_backend/ .
COPY scraper_service/ ./scraper_service/

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
