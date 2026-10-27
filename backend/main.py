from typing import Literal
from urllib.parse import quote_plus

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from curriculum_grounding import ground_domain
from llm import evaluate_solution, generate_learning_plan
from progress_tracking import (
    get_checkpoints,
    get_latest_plan,
    get_solution_history,
    get_solution_progress,
    init_db,
    plan_exists,
    save_plan,
    save_solution_submission,
    update_checkpoint_status,
)
from rice_profiling import compute_rice_vector


class GeneratePlanRequest(BaseModel):
    goal: str = Field(min_length=2, max_length=300)
    resources: list[str] = Field(default_factory=list)
    intensity: str = Field(default="Medium", min_length=1, max_length=80)
    constraints: list[str] = Field(default_factory=list)
    experience: str = Field(default="Beginner", min_length=1, max_length=80)


class CheckpointStatusRequest(BaseModel):
    status: Literal["not_started", "in_progress", "completed"]


class EvaluateSolutionRequest(BaseModel):
    plan_id: int = Field(gt=0)
    topic: str = Field(min_length=1, max_length=200)
    task: str = Field(min_length=1, max_length=4000)
    solution: str = Field(min_length=1, max_length=20000)


app = FastAPI(title="Instincts AI API", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    """Lightweight endpoint to verify that the backend is running."""
    return {"status": "ok", "service": "instincts-ai-api"}


@app.post("/api/generate-plan")
def create_plan(request: GeneratePlanRequest) -> dict:
    profile = request.model_dump()
    rice_vector = compute_rice_vector(profile)
    grounding = ground_domain(profile["goal"])
    try:
        plan = generate_learning_plan(profile, rice_vector, grounding)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Learning-plan generation failed. Check the AI service configuration and try again.",
        ) from error

    plan_id = save_plan(profile, plan)
    return {
        "plan_id": plan_id,
        "plan": plan,
        "profile_vector": rice_vector,
        "grounded_domain": grounding["domain"],
    }


@app.get("/api/resources")
def get_learning_resources(
    goal: str = Query(min_length=1, max_length=300),
    topic: str = Query(default="", max_length=200),
) -> dict:
    """Return curated materials plus searches for video tutorials and summaries."""
    search_text = " ".join(part.strip() for part in (goal, topic) if part and part.strip())
    # Prefer the learner's stated goal so an unrelated topic keyword cannot change domains.
    grounding = ground_domain(goal)
    if not grounding["grounded"] and topic.strip():
        grounding = ground_domain(topic)
    query = quote_plus(search_text)
    return {
        "grounded": grounding["grounded"],
        "domain": grounding["domain"],
        "resources": grounding["resources"],
        "youtube_search_url": f"https://www.youtube.com/results?search_query={query}+tutorial",
        "summary_search_url": f"https://www.google.com/search?q={query}+learning+summary",
        "note": None if grounding["grounded"] else "No curated category matched this goal. Search links are suggestions, not verified curated resources.",
    }


@app.get("/api/checkpoints/{plan_id}")
def list_plan_checkpoints(plan_id: int) -> list[dict]:
    if not plan_exists(plan_id):
        raise HTTPException(status_code=404, detail="Learning plan not found.")
    return get_checkpoints(plan_id)


@app.patch("/api/checkpoints/{checkpoint_id}")
def set_checkpoint_status(checkpoint_id: int, request: CheckpointStatusRequest) -> dict:
    updated = update_checkpoint_status(checkpoint_id, request.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Checkpoint not found.")
    return {"checkpoint_id": checkpoint_id, "status": request.status}


@app.get("/api/latest-plan")
def latest_plan() -> dict | None:
    return get_latest_plan()


@app.post("/api/evaluate-solution")
def submit_solution(request: EvaluateSolutionRequest) -> dict:
    """Grade the learner's own attempt and save every revision for progress tracking."""
    if not plan_exists(request.plan_id):
        raise HTTPException(status_code=404, detail="Learning plan not found.")

    try:
        evaluation = evaluate_solution(
            topic=request.topic,
            task=request.task,
            solution=request.solution,
        )
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Solution evaluation is temporarily unavailable. Your attempt was not saved; please try again.",
        ) from error

    submission = save_solution_submission(
        plan_id=request.plan_id,
        topic=request.topic.strip(),
        task=request.task.strip(),
        solution=request.solution,
        score=evaluation["score"],
        feedback=evaluation["feedback"],
    )
    progress = get_solution_progress(request.plan_id)
    topic_progress = next(
        item for item in progress["topics"] if item["topic"].casefold() == request.topic.strip().casefold()
    )
    return {
        **submission,
        "percentage": round(evaluation["score"] * 100),
        "mastered": topic_progress["mastered"],
        "attempt_count": topic_progress["attempt_count"],
        "best_score": topic_progress["best_score"],
    }


@app.get("/api/solution-progress/{plan_id}")
def solution_progress(plan_id: int) -> dict:
    if not plan_exists(plan_id):
        raise HTTPException(status_code=404, detail="Learning plan not found.")
    return get_solution_progress(plan_id)


@app.get("/api/solution-history/{plan_id}")
def solution_history(
    plan_id: int,
    topic: str = Query(min_length=1, max_length=200),
) -> list[dict]:
    if not plan_exists(plan_id):
        raise HTTPException(status_code=404, detail="Learning plan not found.")
    return get_solution_history(plan_id, topic)
