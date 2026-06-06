import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.analysis_history import AnalysisHistory

logger = logging.getLogger(__name__)


def _extract_save_fields(repo_data: dict) -> dict:
    """
    Extract repository metadata for persistence.
    Prefers GitHub API field names (stargazers_count, forks_count).
    """
    stars = repo_data.get("stargazers_count", repo_data.get("stars", 0))
    forks = repo_data.get("forks_count", repo_data.get("forks", 0))

    return {
        "repo_url": repo_data.get("repo_url", ""),
        "repo_name": repo_data.get("name") or repo_data.get("repo_name", ""),
        "description": repo_data.get("description"),
        "language": repo_data.get("language"),
        "stars": int(stars) if stars is not None else 0,
        "forks": int(forks) if forks is not None else 0,
    }


def save_analysis_history(db: Session, repo_data: dict) -> AnalysisHistory:
    """Persist a successful repository analysis to the database."""
    fields = _extract_save_fields(repo_data)
    evaluation = repo_data.get("evaluation") or {}

    print("Saving:")
    print(f"  repo_name: {fields['repo_name']}")
    print(f"  stars:     {fields['stars']}")
    print(f"  forks:     {fields['forks']}")
    print(f"  language:  {fields['language']}")

    logger.info(
        "Saving analysis — repo_name=%s stars=%s forks=%s language=%s",
        fields["repo_name"],
        fields["stars"],
        fields["forks"],
        fields["language"],
    )

    record = AnalysisHistory(
        repo_url=fields["repo_url"],
        repo_name=fields["repo_name"],
        description=fields["description"],
        language=fields["language"],
        stars=fields["stars"],
        forks=fields["forks"],
        score=evaluation.get("score", 0),
        maturity=evaluation.get("maturity"),
        potential_score=evaluation.get("potential_score"),
        technologies=repo_data.get("technologies"),
        features=repo_data.get("features"),
        evaluation=evaluation,
        recommendations=repo_data.get("recommendations"),
        analyzed_at=datetime.now(timezone.utc),
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info(
            "Analysis saved successfully (id=%s, repo=%s, stars=%s, forks=%s)",
            record.id,
            record.repo_name,
            record.stars,
            record.forks,
        )
        print("Analysis saved successfully")
        return record
    except Exception as exc:
        db.rollback()
        logger.error("Failed to save analysis history: %s", exc, exc_info=True)
        print(f"Failed to save analysis history: {exc}")
        raise
