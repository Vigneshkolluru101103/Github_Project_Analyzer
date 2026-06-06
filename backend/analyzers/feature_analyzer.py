"""
Feature Analyzer — Detects implemented software engineering features in a repository.

Architecture: Each feature category has its own detector function. Detectors are registered
in FEATURE_DETECTORS so new features can be added by simply writing a function and adding
an entry to the dict.
"""

import json
from services.github_service import fetch_file_content


# ---------------------------------------------------------------------------
# Content-fetching helper with per-analysis cache (avoids duplicate API calls
# when multiple detectors need the same file)
# ---------------------------------------------------------------------------

def _build_content_fetcher(owner: str, repo: str):
    """Returns a cached content-fetcher bound to a specific repo."""
    cache = {}

    def get(path: str):
        if path not in cache:
            cache[path] = fetch_file_content(owner, repo, path)
        return cache[path]

    return get


# ---------------------------------------------------------------------------
# Helper: parse package.json dependencies into a flat set of dep names
# ---------------------------------------------------------------------------

def _parse_js_deps(get_content) -> set:
    """Returns a set of all JS dependency names from package.json."""
    raw = get_content("package.json")
    if not raw:
        return set()
    try:
        pkg = json.loads(raw)
        deps = set(pkg.get("dependencies", {}).keys())
        deps.update(pkg.get("devDependencies", {}).keys())
        return deps
    except (json.JSONDecodeError, Exception):
        return set()


# ---------------------------------------------------------------------------
# Helper: collect all Python requirement lines (lowered) from the repo
# ---------------------------------------------------------------------------

def _collect_python_deps(file_paths: list, get_content) -> str:
    """Returns combined lowercase text of all requirements.txt / pyproject.toml files."""
    fragments = []
    for path in file_paths:
        if path.endswith("requirements.txt") or path == "pyproject.toml" or path == "Pipfile":
            content = get_content(path)
            if content:
                fragments.append(content.lower())
    return "\n".join(fragments)


# ===================================================================
#  INDIVIDUAL FEATURE DETECTORS
#  Each receives (file_paths, js_deps, py_deps_text, get_content)
#  and returns True / False.
# ===================================================================

