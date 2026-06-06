import base64
import logging
import os
import re

import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
logger = logging.getLogger(__name__)

def _get_headers():
    """Returns GitHub API headers with optional auth token."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

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
    
    response = requests.get(api_url, headers=_get_headers())
    
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Repository not found: {owner}/{repo}. Is it private?")
    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded. Please configure a GITHUB_TOKEN in backend/.env")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository data from GitHub.")
        
    data = response.json()

    stargazers_count = data.get("stargazers_count", 0)
    forks_count = data.get("forks_count", 0)

    repo_metadata = {
        "owner": owner,
        "repo_name": data.get("name", repo),
        "default_branch": data.get("default_branch", "main"),
        "name": data.get("name", repo),
        "description": data.get("description") or "No description provided.",
        "language": data.get("language") or "Unknown",
        "stargazers_count": stargazers_count,
        "forks_count": forks_count,
        # Aliases used by the frontend response
        "stars": stargazers_count,
        "forks": forks_count,
        "visibility": data.get("visibility", "public").capitalize(),
        "repo_url": data.get("html_url", repo_url),
    }

    logger.info(
        "GitHub API metadata for %s/%s — stars=%s forks=%s language=%s",
        owner,
        repo,
        stargazers_count,
        forks_count,
        repo_metadata["language"],
    )

    return repo_metadata

def fetch_repo_tree(owner: str, repo: str, default_branch: str):
    """Fetches the full recursive file tree for a repository. Returns list of file paths."""
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    response = requests.get(tree_url, headers=_get_headers())
    if response.status_code != 200:
        return []
    tree = response.json().get("tree", [])
    return [item["path"] for item in tree if item["type"] == "blob"]

def fetch_file_content(owner: str, repo: str, path: str):
    """Fetches and decodes the content of a specific file from the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=_get_headers())
    if response.status_code == 200:
        data = response.json()
        if "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8")
    return None
