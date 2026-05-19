FROM python:3.12-slim

WORKDIR /app

COPY rag_backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY rag_backend/ .
COPY scraper_service/ ./scraper_service/

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
