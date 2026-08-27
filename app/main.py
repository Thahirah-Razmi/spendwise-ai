from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_database
from app.models import ChatRequest
from app.ai import ai


app = FastAPI(
    title="SpendWise AI",
    description="Local AI expense management SaaS",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_database()


@app.post("/api/chat")
def chat(request: ChatRequest):

    result = ai.chat(request.message)

    return result


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "model": "Qwen/Qwen3-0.6B",
        "provider": "local"
    }


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/info")
def info():
    return {
        "application": "SpendWise AI",
        "model": "Qwen/Qwen3-0.6B",
        "provider": "Hugging Face Transformers",
        "inference": "local",
        "api_key_required": False,
        "tool_calling": True
    }