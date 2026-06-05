from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_service import fetch_repository_data
from analyzers.tech_analyzer import analyze_project

router = APIRouter()

class RepoRequest(BaseModel):
    repo_url: str

@router.post("/analyze")
def analyze_repo(request: RepoRequest):
    try:
        repo_data = fetch_repository_data(request.repo_url)
        
        # Detect technologies and features
        analysis = analyze_project(
            repo_data["owner"], 
            repo_data["repo_name"], 
            repo_data["default_branch"]
        )
        
        repo_data["technologies"] = analysis["technologies"]
        repo_data["features"] = analysis["features"]
        
        return {
            "message": "Repository data fetched successfully",
            "data": repo_data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
