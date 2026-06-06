"""
Category-specific feature detectors for Mobile, ML, and Data Science projects.

Web Application and Backend API reuse standard detectors from feature_analyzer.
"""

import json

from analyzers.feature_analyzer import (
    FEATURE_DETECTORS as STANDARD_DETECTORS,
    _build_content_fetcher,
    _collect_python_deps,
    _parse_js_deps,
)
from analyzers.project_types import get_feature_labels, normalize_project_type

# ---------------------------------------------------------------------------
# Shared category detector helpers
# ---------------------------------------------------------------------------

_DATA_EXTENSIONS = (".csv", ".tsv", ".parquet", ".json", ".jsonl", ".xlsx", ".feather")
_MODEL_EXTENSIONS = (".pkl", ".pickle", ".joblib", ".h5", ".hdf5", ".pt", ".pth", ".onnx", ".pb", ".safetensors")
_DOC_FILES = {"readme.md", "readme.rst", "readme.txt", "contributing.md", "changelog.md"}


def _path_has_any(path_lower: str, markers: tuple[str, ...]) -> bool:
    return any(m in path_lower for m in markers)


def _detect_documentation(file_paths, js_deps, py_deps_text, get_content):
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        basename = path_lower.split("/")[-1]
        if basename in _DOC_FILES:
            return True
        if path_lower.startswith("docs/") or "/docs/" in path_lower:
            return True
    readme = get_content("README.md") or get_content("readme.md")
    return bool(readme and len(readme.strip()) > 50)


def _detect_dataset(file_paths, js_deps, py_deps_text, get_content):
    data_dirs = ("data/", "dataset/", "datasets/", "raw_data/", "processed/")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if any(path_lower.startswith(d) or f"/{d}" in path_lower for d in data_dirs):
            return True
        if path_lower.endswith(_DATA_EXTENSIONS):
            return True
    return False


def _detect_requirements_file(file_paths, js_deps, py_deps_text, get_content):
    req_markers = (
        "requirements.txt", "requirements-dev.txt", "environment.yml",
        "environment.yaml", "conda.yml", "pyproject.toml", "pipfile", "setup.py",
    )
    for path in file_paths:
        basename = path.lower().replace("\\", "/").split("/")[-1]
        if basename in req_markers:
            return True
    return False


# ---------------------------------------------------------------------------
# Mobile App detectors
# ---------------------------------------------------------------------------

def _detect_api_integration(file_paths, js_deps, py_deps_text, get_content):
    js_api = {
        "axios", "@tanstack/react-query", "react-query", "swr",
        "@reduxjs/toolkit", "apollo-client", "@apollo/client",
    }
    if js_deps & js_api:
        return True

    mobile_api = {
        "retrofit", "dio", "http", "chopper", "graphql_flutter",
        "react-native-config", "@react-native-community/netinfo",
    }
    if js_deps & mobile_api:
        return True

    api_keywords = ("api", "client", "service", "endpoint")
    code_ext = (".js", ".ts", ".jsx", ".tsx", ".dart", ".kt", ".swift")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if path_lower.endswith(code_ext):
            basename = path_lower.split("/")[-1]
            if any(kw in basename for kw in api_keywords):
                return True
            if "/services/" in path_lower or "/api/" in path_lower:
                return True
    return False


def _detect_local_storage(file_paths, js_deps, py_deps_text, get_content):
    js_storage = {
        "@react-native-async-storage/async-storage", "async-storage",
        "react-native-mmkv", "@react-native-community/async-storage",
        "expo-secure-store", "react-native-keychain",
        "localforage", "idb", "dexie",
    }
    if js_deps & js_storage:
        return True

    storage_keywords = ("storage", "cache", "preferences", "securestore", "keychain")
    mobile_ext = (".js", ".ts", ".jsx", ".tsx", ".dart", ".kt", ".swift")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if path_lower.endswith(mobile_ext):
            basename = path_lower.split("/")[-1]
            if any(kw in basename for kw in storage_keywords):
                return True
        if "sharedpreferences" in path_lower or "userdefaults" in path_lower:
            return True
    return False


MOBILE_DETECTORS = {
    "authentication": STANDARD_DETECTORS["authentication"],
    "api_integration": _detect_api_integration,
    "local_storage": _detect_local_storage,
    "database": STANDARD_DETECTORS["database"],
    "testing": STANDARD_DETECTORS["testing"],
    "cicd": STANDARD_DETECTORS["cicd"],
    "documentation": _detect_documentation,
}

# ---------------------------------------------------------------------------
# Machine Learning detectors
# ---------------------------------------------------------------------------

def _detect_model_files(file_paths, js_deps, py_deps_text, get_content):
    model_dirs = ("models/", "model/", "checkpoints/", "weights/", "saved_models/")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if any(path_lower.startswith(d) or f"/{d}" in path_lower for d in model_dirs):
            return True
        if path_lower.endswith(_MODEL_EXTENSIONS):
            return True
    ml_libs = ["tensorflow", "torch", "pytorch", "keras", "sklearn", "scikit-learn", "xgboost", "lightgbm"]
    return any(lib in py_deps_text for lib in ml_libs) and _path_has_any(
        "\n".join(file_paths).lower(), ("train", "model", "predict")
    )


