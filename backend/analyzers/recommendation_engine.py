"""
Recommendation Engine — suggests missing capabilities only (never alternative technologies).
"""

from analyzers.capabilities import get_recommendation_rules, get_score_weights, normalize_project_type
from analyzers.scoring_engine import _capability_detected


def _impact_for_points(points: int) -> str:
    if points >= 20:
        return "High"
    if points >= 15:
        return "Medium"
    return "Low"


def generate_recommendations(
    capabilities: dict,
    project_type: str | None = None,
) -> dict:
    """
    Builds recommendations only for capabilities that are truly missing.
    Never recommends alternative frameworks when a capability is already satisfied.
    """
    normalized_type = normalize_project_type(project_type)
    weights = get_score_weights(normalized_type)
    rules = get_recommendation_rules(normalized_type)

    recommendations = []

    for feature_key, rule in rules.items():
        if _capability_detected(capabilities, feature_key):
            continue

        points = weights.get(feature_key, 0)
        recommendations.append({
            "title": rule["title"],
            "impact": _impact_for_points(points),
            "points": points,
            "capability": feature_key,
        })

    recommendations.sort(key=lambda r: r["points"], reverse=True)
    return {"recommendations": recommendations}
