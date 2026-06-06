"""
Recommendation Engine — Rule-based improvement suggestions from missing features.

Recommendations and point values vary by project type.
"""

from analyzers.project_types import get_recommendation_rules, get_score_weights, normalize_project_type


def _impact_for_points(points: int) -> str:
    if points >= 20:
        return "High"
    if points >= 15:
        return "Medium"
    return "Low"


def generate_recommendations(
    features: dict,
    project_type: str | None = None,
) -> dict:
    """
    Builds actionable recommendations for each missing feature.

    Returns:
        { "recommendations": [ { "title", "impact", "points" }, ... ] }
    """
    normalized_type = normalize_project_type(project_type)
    weights = get_score_weights(normalized_type)
    rules = get_recommendation_rules(normalized_type)

    if not features:
        features = {}

    recommendations = []

    for feature_key, rule in rules.items():
        if features.get(feature_key):
            continue

        points = weights.get(feature_key, 0)
        recommendations.append({
            "title": rule["title"],
            "impact": _impact_for_points(points),
            "points": points,
        })

    recommendations.sort(key=lambda r: r["points"], reverse=True)

    return {"recommendations": recommendations}
