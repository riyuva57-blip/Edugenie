from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import LearningPathRequest, QuizResponse, TextRequest, TextResponse
from summary_module import summarize_text
from config import get_settings

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()

app = FastAPI(
    title="EduGenie",
    description="Gemini-powered educational assistant with a local LaMini explanation module.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "explanation_backend": settings.explanation_backend,
        "local_model_enabled": settings.local_model_enabled,
    }


@app.post("/qa", response_model=TextResponse)
async def qa(request: TextRequest):
    return TextResponse(result=answer_question(request.text))


@app.post("/explain", response_model=TextResponse)
async def explain(request: TextRequest):
    return TextResponse(result=explain_concept(request.text))


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    return QuizResponse(questions=generate_quiz(request.text))


@app.post("/summarize", response_model=TextResponse)
async def summarize(request: TextRequest):
    return TextResponse(result=summarize_text(request.text))


@app.post("/learn/recommendations", response_model=TextResponse)
async def recommendations(request: LearningPathRequest):
    return TextResponse(
        result=get_learning_recommendations(request.text, request.level, request.weeks)
    )
