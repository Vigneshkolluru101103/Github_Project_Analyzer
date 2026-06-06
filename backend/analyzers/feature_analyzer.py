"""
Feature Analyzer — delegates to capability-based detection.

Capabilities are architectural building blocks; individual technologies
only serve as indicators to detect them.
"""

from analyzers.capability_detector import capabilities_to_bool_map, detect_capabilities


def detect_features(
    file_paths: list,
    owner: str,
    repo: str,
    project_type: str | None = None,
    technologies: list[str] | None = None,
) -> dict:
    """
    Detect project capabilities for the given project type.
    Returns detailed capability map { key: { detected, label, weight, matched } }.
    """
    return detect_capabilities(
        file_paths, owner, repo, project_type, technologies=technologies
    )


def detect_features_bool(
    file_paths: list,
    owner: str,
    repo: str,
    project_type: str | None = None,
    technologies: list | None = None,
) -> dict[str, bool]:
    """Return flat { capability_key: bool } map."""
    detailed = detect_features(file_paths, owner, repo, project_type, technologies)
    return capabilities_to_bool_map(detailed)
