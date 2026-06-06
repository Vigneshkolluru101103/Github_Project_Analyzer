import logging
from typing import Literal

import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import jwt

from analyzers.capabilities import PROJECT_TYPES
from analyzers.feature_analyzer import detect_features
from analyzers.recommendation_engine import generate_recommendations
from analyzers.scoring_engine import calculate_score
from analyzers.tech_analyzer import detect_technologies
from database.database import get_db
from models.analysis_history import AnalysisHistory
from services.analysis_history_service import save_analysis_history
from services.jwt_service import decode_access_token
from services.github_service import fetch_repository_data, fetch_repo_tree
from services.pdf_service import generate_report_pdf

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer(auto_error=False)

def get_current_user_id_optional(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> int | None:
    if not credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None

def get_current_user_id_required(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> int:
    user_id = get_current_user_id_optional(credentials)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user_id

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
def analyze_repo(
    request: RepoRequest, 
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_current_user_id_optional)
):
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

        if user_id:
            try:
                record = save_analysis_history(db, repo_data, user_id=user_id)
                repo_data["id"] = record.id
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


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_required)
):
    records = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == user_id).order_by(AnalysisHistory.analyzed_at.desc()).all()
    return [
        {
            "id": r.id,
            "name": r.repo_name,
            "project_type": r.project_type,
            "score": r.score,
            "date": r.analyzed_at.strftime("%Y-%m-%d"),
        }
        for r in records
    ]


@router.get("/analysis/{analysis_id}")
def get_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_required)
):
    record = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    return {
        "message": "Analysis retrieved successfully",
        "data": {
            "repo_url": record.repo_url,
            "name": record.repo_name,
            "project_type": record.project_type,
            "description": record.description,
            "language": record.language,
            "stars": record.stars,
            "forks": record.forks,
            "score": record.score,
            "maturity": record.maturity,
            "potential_score": record.potential_score,
            "technologies": record.technologies,
            "features": record.features,
            "capabilities": record.features,
            "evaluation": record.evaluation,
            "recommendations": record.recommendations,
            "analyzed_at": record.analyzed_at.isoformat() if record.analyzed_at else None,
        }
    }


@router.get("/analysis/{analysis_id}/pdf")
def get_analysis_pdf(
    analysis_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id_required)
):
    record = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id, AnalysisHistory.user_id == user_id).first()
    if not record:
        logger.warning(f"Analysis {analysis_id} not found for user {user_id}")
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    logger.info(f"Generating PDF for Analysis ID: {analysis_id}")
    logger.info(f"Repository Name: {record.repo_name}")
    logger.info(f"User ID: {user_id}")
    logger.info("PDF generation start")
    
    try:
        report_data = {
            "repo_url": record.repo_url,
            "name": record.repo_name,
            "project_type": record.project_type,
            "description": record.description,
            "language": record.language,
            "stars": record.stars,
            "forks": record.forks,
            "score": record.score,
            "maturity": record.maturity,
            "potential_score": record.potential_score,
            "technologies": record.technologies,
            "features": record.features,
            "capabilities": record.features,
            "evaluation": record.evaluation,
            "recommendations": record.recommendations,
            "analyzed_at": record.analyzed_at,
        }
        
        pdf_buffer = generate_report_pdf(report_data)
        
        # Sanitize repo name for filename
        safe_name = "".join(c if c.isalnum() else "-" for c in record.repo_name).strip("-")
        if not safe_name:
            safe_name = "project"
        filename = f"{safe_name}-analysis-report.pdf"
        
        # Save buffer to a temporary file
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, filename)
        
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getbuffer())
            
        # Verify file
        if not os.path.exists(pdf_path):
            raise Exception("Output path does not exist after generation")
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            raise Exception("Generated PDF file is 0 bytes")
            
        logger.info(f"PDF generation success. Size: {file_size} bytes. Path: {pdf_path}")
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )

@router.post("/analysis/pdf/raw")
def get_raw_analysis_pdf(request: dict):
    # Endpoint for downloading unsaved analysis (e.g. guest users)
    # The frontend can send the result.data to get a PDF back.
    repo_name = request.get("name", "project")
    safe_name = "".join(c if c.isalnum() else "-" for c in repo_name).strip("-")
    if not safe_name:
        safe_name = "project"
    filename = f"{safe_name}-analysis-report.pdf"
    
    logger.info(f"Generating RAW PDF for Repository: {repo_name}")
    logger.info("PDF generation start")
    
    try:
        pdf_buffer = generate_report_pdf(request)
        
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, filename)
        
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getbuffer())
            
        if not os.path.exists(pdf_path):
            raise Exception("Output path does not exist after generation")
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            raise Exception("Generated PDF file is 0 bytes")
            
        logger.info(f"PDF generation success. Size: {file_size} bytes. Path: {pdf_path}")
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        logger.error(f"RAW PDF generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )
