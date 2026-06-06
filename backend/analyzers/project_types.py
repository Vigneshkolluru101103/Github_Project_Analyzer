"""
Backward-compatible re-exports from the capabilities registry.
"""

from analyzers.capabilities import (
    CAPABILITIES_BY_TYPE,
    DEFAULT_PROJECT_TYPE,
    MAX_SCORE,
    PROJECT_TYPES,
    RecommendationRule,
    get_capability_labels,
    get_recommendation_rules,
    get_score_weights,
    normalize_project_type,
)

# Legacy aliases
FEATURE_LABELS_BY_TYPE = {
    pt: get_capability_labels(pt) for pt in PROJECT_TYPES
}
get_feature_labels = get_capability_labels
