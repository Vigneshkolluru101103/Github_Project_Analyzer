"""
Project Scoring Engine — scores capabilities, not individual technologies.
"""

from analyzers.capabilities import MAX_SCORE, get_capability_labels, get_score_weights, normalize_project_type


def get_maturity_level(score: int) -> str:
    if score >= 86:
        return "Production Ready"
    if score >= 61:
        return "Advanced"
    if score >= 31:
        return "Intermediate"
    return "Beginner"


def _capability_detected(capabilities: dict, key: str) -> bool:
    """Read detected flag from bool map or detailed capability dict."""
    value = capabilities.get(key)
    if isinstance(value, dict):
        return bool(value.get("detected"))
    return bool(value)


def calculate_score(capabilities: dict, project_type: str | None = None) -> dict:
    """
    Computes project quality score from capability detection results.

    Each capability contributes its full weight when ANY indicator is present.
    """
    normalized_type = normalize_project_type(project_type)
    weights = get_score_weights(normalized_type)
    labels = get_capability_labels(normalized_type)

    if not capabilities:
        return {
            "score": 0,
            "maturity": "Beginner",
            "potential_score": MAX_SCORE,
            "project_type": normalized_type,
            "strengths": [],
            "missing": [labels[k] for k in weights],
        }

    score = 0
    missing_points = 0
    strengths = []
    missing = []
    breakdown = []

    for key, points in weights.items():
        label = labels.get(key, key.replace("_", " ").title())
        is_detected = _capability_detected(capabilities, key)
        if is_detected:
            score += points
            strengths.append(label)
            breakdown.append({
                "category": label,
                "score": points,
                "max_score": points,
                "reason": f"{label} detected and configured."
            })
        else:
            missing.append(label)
            missing_points += points
            breakdown.append({
                "category": label,
                "score": 0,
                "max_score": points,
                "reason": f"No {label.lower()} implementation found."
            })

    score = min(score, MAX_SCORE)

    return {
        "score": score,
        "maturity": get_maturity_level(score),
        "potential_score": min(score + missing_points, MAX_SCORE),
        "project_type": normalized_type,
        "strengths": strengths,
        "missing": missing,
        "breakdown": breakdown,
    }
