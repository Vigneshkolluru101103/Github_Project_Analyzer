"""
Project Scoring Engine — Calculates quality score from detected features.

Each feature contributes a fixed number of points (max 100 total).
"""

MAX_SCORE = 100

SCORE_WEIGHTS = {
    "authentication":        20,
    "database":              20,
    "api_layer":             15,
    "testing":               15,
    "docker":                10,
    "cicd":                  10,
    "environment_variables": 10,
}

FEATURE_LABELS = {
    "authentication":        "Authentication",
    "database":              "Database",
    "api_layer":             "API Layer",
    "testing":               "Testing",
    "docker":                "Docker",
    "cicd":                  "CI/CD",
    "environment_variables": "Environment Variables",
}


def get_maturity_level(score: int) -> str:
    """Maps a score to a project maturity label."""
    if score >= 86:
        return "Production Ready"
    if score >= 61:
        return "Advanced"
    if score >= 31:
        return "Intermediate"
    return "Beginner"


def calculate_score(features: dict) -> dict:
    """
    Computes project quality score from feature detection results.

    Returns:
        {
            "score": int,
            "maturity": str,
            "potential_score": int,
            "strengths": list[str],
            "missing": list[str],
        }
    """
    if not features:
        return {
            "score": 0,
            "maturity": "Beginner",
            "potential_score": MAX_SCORE,
            "strengths": [],
            "missing": list(FEATURE_LABELS.values()),
        }

    score = 0
    missing_points = 0
    strengths = []
    missing = []

    for key, points in SCORE_WEIGHTS.items():
        label = FEATURE_LABELS.get(key, key.replace("_", " ").title())
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
        "strengths": strengths,
        "missing": missing,
    }
