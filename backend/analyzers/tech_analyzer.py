import requests
import json
import base64
from services.github_service import GITHUB_TOKEN

def fetch_file_content(owner: str, repo: str, path: str):
    """Fetches the content of a specific file from the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8")
    return None

def analyze_project(owner: str, repo: str, default_branch: str):
    """Detects technologies and software engineering features."""
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        
    response = requests.get(tree_url, headers=headers)
    if response.status_code != 200:
        return {"technologies": [], "features": {}}
        
    tree = response.json().get("tree", [])
    file_paths = [item["path"] for item in tree if item["type"] == "blob"]
    
    technologies = set()
    features = {
        "authentication": False,
        "database": False,
        "rest_api": False,
        "testing": False,
        "docker": False,
        "cicd": False,
        "env_variables": False
    }
    
    # 1. Path-based detection
    for path in file_paths:
        path_lower = path.lower()
        if path_lower == "dockerfile" or path_lower.endswith("/dockerfile") or "docker-compose" in path_lower:
            technologies.add("Docker")
            features["docker"] = True
        if path_lower.startswith(".github/workflows/"):
            technologies.add("GitHub Actions")
            features["cicd"] = True
        if "jest.config" in path_lower or "test" in path_lower or "vitest.config" in path_lower:
            technologies.add("Testing Frameworks")
            features["testing"] = True
        if "pytest" in path_lower or "conftest.py" in path_lower:
            technologies.add("Testing Frameworks")
            features["testing"] = True
        if path_lower.endswith(".env") or ".env.example" in path_lower:
            features["env_variables"] = True
    
    # 2. package.json analysis
    if "package.json" in file_paths:
        technologies.add("Node.js")
        content = fetch_file_content(owner, repo, "package.json")
        if content:
            try:
                pkg = json.loads(content)
                deps = str(pkg.get("dependencies", {})) + str(pkg.get("devDependencies", {}))
                
                # Technologies
                if "react" in deps: technologies.add("React")
                if "next" in deps: technologies.add("Next.js")
                if "express" in deps: technologies.add("Express")
                if "mongodb" in deps or "mongoose" in deps: technologies.add("MongoDB")
                if "pg" in deps or "sequelize" in deps or "prisma" in deps: technologies.add("PostgreSQL")
                if "jest" in deps or "mocha" in deps or "vitest" in deps: technologies.add("Testing Frameworks")
                
                # Features
                if "jwt" in deps or "passport" in deps or "bcrypt" in deps or "next-auth" in deps:
                    features["authentication"] = True
                if "mongoose" in deps or "pg" in deps or "sequelize" in deps or "prisma" in deps or "typeorm" in deps:
                    features["database"] = True
                if "express" in deps or "nestjs" in deps:
                    features["rest_api"] = True
                if "jest" in deps or "vitest" in deps or "mocha" in deps:
                    features["testing"] = True
                if "dotenv" in deps:
                    features["env_variables"] = True
            except:
                pass
                
    # 3. requirements.txt or pyproject.toml analysis
    req_files = [p for p in file_paths if p.endswith("requirements.txt") or p == "pyproject.toml"]
    for req_file in req_files[:2]:
        content = fetch_file_content(owner, repo, req_file)
        if content:
            content_lower = content.lower()
            
            # Technologies
            if "fastapi" in content_lower: technologies.add("FastAPI")
            if "django" in content_lower: technologies.add("Django")
            if "psycopg2" in content_lower or "asyncpg" in content_lower or "sqlalchemy" in content_lower: technologies.add("PostgreSQL")
            if "pytest" in content_lower or "unittest" in content_lower: technologies.add("Testing Frameworks")
            
            # Features
            if "jwt" in content_lower or "bcrypt" in content_lower or "oauth" in content_lower or "passlib" in content_lower:
                features["authentication"] = True
            if "sqlalchemy" in content_lower or "psycopg2" in content_lower or "pymongo" in content_lower or "django" in content_lower:
                features["database"] = True
            if "fastapi" in content_lower or "django" in content_lower or "flask" in content_lower:
                features["rest_api"] = True
            if "pytest" in content_lower or "coverage" in content_lower:
                features["testing"] = True
            if "python-dotenv" in content_lower or "decouple" in content_lower:
                features["env_variables"] = True

    return {
        "technologies": sorted(list(technologies)),
        "features": features
    }
