import json
from functools import lru_cache
from pathlib import Path

RESOURCE_PATH = Path(__file__).resolve().parent / "curated_resources.json"


@lru_cache(maxsize=1)
def _load_resources() -> dict:
    with RESOURCE_PATH.open(encoding="utf-8") as resource_file:
        return json.load(resource_file)


def ground_domain(goal: str) -> dict:
    """Match a learner goal to a curated domain using keyword search."""
    goal_lower = (goal or "").strip().casefold()
    for domain, data in _load_resources().items():
        if any(keyword.casefold() in goal_lower for keyword in data.get("keywords", [])):
            return {"grounded": True, "domain": domain, "resources": data.get("resources", [])}
    return {"grounded": False, "domain": None, "resources": []}