def _detect_authentication(file_paths, js_deps, py_deps_text, get_content):
    """JWT, OAuth, bcrypt, passport, login/register routes, auth folders."""
    js_auth = {
        "jsonwebtoken", "jwt-decode", "bcrypt", "bcryptjs", "passport",
        "passport-jwt", "passport-local", "next-auth", "@auth0/nextjs-auth0",
        "express-session", "cookie-session", "@supabase/auth-helpers-nextjs",
        "firebase-admin", "jose",
    }
    if js_deps & js_auth:
        return True

    py_auth = [
        "pyjwt", "python-jose", "jose", "passlib", "bcrypt", "oauthlib",
        "django-allauth", "djangorestframework-simplejwt", "flask-login",
        "flask-jwt-extended", "authlib", "python-oauth2",
    ]
    if any(dep in py_deps_text for dep in py_auth):
        return True

    auth_keywords = {"auth", "login", "register", "signup", "signin"}
    code_extensions = (".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".rb")
    for path in file_paths:
        path_lower = path.lower()
        parts = path_lower.replace("\\", "/").split("/")
        if any(part in auth_keywords or part == "authentication" for part in parts):
            return True
        if path_lower.endswith(code_extensions):
            basename = parts[-1]
            if any(kw in basename for kw in auth_keywords):
                return True

    return False


def _detect_database(file_paths, js_deps, py_deps_text, get_content):
    """ORMs, SQL/NoSQL drivers, PostgreSQL/MySQL/SQLite, database config files."""
    js_db = {
        "mongoose", "mongodb", "pg", "mysql2", "sequelize", "sqlite3",
        "@prisma/client", "prisma", "typeorm", "knex", "better-sqlite3",
    }
    if js_deps & js_db:
        return True

    py_db = [
        "sqlalchemy", "psycopg2", "asyncpg", "pymongo", "motor", "peewee",
        "tortoise-orm", "alembic", "mysqlclient", "pymysql", "sqlite3",
        "django.db", "databases",
    ]
    if any(dep in py_deps_text for dep in py_db):
        return True

    db_config_names = {
        "database.yml", "database.yaml", "ormconfig.json", "ormconfig.js",
        "drizzle.config.ts", "drizzle.config.js", "schema.prisma",
    }
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        basename = path_lower.split("/")[-1]
        if basename in db_config_names or "schema.prisma" in path_lower:
            return True
        if "/migrations/" in path_lower or path_lower.startswith("migrations/"):
            return True
        if path_lower.endswith(".sql"):
            return True
        if "/database/" in path_lower or path_lower.startswith("database/"):
            return True

    return False


def _detect_api_layer(file_paths, js_deps, py_deps_text, get_content):
    """Express, FastAPI, Django REST Framework, etc."""
    # 1. JS dependencies
    js_api = {
        "express", "fastify", "koa", "@hapi/hapi",
        "@nestjs/core", "@nestjs/common",
    }
    if js_deps & js_api:
        return True

    # 2. Python dependencies
    py_api = ["fastapi", "flask", "djangorestframework", "django-ninja",
              "tornado", "aiohttp", "sanic"]
    if any(dep in py_deps_text for dep in py_api):
        return True

    # 3. Django projects with urls.py / views.py are API projects
    if "django" in py_deps_text:
        for path in file_paths:
            if path.endswith("views.py") or path.endswith("urls.py"):
                return True

    # 4. Route / controller directories
    route_dirs = ["routes/", "api/", "controllers/", "endpoints/", "routers/"]
    for path in file_paths:
        path_lower = path.lower()
        if any(path_lower.startswith(d) or f"/{d}" in path_lower for d in route_dirs):
            if path_lower.endswith((".py", ".js", ".ts")):
                return True

    return False


def _detect_testing(file_paths, js_deps, py_deps_text, get_content):
    """pytest, unittest, jest, vitest, test folders, __tests__."""
    js_test = {
        "jest", "vitest", "mocha", "chai", "cypress", "@playwright/test",
        "@testing-library/react", "@testing-library/jest-dom",
    }
    if js_deps & js_test:
        return True

    py_test = ["pytest", "unittest", "coverage", "tox", "nose2", "hypothesis"]
    if any(dep in py_deps_text for dep in py_test):
        return True

    test_dir_markers = {"/tests/", "/test/", "/__tests__/", "/spec/"}
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        normalized = f"/{path_lower}" if not path_lower.startswith("/") else path_lower
        if any(marker in normalized for marker in test_dir_markers):
            return True
        if path_lower.startswith(("tests/", "test/", "__tests__/")):
            return True
        if path_lower == "conftest.py" or path_lower.endswith("/conftest.py"):
            return True
        if "jest.config" in path_lower or "vitest.config" in path_lower:
            return True
        if path_lower.endswith((
            ".test.js", ".test.ts", ".test.jsx", ".test.tsx",
            ".spec.js", ".spec.ts", ".spec.jsx", ".spec.tsx",
        )):
            return True
        basename = path_lower.split("/")[-1]
        if basename.startswith("test_") and basename.endswith(".py"):
            return True

    return False


def _detect_docker(file_paths, js_deps, py_deps_text, get_content):
    """Dockerfile, docker-compose.yml, docker-compose.yaml."""
    compose_names = {
        "docker-compose.yml", "docker-compose.yaml",
        "docker-compose.override.yml", "compose.yml", "compose.yaml",
    }
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        basename = path_lower.split("/")[-1]
        if path_lower == "dockerfile" or path_lower.endswith("/dockerfile"):
            return True
        if basename in compose_names or "docker-compose" in basename:
            return True
        if path_lower == ".dockerignore":
            return True
    return False


def _detect_cicd(file_paths, js_deps, py_deps_text, get_content):
    """GitHub Actions workflows under .github/workflows/."""
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if path_lower.startswith(".github/workflows/"):
            return True
    return False


def _detect_environment_variables(file_paths, js_deps, py_deps_text, get_content):
    """.env.example, .env files, dotenv packages."""
    env_files = {
        ".env", ".env.example", ".env.local", ".env.development",
        ".env.production", ".env.test", ".env.sample",
    }
    for path in file_paths:
        basename = path.lower().replace("\\", "/").split("/")[-1]
        if basename in env_files:
            return True

    if "dotenv" in js_deps or "@nestjs/config" in js_deps:
        return True

    if "python-dotenv" in py_deps_text or "python-decouple" in py_deps_text:
        return True

    return False


# ===================================================================
#  DETECTOR REGISTRY — add new features here
# ===================================================================

FEATURE_DETECTORS = {
    "authentication":         _detect_authentication,
    "database":               _detect_database,
    "api_layer":              _detect_api_layer,
    "testing":                _detect_testing,
    "docker":                 _detect_docker,
    "cicd":                   _detect_cicd,
    "environment_variables":  _detect_environment_variables,
}


# ===================================================================
#  PUBLIC API
# ===================================================================

def detect_features(file_paths: list, owner: str, repo: str) -> dict:
    """
    Runs every registered feature detector against the repository.
    Returns a dict of { feature_name: bool }.
    """
    get_content = _build_content_fetcher(owner, repo)

    # Pre-parse shared dependency data once for all detectors
    js_deps = _parse_js_deps(get_content)
    py_deps_text = _collect_python_deps(file_paths, get_content)

    features = {}
    for name, detector in FEATURE_DETECTORS.items():
        try:
            features[name] = detector(file_paths, js_deps, py_deps_text, get_content)
        except Exception:
            features[name] = False

    return features
