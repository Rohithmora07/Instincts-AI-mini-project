import os
from pathlib import Path

from dotenv import load_dotenv

from prompts import build_learning_plan_prompt, build_solution_evaluation_prompt
from utils import normalize_plan, parse_json_object

# Load the backend .env regardless of the directory from which Uvicorn is started.
load_dotenv(Path(__file__).resolve().parent / ".env")

MODEL = "openai/gpt-oss-120b"


def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Add GROQ_API_KEY to backend/.env to use AI-powered features.")
    try:
        from groq import Groq
    except ImportError as error:
        raise RuntimeError("The Groq package is missing. Install backend requirements first.") from error
    return Groq(api_key=api_key)


def _generate_json(prompt: str, max_tokens: int) -> dict:
    request = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    client = get_client()
    try:
        response = client.chat.completions.create(**request)
    except Exception as error:
        error_text = str(error).lower()
        # Some model/API versions reject JSON mode. Retry once without that option only then.
        if "response_format" not in error_text and "json_validate_failed" not in error_text and "failed_generation" not in error_text:
            raise
        request.pop("response_format", None)
        response = client.chat.completions.create(**request)

    content = response.choices[0].message.content or ""
    return parse_json_object(content)


def generate_learning_plan(profile: dict, rice_vector: dict, grounding: dict) -> dict[str, str]:
    raw_plan = _generate_json(build_learning_plan_prompt(profile, rice_vector, grounding), max_tokens=2200)
    return normalize_plan(raw_plan)


def evaluate_solution(topic: str, task: str, solution: str) -> dict:
    """Return rubric-based partial credit and a hint without revealing a full solution."""
    raw = _generate_json(
        build_solution_evaluation_prompt(topic=topic, task=task, solution=solution),
        max_tokens=700,
    )
    try:
        score = float(raw["score"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("The AI evaluator did not return a valid numeric score.") from error
    if not 0.0 <= score <= 1.0:
        raise ValueError("The AI evaluator returned a score outside the 0 to 1 range.")
    rounded_score = round(score, 2)
    if score < 1.0 and rounded_score >= 1.0:
        rounded_score = 0.99
    feedback = raw.get("feedback")
    if not isinstance(feedback, str) or not feedback.strip():
        raise ValueError("The AI evaluator did not return useful feedback.")
    return {"score": rounded_score, "feedback": feedback.strip()}
