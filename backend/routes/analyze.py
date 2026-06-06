import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from analyzers.capabilities import PROJECT_TYPES
from analyzers.feature_analyzer import detect_features
from analyzers.recommendation_engine import generate_recommendations
from analyzers.scoring_engine import calculate_score
from analyzers.tech_analyzer import detect_technologies
from database.database import get_db
from services.analysis_history_service import save_analysis_history
from services.github_service import fetch_repository_data, fetch_repo_tree

logger = logging.getLogger(__name__)

router = APIRouter()

ProjectType = Literal[
    "Web Application",
    "Backend API",
    "Mobile App",
    "Machine Learning",
    "Data Science",
]


class RepoRequest(BaseModel):
    repo_url: str
    project_type: ProjectType = Field(
        ...,
        description="Category of project being analyzed",
    )


@router.post("/analyze")
def analyze_repo(request: RepoRequest, db: Session = Depends(get_db)):
    try:
        project_type = request.project_type

        repo_data = fetch_repository_data(request.repo_url)
        repo_data["project_type"] = project_type

        owner = repo_data["owner"]
        repo_name = repo_data["repo_name"]
        branch = repo_data["default_branch"]

        file_paths = fetch_repo_tree(owner, repo_name, branch)

        # Technologies: informational stack detection (not scored individually)
        repo_data["technologies"] = detect_technologies(file_paths, owner, repo_name)

        # Capabilities: scored architectural building blocks
        repo_data["capabilities"] = detect_features(
            file_paths, owner, repo_name, project_type,
            technologies=repo_data["technologies"],
        )

        # Backward-compatible alias for DB / legacy consumers
        repo_data["features"] = repo_data["capabilities"]

        repo_data["evaluation"] = calculate_score(repo_data["capabilities"], project_type)
        repo_data["recommendations"] = generate_recommendations(
            repo_data["capabilities"], project_type
        )["recommendations"]

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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Analysis failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-types")
def list_project_types():
    return {"project_types": list(PROJECT_TYPES)}
