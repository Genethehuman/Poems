# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: FastAPI service in `backend/main.py`, Python dependencies in `backend/requirements.txt`.
- `frontend/`: Vite + React app (`frontend/src/` for UI code, `frontend/index.html` entry).
- `frontend/src/`: `App.jsx`, `main.jsx`, and `styles.css` for UI, entry, and styling.
- No test directories are present in the current repository.

## Build, Test, and Development Commands
- Backend setup:
  - `cd backend && python -m venv venv && source venv/bin/activate`
  - `pip install -r requirements.txt`
- Run backend (dev):
  - `uvicorn main:app --reload --port 8000`
- Frontend setup:
  - `cd frontend && npm install`
- Run frontend (dev):
  - `npm run dev`
- Build frontend:
  - `npm run build`
- Preview frontend build:
  - `npm run preview`

## Coding Style & Naming Conventions
- JavaScript/React: 2-space indentation (see `frontend/src/App.jsx`).
- Python: follow standard 4-space indentation.
- Keep file names descriptive (e.g., `main.py`, `App.jsx`).
- No formatting or linting tools are configured in the repo yet.

## Testing Guidelines
- No test framework or test commands are configured.
- If adding tests, prefer colocated `__tests__/` or a top-level `tests/` directory and document the command.

## Commit & Pull Request Guidelines
- Git history is empty, so no commit message convention is established yet.
- Suggested practice:
  - Commits: short, imperative summaries (e.g., “Add poem API fallback”).
  - PRs: include a clear description, steps to verify, and screenshots for UI changes.

## Security & Configuration Tips
- Backend expects `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`) in `backend/.env`.
- Avoid committing secrets; keep environment variables in local `.env` files.
