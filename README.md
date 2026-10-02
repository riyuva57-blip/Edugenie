# EduGenie — Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A for academic questions
- simplified concept explanations
- three-question MCQ quizzes
- concise summaries
- personalized beginner-to-advanced learning paths

## Architecture

- **FastAPI** — REST API and server-rendered frontend
- **Google Gemini** — Q&A, quizzes, summaries, learning paths, and optional explanation fallback
- **LaMini-Flan-T5-783M** — local concept explanation model
- **Jinja2 + HTML/CSS/JavaScript** — browser interface
- **Pydantic** — request/response validation

## Requirements

- Python 3.10+
- Google Gemini API key for Gemini-powered features
- Enough disk/RAM for the local LaMini model if `LOCAL_MODEL_ENABLED=true`

## Quick start

### Windows PowerShell

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

API docs are available at http://127.0.0.1:8000/docs

## Local-model option

The project documentation assigns LaMini-Flan-T5 to the explanation module. The application loads it lazily on the first `/explain` request so startup remains fast. The model is downloaded by Hugging Face/Transformers the first time it is needed.

If your machine cannot comfortably run the local model, set:

```env
LOCAL_MODEL_ENABLED=false
```

Then `/explain` uses Gemini instead. This is an implementation fallback, not a change to the documented module contract.

## API examples

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"text":"Which is the largest ocean?"}'

curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain photosynthesis for a beginner."}'

curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"The Pythagorean theorem relates the sides of a right triangle."}'

curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Paste a long educational passage here."}'

curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d '{"text":"SQL","level":"beginner","weeks":6}'
```

## Testing

Run:

```bash
pytest -q
```

The tests validate request validation, JSON cleaning, quiz normalization, and the FastAPI routes without making paid Gemini requests or downloading the local model.

## Security notes

- Never commit `.env` or your API key.
- API keys stay on the server; the browser never receives `GEMINI_API_KEY`.
- The app limits request size to prevent accidentally sending extremely large prompts.
- AI output is treated as untrusted text and is escaped by the browser when inserted into the DOM.
