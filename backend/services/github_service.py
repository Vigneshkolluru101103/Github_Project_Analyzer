import requests
import re
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def extract_owner_repo(url: str):
    """
    Extracts the owner and repository name from a GitHub URL.
    """
    url = url.strip().rstrip("/")
    
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format. Expected: https://github.com/owner/repo")
    
    owner = match.group(1)
    repo = match.group(2)
    if repo.endswith(".git"):
        repo = repo[:-4]
        
    return owner, repo

def fetch_repository_data(repo_url: str):
    """
    Fetches core repository details from the GitHub REST API.
    """
    owner, repo = extract_owner_repo(repo_url)
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Repository not found: {owner}/{repo}. Is it private?")
    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded. Please configure a GITHUB_TOKEN in backend/.env")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository data from GitHub.")
        
    data = response.json()
    
    return {
        "owner": owner,
        "repo_name": repo,
        "default_branch": data.get("default_branch", "main"),
        "name": data.get("name", ""),
        "description": data.get("description", "No description provided."),
        "language": data.get("language", "Unknown"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "visibility": data.get("visibility", "public").capitalize(),
        "repo_url": data.get("html_url", repo_url)
    }
