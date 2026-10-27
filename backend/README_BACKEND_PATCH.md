# Instincts AI backend patch

This is a source-only backend patch. It intentionally excludes `.env`, `__pycache__`, and the database file.

## Install / run

From the `backend` directory in your existing project, retain your existing `.env` and copy these updated files over the corresponding source files. Keep your current `instincts_ai.db`; the application creates the new `solution_submissions` table automatically on startup.

Install the existing requirements if not already installed:

```powershell
python -m pip install -r requirements.txt
```

Run from the backend directory:

```powershell
python -m uvicorn main:app --reload
```

The existing roadmap endpoints remain available. New endpoints:

- `GET /api/health`
- `GET /api/resources?goal=python%20programming&topic=loops`
- `POST /api/evaluate-solution`
- `GET /api/solution-progress/{plan_id}`
- `GET /api/solution-history/{plan_id}?topic=Python%20loops`

Example solution request body:

```json
{
  "plan_id": 1,
  "topic": "Python loops",
  "task": "Write a loop that adds integers from 1 through 5.",
  "solution": "total = 0\nfor i in range(1, 6):\n    total += i"
}
```

The AI evaluator returns a score in `[0, 1]`, a percentage, constructive feedback, and whether the topic has reached a perfect score in its attempt history. Each submission is saved, so the learner can revise and try again. AI evaluation requires a valid `GROQ_API_KEY` in `backend/.env`.