def _detect_evaluation_metrics(file_paths, js_deps, py_deps_text, get_content):
    metric_keywords = (
        "accuracy", "f1_score", "precision", "recall", "roc_auc", "rmse", "mae",
        "confusion_matrix", "classification_report", "cross_val_score",
    )
    if any(kw in py_deps_text for kw in ("sklearn", "scikit-learn", "tensorflow", "torch")):
        for path in file_paths:
            if path.endswith((".py", ".ipynb")):
                content = get_content(path)
                if content and any(kw in content.lower() for kw in metric_keywords):
                    return True
    for path in file_paths:
        path_lower = path.lower()
        if "eval" in path_lower or "metric" in path_lower:
            if path_lower.endswith((".py", ".ipynb", ".js")):
                return True
    return False


def _detect_deployment(file_paths, js_deps, py_deps_text, get_content):
    if STANDARD_DETECTORS["docker"](file_paths, js_deps, py_deps_text, get_content):
        return True
    deploy_libs = ["gradio", "streamlit", "fastapi", "flask", "bentoml", "mlflow", "seldon-core"]
    if any(lib in py_deps_text for lib in deploy_libs):
        return True
    deploy_paths = ("serve", "inference", "deploy", "app.py", "main.py", "api.py")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        basename = path_lower.split("/")[-1]
        if basename in deploy_paths and path_lower.endswith(".py"):
            return True
    return False


ML_DETECTORS = {
    "dataset": _detect_dataset,
    "model_files": _detect_model_files,
    "evaluation_metrics": _detect_evaluation_metrics,
    "documentation": _detect_documentation,
    "requirements_file": _detect_requirements_file,
    "deployment": _detect_deployment,
}

# ---------------------------------------------------------------------------
# Data Science detectors
# ---------------------------------------------------------------------------

def _detect_eda_notebook(file_paths, js_deps, py_deps_text, get_content):
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if path_lower.endswith(".ipynb"):
            return True
        if "/notebooks/" in path_lower or path_lower.startswith("notebooks/"):
            return True
    return False


def _detect_visualizations(file_paths, js_deps, py_deps_text, get_content):
    viz_libs = [
        "matplotlib", "seaborn", "plotly", "bokeh", "altair",
        "ggplot", "dash", "streamlit", "pygal",
    ]
    if any(lib in py_deps_text for lib in viz_libs):
        return True
    viz_js = {"chart.js", "recharts", "d3", "plotly.js", "echarts", "highcharts"}
    if js_deps & viz_js:
        return True
    for path in file_paths:
        if path.endswith((".py", ".ipynb", ".r", ".R")):
            content = get_content(path)
            if content and any(lib in content.lower() for lib in ("plt.", "sns.", "plotly", "ggplot")):
                return True
    return False


def _detect_insights_reports(file_paths, js_deps, py_deps_text, get_content):
    report_dirs = ("reports/", "report/", "output/", "outputs/", "findings/", "analysis/", "results/")
    report_ext = (".pdf", ".html", ".md", ".docx")
    for path in file_paths:
        path_lower = path.lower().replace("\\", "/")
        if any(path_lower.startswith(d) or f"/{d}" in path_lower for d in report_dirs):
            return True
        basename = path_lower.split("/")[-1]
        if basename.endswith(report_ext) and any(kw in basename for kw in ("report", "analysis", "insight", "finding")):
            return True
    return False


DS_DETECTORS = {
    "dataset": _detect_dataset,
    "eda_notebook": _detect_eda_notebook,
    "visualizations": _detect_visualizations,
    "documentation": _detect_documentation,
    "requirements_file": _detect_requirements_file,
    "insights_reports": _detect_insights_reports,
}

# ---------------------------------------------------------------------------
# Registry: project type -> detector map
# ---------------------------------------------------------------------------

WEB_DETECTORS = {k: STANDARD_DETECTORS[k] for k in (
    "authentication", "database", "api_layer", "testing",
    "docker", "cicd", "environment_variables",
)}

BACKEND_API_DETECTORS = {k: STANDARD_DETECTORS[k] for k in (
    "api_layer", "authentication", "database", "testing", "docker", "cicd",
)}

DETECTORS_BY_TYPE = {
    "Web Application": WEB_DETECTORS,
    "Backend API": BACKEND_API_DETECTORS,
    "Mobile App": MOBILE_DETECTORS,
    "Machine Learning": ML_DETECTORS,
    "Data Science": DS_DETECTORS,
}


def detect_category_features(
    file_paths: list,
    owner: str,
    repo: str,
    project_type: str | None = None,
) -> dict:
    """
    Run category-specific feature detectors for the given project type.
    Returns { feature_key: bool } for all features in that category.
    """
    normalized = normalize_project_type(project_type)
    detectors = DETECTORS_BY_TYPE[normalized]
    expected_keys = set(get_feature_labels(normalized).keys())

    get_content = _build_content_fetcher(owner, repo)
    js_deps = _parse_js_deps(get_content)
    py_deps_text = _collect_python_deps(file_paths, get_content)

    features = {}
    for name in expected_keys:
        detector = detectors.get(name)
        if not detector:
            features[name] = False
            continue
        try:
            features[name] = detector(file_paths, js_deps, py_deps_text, get_content)
        except Exception:
            features[name] = False

    return features
