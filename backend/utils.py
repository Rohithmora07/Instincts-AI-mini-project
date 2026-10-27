import json
from typing import Any


def build_profile(goal: str, resources: list[str], intensity: str, constraints: list[str], experience: str) -> dict:
    return {
        "goal": goal.strip(),
        "resources": resources or ["None"],
        "intensity": intensity,
        "constraints": constraints or ["None"],
        "experience": experience,
    }


def parse_json_object(text: str) -> dict[str, Any]:
    """Extract the first JSON object from a model response and validate its shape."""
    if not isinstance(text, str):
        raise ValueError("The AI response was empty or not text.")
    start = text.find("{")
    if start == -1:
        raise ValueError("The response was not returned in the expected JSON format.")
    try:
        result, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as error:
        raise ValueError("The response could not be read. Please try again.") from error
    if not isinstance(result, dict):
        raise ValueError("The response must be a JSON object.")
    return result


def normalize_plan(raw_plan: dict[str, Any]) -> dict[str, str]:
    fields = (
        "goal_summary", "learning_path", "weekly_roadmap", "recommended_resources",
        "practice_strategy", "milestones", "expected_outcome",
    )
    return {
        field: str(raw_plan.get(field, "Plan details are not available yet."))
        for field in fields
    }
