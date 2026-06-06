"""
Project type registry — category-based scoring weights, labels, and recommendations.

Each project type defines its own feature keys and point values (max 100).
"""

from typing import TypedDict


class RecommendationRule(TypedDict):
    title: str


PROJECT_TYPES: tuple[str, ...] = (
    "Web Application",
    "Machine Learning",
    "Data Science",
    "Mobile App",
    "Backend API",
)

DEFAULT_PROJECT_TYPE = "Web Application"
MAX_SCORE = 100

# ---------------------------------------------------------------------------
# Feature labels per project type
# ---------------------------------------------------------------------------

FEATURE_LABELS_BY_TYPE: dict[str, dict[str, str]] = {
    "Web Application": {
        "authentication": "Authentication",
        "database": "Database",
        "api_layer": "API Layer",
        "testing": "Testing",
        "docker": "Docker",
        "cicd": "CI/CD",
        "environment_variables": "Environment Variables",
    },
    "Backend API": {
        "api_layer": "API Layer",
        "authentication": "Authentication",
        "database": "Database",
        "testing": "Testing",
        "docker": "Docker",
        "cicd": "CI/CD",
    },
    "Mobile App": {
        "authentication": "Authentication",
        "api_integration": "API Integration",
        "local_storage": "Local Storage",
        "database": "Database",
        "testing": "Testing",
        "cicd": "CI/CD",
        "documentation": "Documentation",
    },
    "Machine Learning": {
        "dataset": "Dataset",
        "model_files": "Model Files",
        "evaluation_metrics": "Evaluation Metrics",
        "documentation": "Documentation",
        "requirements_file": "Requirements File",
        "deployment": "Deployment",
    },
    "Data Science": {
        "dataset": "Dataset",
        "eda_notebook": "EDA Notebook",
        "visualizations": "Visualizations",
        "documentation": "Documentation",
        "requirements_file": "Requirements File",
        "insights_reports": "Insights/Reports",
    },
}

# ---------------------------------------------------------------------------
# Scoring weights per project type (each sums to 100)
# ---------------------------------------------------------------------------

SCORE_WEIGHTS_BY_TYPE: dict[str, dict[str, int]] = {
    "Web Application": {
        "authentication": 20,
        "database": 20,
        "api_layer": 15,
        "testing": 15,
        "docker": 10,
        "cicd": 10,
        "environment_variables": 10,
    },
    "Backend API": {
        "api_layer": 25,
        "authentication": 20,
        "database": 20,
        "testing": 15,
        "docker": 10,
        "cicd": 10,
    },
    "Mobile App": {
        "authentication": 20,
        "api_integration": 20,
        "local_storage": 15,
        "database": 15,
        "testing": 10,
        "cicd": 10,
        "documentation": 10,
    },
    "Machine Learning": {
        "dataset": 20,
        "model_files": 20,
        "evaluation_metrics": 20,
        "documentation": 15,
        "requirements_file": 10,
        "deployment": 15,
    },
    "Data Science": {
        "dataset": 20,
        "eda_notebook": 20,
        "visualizations": 20,
        "documentation": 15,
        "requirements_file": 10,
        "insights_reports": 15,
    },
}

# ---------------------------------------------------------------------------
# Recommendation copy per project type
# ---------------------------------------------------------------------------

RECOMMENDATION_RULES_BY_TYPE: dict[str, dict[str, RecommendationRule]] = {
    "Web Application": {
        "authentication": {"title": "Implement JWT or OAuth authentication for users"},
        "database": {"title": "Integrate PostgreSQL or MongoDB for persistent data"},
        "api_layer": {"title": "Add a REST or GraphQL API layer"},
        "testing": {"title": "Add frontend and backend tests with Jest or pytest"},
        "docker": {"title": "Containerize the application using Docker"},
        "cicd": {"title": "Configure GitHub Actions for automated deploys"},
        "environment_variables": {"title": "Move secrets and config into .env files"},
    },
    "Backend API": {
        "api_layer": {"title": "Define RESTful routes with FastAPI or Express"},
        "authentication": {"title": "Implement JWT Authentication for API consumers"},
        "database": {"title": "Integrate PostgreSQL or MongoDB as the data layer"},
        "testing": {"title": "Add API integration tests with pytest or jest"},
        "docker": {"title": "Containerize the API using Docker"},
        "cicd": {"title": "Configure GitHub Actions for API deployment"},
    },
    "Mobile App": {
        "authentication": {"title": "Implement secure login with JWT or OAuth"},
        "api_integration": {"title": "Connect to backend APIs for data sync"},
        "local_storage": {"title": "Add local storage with AsyncStorage or SQLite"},
        "database": {"title": "Integrate Firebase, Supabase, or a mobile database"},
        "testing": {"title": "Add unit and integration tests for app logic"},
        "cicd": {"title": "Set up CI/CD for automated builds and releases"},
        "documentation": {"title": "Add README and setup documentation"},
    },
    "Machine Learning": {
        "dataset": {"title": "Include a structured dataset in data/ or datasets/"},
        "model_files": {"title": "Add trained model artifacts (.pkl, .pt, .h5)"},
        "evaluation_metrics": {"title": "Implement model evaluation with accuracy, F1, or RMSE"},
        "documentation": {"title": "Document model architecture and training steps"},
        "requirements_file": {"title": "Add requirements.txt or environment.yml"},
        "deployment": {"title": "Deploy models via Docker, FastAPI, or Gradio"},
    },
    "Data Science": {
        "dataset": {"title": "Include raw or processed datasets for analysis"},
        "eda_notebook": {"title": "Add Jupyter notebooks for exploratory data analysis"},
        "visualizations": {"title": "Include charts with matplotlib, seaborn, or plotly"},
        "documentation": {"title": "Document data sources and methodology in README"},
        "requirements_file": {"title": "Add requirements.txt for reproducible environments"},
        "insights_reports": {"title": "Publish analysis reports or findings summaries"},
    },
}


def normalize_project_type(project_type: str | None) -> str:
    if not project_type:
        return DEFAULT_PROJECT_TYPE
    if project_type not in PROJECT_TYPES:
        raise ValueError(
            f"Invalid project_type '{project_type}'. "
            f"Must be one of: {', '.join(PROJECT_TYPES)}"
        )
    return project_type


def get_feature_labels(project_type: str) -> dict[str, str]:
    normalized = normalize_project_type(project_type)
    return FEATURE_LABELS_BY_TYPE[normalized]


def get_score_weights(project_type: str) -> dict[str, int]:
    normalized = normalize_project_type(project_type)
    return SCORE_WEIGHTS_BY_TYPE[normalized]


def get_recommendation_rules(project_type: str) -> dict[str, RecommendationRule]:
    normalized = normalize_project_type(project_type)
    return RECOMMENDATION_RULES_BY_TYPE[normalized]
