def _experience_score(experience: str) -> float:
    value = str(experience or "").strip().casefold()
    if value.startswith("beginner"):
        return 0.2
    if value.startswith("intermediate"):
        return 0.6
    if value.startswith("advanced"):
        return 1.0
    return 0.5


def _intensity_score(intensity: str) -> float:
    value = str(intensity or "").strip().casefold()
    # Check the more specific phrase before the shorter 'high' label.
    if value.startswith("very high"):
        return 1.0
    if value.startswith("low"):
        return 0.25
    if value.startswith("medium"):
        return 0.5
    if value.startswith("high"):
        return 0.75
    return 0.5


def _resource_score(resources: list[str]) -> float:
    useful_resources = [
        str(resource).strip()
        for resource in (resources or [])
        if str(resource).strip() and str(resource).strip().casefold() != "none"
    ]
    if not useful_resources:
        return 0.1
    return min(1.0, len(useful_resources) / 5)


def _constraint_score(constraints: list[str]) -> float:
    meaningful_constraints = [
        str(constraint).strip()
        for constraint in (constraints or [])
        if str(constraint).strip() and str(constraint).strip().casefold() != "none"
    ]
    return max(0.2, 1.0 - 0.2 * len(meaningful_constraints))


def compute_rice_vector(profile: dict) -> dict[str, float]:
    """Convert learner profile inputs into the project's pacing/difficulty vector.

    This preserves the project's existing weights; it is a lightweight rule-based
    profile vector, not the standard business-prioritization RICE formula.
    """
    experience = _experience_score(profile.get("experience", ""))
    intensity = _intensity_score(profile.get("intensity", ""))
    resources = _resource_score(profile.get("resources", []))
    constraints = _constraint_score(profile.get("constraints", []))

    pace = round(0.5 * intensity + 0.5 * experience, 2)
    difficulty = round(0.7 * experience + 0.3 * resources, 2)
    return {"pace": pace, "difficulty": difficulty, "availability": constraints}
