# Prompt Poem

Generate a short free-verse poem from a user prompt. The backend uses FastAPI and the OpenAI API, and the frontend is a Vite + React single-page app with Russian and English UI.

## Features
- Prompt-to-poem generation with keyword extraction and LLM fallback handling.
- Simple REST API: `POST /api/poem` and `GET /health`.
- Bilingual UI with example prompts.

## Tech Stack
- Backend: FastAPI, OpenAI SDK, Python 3.10+
- Frontend: React 18, Vite 5

## Prerequisites
- Python 3.10+
- Node.js 18+
- An OpenAI API key

## Setup

### 1) Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend`:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.1
```

Run the API:
```bash
uvicorn main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `/api/poem`. During development, configure a Vite proxy or run the frontend behind a reverse proxy that forwards `/api` to `http://localhost:8000`.

## API

### `POST /api/poem`
Request body:
```json
{
  "prompt": "city after rain, warm light, a window dialogue"
}
```

Response:
```json
{
  "poem": "…",
  "used_words": ["city", "rain", "light"],
  "source": "llm"
}
```

### `GET /health`
Response:
```json
{ "status": "ok" }
```

## Notes
- If the LLM call fails, the backend falls back to a local poem generator.
- The UI includes a language toggle for Russian and English.
