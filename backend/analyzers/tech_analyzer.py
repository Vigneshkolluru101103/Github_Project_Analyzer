import json
from services.github_service import fetch_file_content

def detect_technologies(file_paths: list, owner: str, repo: str) -> list:
    """
    Detects technologies used in a project by analyzing file paths and dependency files.
    Returns a sorted list of technology names.
    """
    if not file_paths:
        return []
    
    technologies = set()
    
    # --- 1. Path-based detection ---
    for path in file_paths:
        path_lower = path.lower()
        
        if path_lower == "dockerfile" or path_lower.endswith("/dockerfile") or "docker-compose" in path_lower:
            technologies.add("Docker")
        if path_lower.startswith(".github/workflows/"):
            technologies.add("GitHub Actions")
        if ".gitlab-ci" in path_lower:
            technologies.add("GitLab CI")
        if "tailwind.config" in path_lower:
            technologies.add("Tailwind CSS")
        if "vite.config" in path_lower:
            technologies.add("Vite")
        if "webpack.config" in path_lower:
            technologies.add("Webpack")
        if "tsconfig" in path_lower:
            technologies.add("TypeScript")
    
    # --- 2. package.json analysis (JavaScript/Node ecosystem) ---
    if "package.json" in file_paths:
        technologies.add("Node.js")
        content = fetch_file_content(owner, repo, "package.json")
        if content:
            try:
                pkg = json.loads(content)
                all_deps = {
                    **pkg.get("dependencies", {}),
                    **pkg.get("devDependencies", {})
                }
                
                tech_map = {
                    "react": "React",
                    "next": "Next.js",
                    "vue": "Vue.js",
                    "svelte": "Svelte",
                    "express": "Express",
                    "fastify": "Fastify",
                    "mongoose": "MongoDB",
                    "mongodb": "MongoDB",
                    "pg": "PostgreSQL",
                    "mysql2": "MySQL",
                    "sequelize": "Sequelize ORM",
                    "@prisma/client": "Prisma",
                    "prisma": "Prisma",
                    "typeorm": "TypeORM",
                    "redis": "Redis",
                    "tailwindcss": "Tailwind CSS",
                    "@tailwindcss/vite": "Tailwind CSS",
                    "typescript": "TypeScript",
                    "socket.io": "Socket.IO",
                    "graphql": "GraphQL",
                }
                
                for dep_key, tech_name in tech_map.items():
                    if dep_key in all_deps:
                        technologies.add(tech_name)
            except (json.JSONDecodeError, Exception):
                pass
    
    # --- 3. Python dependency file analysis ---
    req_files = [p for p in file_paths if p.endswith("requirements.txt") or p == "pyproject.toml"]
    for req_file in req_files[:2]:
        content = fetch_file_content(owner, repo, req_file)
        if content:
            technologies.add("Python")
            content_lower = content.lower()
            
            py_tech_map = {
                "fastapi": "FastAPI",
                "flask": "Flask",
                "django": "Django",
                "sqlalchemy": "SQLAlchemy",
                "psycopg2": "PostgreSQL",
                "asyncpg": "PostgreSQL",
                "pymongo": "MongoDB",
                "redis": "Redis",
                "celery": "Celery",
                "streamlit": "Streamlit",
                "tensorflow": "TensorFlow",
                "pytorch": "PyTorch",
                "torch": "PyTorch",
                "pandas": "Pandas",
                "numpy": "NumPy",
            }
            
            for dep_key, tech_name in py_tech_map.items():
                if dep_key in content_lower:
                    technologies.add(tech_name)
    
    return sorted(list(technologies))
