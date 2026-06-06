import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from analyzers.feature_analyzer import detect_features
from analyzers.recommendation_engine import generate_recommendations
from analyzers.scoring_engine import calculate_score
from analyzers.tech_analyzer import detect_technologies
from database.database import get_db
from services.analysis_history_service import save_analysis_history
from services.github_service import fetch_repository_data, fetch_repo_tree

logger = logging.getLogger(__name__)

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: str


@router.post("/analyze")
def analyze_repo(request: RepoRequest, db: Session = Depends(get_db)):
    try:
        # 1. Fetch core repo metadata from GitHub
        repo_data = fetch_repository_data(request.repo_url)

        owner = repo_data["owner"]
        repo_name = repo_data["repo_name"]
        branch = repo_data["default_branch"]

        # 2. Fetch file tree once (shared by all analyzers)
        file_paths = fetch_repo_tree(owner, repo_name, branch)

        # 3. Run analyzers
        repo_data["technologies"] = detect_technologies(file_paths, owner, repo_name)
        repo_data["features"] = detect_features(file_paths, owner, repo_name)
        repo_data["evaluation"] = calculate_score(repo_data["features"])
        repo_data["recommendations"] = generate_recommendations(repo_data["features"])["recommendations"]

        # 4. Save analysis history to PostgreSQL
        try:
            save_analysis_history(db, repo_data)
        except Exception as save_exc:
            logger.error("Analysis completed but database save failed: %s", save_exc)

        return {
            "message": "Repository analyzed successfully",
            "data": repo_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Analysis failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
