import sys
import os
import tempfile

# Add parent directory to Python path
sys.path.append(os.path.abspath(".."))

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from rag import ChatPDF
from scraper_service.scraper import ScrapingAssistant

app = FastAPI()

# -----------------------------------
# Initialize RAG Assistant
# -----------------------------------
chat_pdf = ChatPDF()


# -----------------------------------
# Request Models
# -----------------------------------
class QuestionRequest(BaseModel):
    question: str


class ScrapeRequest(BaseModel):
    url: str


# -----------------------------------
# Health Check API
# -----------------------------------
@app.get("/")
def home():
    return {
        "message": "RAG API Running"
    }


# -----------------------------------
# Upload PDF API
# -----------------------------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(await file.read())
        temp_path = tf.name

    # Ingest PDF into vector DB
    chat_pdf.ingest(temp_path)

    # Delete temp file
    os.remove(temp_path)

    return {
        "status": "success",
        "filename": file.filename
    }


# -----------------------------------
# Ask Question API
# -----------------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    response = chat_pdf.ask(request.question)

    return {
        "question": request.question,
        "answer": response
    }


# -----------------------------------
# Website Scraping API
# -----------------------------------
@app.post("/scrape")
def scrape_website(request: ScrapeRequest):

    scraper = ScrapingAssistant(
        root_url=request.url,
        max_pages=1,
        max_depth=1,
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",
        strategy="text",
    )

    scraper.run()

    return {
        "status": "success",
        "url": request.url,
        "pages_scraped": scraper.pages_scraped
    }