"""
Recommendation Engine — Rule-based improvement suggestions from missing features.
"""

from analyzers.scoring_engine import SCORE_WEIGHTS


RECOMMENDATION_RULES = {
    "authentication": {
        "title": "Implement JWT Authentication",
    },
    "database": {
        "title": "Integrate PostgreSQL or MongoDB",
    },
    "testing": {
        "title": "Add automated testing using pytest or jest",
    },
    "docker": {
        "title": "Containerize the application using Docker",
    },
    "cicd": {
        "title": "Configure GitHub Actions workflow",
    },
    "environment_variables": {
        "title": "Move secrets and configuration into .env files",
    },
}


def _impact_for_points(points: int) -> str:
    if points >= 20:
        return "High"
    if points >= 15:
        return "Medium"
    return "Low"


def generate_recommendations(features: dict) -> dict:
    """
    Builds actionable recommendations for each missing feature.

    Returns:
        { "recommendations": [ { "title", "impact", "points" }, ... ] }
    """
    if not features:
        features = {}

    recommendations = []

    for feature_key, rule in RECOMMENDATION_RULES.items():
        if features.get(feature_key):
            continue

        points = SCORE_WEIGHTS.get(feature_key, 0)
        recommendations.append({
            "title": rule["title"],
            "impact": _impact_for_points(points),
            "points": points,
        })

    recommendations.sort(key=lambda r: r["points"], reverse=True)

    return {"recommendations": recommendations}
