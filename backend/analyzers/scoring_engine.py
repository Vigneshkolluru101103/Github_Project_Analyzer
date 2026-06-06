"""
Project Scoring Engine — Calculates quality score from detected features.

Weights vary by project type (see project_types.py).
"""

from analyzers.project_types import (
    MAX_SCORE,
    get_feature_labels,
    get_score_weights,
    normalize_project_type,
)


def get_maturity_level(score: int) -> str:
    """Maps a score to a project maturity label."""
    if score >= 86:
        return "Production Ready"
    if score >= 61:
        return "Advanced"
    if score >= 31:
        return "Intermediate"
    return "Beginner"


def calculate_score(features: dict, project_type: str | None = None) -> dict:
    """
    Computes project quality score from feature detection results.

    Returns:
        {
            "score": int,
            "maturity": str,
            "potential_score": int,
            "project_type": str,
            "strengths": list[str],
            "missing": list[str],
        }
    """
    normalized_type = normalize_project_type(project_type)
    weights = get_score_weights(normalized_type)
    labels = get_feature_labels(normalized_type)

    if not features:
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

    for key, points in weights.items():
        label = labels.get(key, key.replace("_", " ").title())
        detected = bool(features.get(key, False))

        if detected:
            score += points
            strengths.append(label)
        else:
            missing.append(label)
            missing_points += points

    score = min(score, MAX_SCORE)

    return {
        "score": score,
        "maturity": get_maturity_level(score),
        "potential_score": min(score + missing_points, MAX_SCORE),
        "project_type": normalized_type,
        "strengths": strengths,
        "missing": missing,
    }
