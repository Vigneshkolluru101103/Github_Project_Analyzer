"""
Capability registry — project evaluation is based on capabilities, not individual technologies.
"""

from dataclasses import dataclass
from typing import TypedDict


class RecommendationRule(TypedDict):
    title: str


PROJECT_TYPES: tuple[str, ...] = (
    "Web Application",
    "Backend API",
    "Mobile App",
    "Machine Learning",
    "Data Science",
)

DEFAULT_PROJECT_TYPE = "Web Application"
MAX_SCORE = 100

_SCAN_EXTENSIONS = (
    ".py", ".js", ".ts", ".jsx", ".tsx", ".ipynb", ".java", ".kt",
    ".dart", ".swift", ".go", ".rb", ".rs", ".cs",
)


@dataclass(frozen=True)
class CapabilitySpec:
    key: str
    label: str
    weight: int
    recommendation: str
    js_packages: tuple[str, ...] = ()
    py_packages: tuple[str, ...] = ()
    tech_names: tuple[str, ...] = ()
    path_markers: tuple[str, ...] = ()
    file_extensions: tuple[str, ...] = ()
    filename_keywords: tuple[str, ...] = ()
    folder_segments: tuple[str, ...] = ()
    import_patterns: tuple[str, ...] = ()
    content_keywords: tuple[str, ...] = ()
    scan_extensions: tuple[str, ...] = _SCAN_EXTENSIONS


CAPABILITIES_BY_TYPE: dict[str, tuple[CapabilitySpec, ...]] = {
    "Web Application": (
        CapabilitySpec(
            key="frontend_framework",
            label="Frontend Framework",
            weight=20,
            recommendation="Add a frontend framework layer",
            js_packages=("react", "react-dom", "next", "vue", "@angular/core", "svelte", "@sveltejs/kit"),
            tech_names=("React", "Next.js", "Vue.js", "Svelte"),
            path_markers=("vite.config", "next.config", "angular.json", "svelte.config"),
            import_patterns=("from 'react'", 'from "react"', "from 'next'", "from 'vue'", "@angular/core"),
        ),
        CapabilitySpec(
            key="backend_framework",
            label="Backend Framework",
            weight=20,
            recommendation="Add a backend framework layer",
            js_packages=("express", "fastify", "koa", "@nestjs/core"),
            py_packages=("fastapi", "flask", "django", "uvicorn", "gunicorn"),
            tech_names=("FastAPI", "Flask", "Django", "Express"),
            path_markers=("spring", "pom.xml", "build.gradle", "routes/", "routers/"),
            filename_keywords=("app.py", "main.py", "server.js", "wsgi.py", "asgi.py"),
            import_patterns=("from fastapi", "import fastapi", "from flask", "import flask", "from django", "import express"),
        ),
        CapabilitySpec(
            key="database",
            label="Database",
            weight=20,
            recommendation="Add a database layer",
            js_packages=(
                "pg", "mysql2", "mongoose", "mongodb", "@prisma/client", "prisma",
                "firebase", "@supabase/supabase-js", "better-sqlite3", "sequelize", "typeorm",
            ),
            py_packages=(
                "sqlalchemy", "psycopg2", "asyncpg", "pymongo", "mysqlclient",
                "pymysql", "sqlite3", "firebase-admin", "supabase", "alembic", "peewee",
            ),
            tech_names=("PostgreSQL", "MySQL", "MongoDB", "Prisma", "Redis"),
            path_markers=("schema.prisma", "firebase.json", "supabase/", "migrations/", ".sql"),
            import_patterns=(
                "import sqlalchemy", "from sqlalchemy", "import psycopg2", "from prisma",
                "import mongoose", "from pymongo", "import mysql", "import sqlite3",
            ),
            content_keywords=("mongodb://", "postgresql://", "mysql://", "create_engine(", "mongoose.connect"),
        ),
        CapabilitySpec(
            key="authentication",
            label="Authentication",
            weight=20,
            recommendation="Add an authentication layer",
            js_packages=(
                "jsonwebtoken", "jwt-decode", "passport", "passport-jwt", "next-auth",
                "@clerk/nextjs", "@auth0/nextjs-auth0", "firebase-admin",
                "@supabase/auth-helpers-nextjs", "@supabase/auth-ui-react",
            ),
            py_packages=(
                "pyjwt", "python-jose", "jose", "passlib", "bcrypt", "authlib",
                "django-allauth", "flask-jwt-extended", "flask-login", "oauthlib",
            ),
            filename_keywords=("auth", "login", "signup", "signin", "register", "authenticate"),
            folder_segments=("auth", "authentication"),
            import_patterns=(
                "import jwt", "from jose", "import passport", "from clerk", "auth0",
                "firebase.auth", "flask_login", "flask_jwt",
            ),
            content_keywords=(
                "jwt", "oauth", "bearer token", "clerk", "auth0", "firebase auth",
                "authenticate", "login_user", "verify_password", "decode_token",
            ),
        ),
        CapabilitySpec(
            key="testing",
            label="Testing",
            weight=20,
            recommendation="Add an automated testing layer",
            js_packages=("jest", "vitest", "cypress", "@playwright/test", "@testing-library/react", "mocha", "chai"),
            py_packages=("pytest", "unittest", "nose", "coverage", "tox"),
            folder_segments=("tests", "test", "__tests__", "spec"),
            path_markers=("/tests/", "/test/", "/__tests__/", "/spec/"),
            file_extensions=(".test.js", ".test.ts", ".test.jsx", ".test.tsx", ".spec.js", ".spec.ts", ".spec.jsx"),
            filename_keywords=("test_", "conftest.py", "_test.py", "_spec."),
            import_patterns=("import pytest", "import unittest", "from jest", "from vitest", "from playwright"),
            content_keywords=("describe(", "it(", "test(", "@pytest", "expect(", "assert "),
        ),
    ),
    "Backend API": (
        CapabilitySpec(
            key="backend_framework",
            label="Backend Framework",
            weight=25,
            recommendation="Add a backend API framework",
            js_packages=("express", "fastify", "koa", "@nestjs/core", "@hapi/hapi"),
            py_packages=("fastapi", "flask", "djangorestframework", "django-ninja", "starlette", "sanic"),
            tech_names=("FastAPI", "Flask", "Django", "Express"),
            path_markers=("routes/", "routers/", "controllers/", "endpoints/", "api/", "spring"),
            import_patterns=("from fastapi", "import fastapi", "from flask", "import express", "from rest_framework"),
        ),
        CapabilitySpec(
            key="database",
            label="Database",
            weight=25,
            recommendation="Add a database layer",
            js_packages=("pg", "mysql2", "mongoose", "mongodb", "ioredis", "redis", "@prisma/client", "sequelize"),
            py_packages=("sqlalchemy", "psycopg2", "asyncpg", "pymongo", "redis", "mysqlclient", "motor", "alembic"),
            tech_names=("PostgreSQL", "MySQL", "MongoDB", "Redis", "Prisma"),
            path_markers=("migrations/", "schema.prisma", ".sql"),
            import_patterns=("import sqlalchemy", "from sqlalchemy", "import psycopg2", "import redis", "from pymongo"),
        ),
        CapabilitySpec(
            key="authentication",
            label="Authentication",
            weight=20,
            recommendation="Add API authentication",
            js_packages=("jsonwebtoken", "passport", "passport-jwt", "express-session", "cookie-session"),
            py_packages=("pyjwt", "python-jose", "passlib", "flask-jwt-extended", "djangorestframework-simplejwt"),
            filename_keywords=("auth", "login", "authenticate"),
            import_patterns=("import jwt", "from jose", "passport", "session"),
            content_keywords=("jwt", "oauth", "bearer", "session", "authenticate", "authorization"),
        ),
        CapabilitySpec(
            key="api_documentation",
            label="API Documentation",
            weight=15,
            recommendation="Add API documentation",
            path_markers=("openapi", "swagger", "redoc", "/docs", "openapi.json", "openapi.yaml"),
            filename_keywords=("openapi.json", "openapi.yaml", "openapi.yml", "swagger.json", "swagger.yaml", "redoc"),
            py_packages=("drf-spectacular", "flasgger"),
            content_keywords=(
                "swagger", "openapi", "redoc", "fastapi.docs", "swagger_ui",
                "openapi_tags", "generate_openapi", "/docs",
            ),
            import_patterns=("from drf_spectacular", "import flasgger"),
        ),
        CapabilitySpec(
            key="testing",
            label="Testing",
            weight=15,
            recommendation="Add API testing",
            js_packages=("jest", "supertest", "mocha", "chai", "vitest"),
            py_packages=("pytest", "unittest", "httpx", "requests-mock"),
            folder_segments=("tests", "test", "__tests__"),
            path_markers=("/tests/", "/test/"),
            file_extensions=(".test.js", ".test.ts", ".spec.js", ".spec.ts"),
            filename_keywords=("test_", "conftest.py"),
            import_patterns=("import pytest", "import unittest", "from fastapi.testclient"),
            content_keywords=("testclient", "assert response", "@pytest"),
        ),
    ),
    "Mobile App": (
        CapabilitySpec(
            key="mobile_framework",
            label="Mobile Framework",
            weight=25,
            recommendation="Add a mobile application framework",
            js_packages=("react-native", "expo", "@react-native-community/cli"),
            path_markers=("pubspec.yaml", "android/", "ios/", ".xcodeproj", ".xcworkspace", "build.gradle"),
            file_extensions=(".dart", ".kt", ".java", ".swift", ".m", ".h"),
            filename_keywords=("main.dart", "appdelegate.swift", "mainactivity.kt", "app.gradle"),
            import_patterns=("import 'package:flutter", "from 'react-native'", "import androidx", "import UIKit"),
        ),
        CapabilitySpec(
            key="authentication",
            label="Authentication",
            weight=20,
            recommendation="Add mobile authentication",
            js_packages=("firebase", "@react-native-firebase/auth", "expo-auth-session", "@clerk/clerk-expo"),
            filename_keywords=("auth", "login", "signin", "signup"),
            import_patterns=("firebase.auth", "FirebaseAuth", "expo-auth-session"),
            content_keywords=("jwt", "oauth", "firebase auth", "signin", "authenticate"),
        ),
        CapabilitySpec(
            key="storage",
            label="Storage",
            weight=20,
            recommendation="Add on-device storage",
            js_packages=(
                "@react-native-async-storage/async-storage", "react-native-mmkv",
                "expo-secure-store", "react-native-sqlite-storage",
            ),
            path_markers=("hive", "room/", "sqlite"),
            filename_keywords=("databasehelper", "sharedpreferences", "roomdatabase", ".db", ".sqlite"),
            folder_segments=("storage", "database"),
            content_keywords=("sqlite", "hive", "sharedpreferences", "room.database", "asyncstorage", "mmkv"),
            import_patterns=("import sqlite3", "AsyncStorage", "Hive", "Room.database"),
        ),
        CapabilitySpec(
            key="api_integration",
            label="API Integration",
            weight=20,
            recommendation="Add backend API integration",
            js_packages=("axios", "@apollo/client", "graphql", "@tanstack/react-query", "urql"),
            path_markers=("/api/", "/services/", "/graphql", "/clients/"),
            filename_keywords=("api.ts", "api.js", "api.dart", "graphql", "client.ts", "client.js"),
            content_keywords=("graphql", "rest api", "fetch(", "axios", "http.get", "dio."),
            import_patterns=("import axios", "from '@apollo/client'", "import graphql", "package:http/http.dart"),
        ),
        CapabilitySpec(
            key="testing",
            label="Testing",
            weight=15,
            recommendation="Add mobile app testing",
            js_packages=("jest", "@testing-library/react-native", "detox"),
            folder_segments=("test", "tests", "__tests__"),
            filename_keywords=("_test.dart", "test.dart", "test_"),
            content_keywords=("flutter_test", "junit", "@test", "describe(", "testwidgets", "expect("),
            import_patterns=("import 'package:flutter_test", "import org.junit", "@Test"),
        ),
    ),
    "Machine Learning": (
        CapabilitySpec(
            key="ml_framework",
            label="ML Framework",
            weight=25,
            recommendation="Add a machine learning framework",
            py_packages=("tensorflow", "torch", "pytorch", "scikit-learn", "sklearn", "xgboost", "lightgbm", "keras"),
            tech_names=("TensorFlow", "PyTorch", "Pandas", "NumPy"),
            import_patterns=(
                "import tensorflow", "import torch", "from torch", "import keras",
                "from sklearn", "import sklearn", "import xgboost", "import lightgbm",
            ),
            content_keywords=("fit(", "predict(", "train_model", "model.compile", "model.fit"),
        ),
        CapabilitySpec(
            key="dataset",
            label="Dataset",
            weight=20,
            recommendation="Add structured datasets",
            folder_segments=("data", "dataset", "datasets", "raw_data", "processed", "raw", "input"),
            path_markers=("data/", "dataset/", "datasets/", "raw_data/", "processed/"),
            file_extensions=(".csv", ".tsv", ".xlsx", ".xls", ".json", ".jsonl", ".parquet", ".feather", ".npy", ".npz"),
            content_keywords=(
                "pd.read_csv(", "pd.read_excel(", "read_csv(", "read_excel(",
                "load_dataset(", "dataset.from_", "datasets.load", "np.load(",
                "pd.read_json(", "read_parquet(",
            ),
            import_patterns=("from datasets import", "import datasets", "from torchvision.datasets"),
        ),
        CapabilitySpec(
            key="model",
            label="Model",
            weight=20,
            recommendation="Add trained model artifacts",
            path_markers=("models/", "model/", "checkpoints/", "weights/", "saved_models/", "saved_model/"),
            file_extensions=(".pkl", ".pickle", ".joblib", ".h5", ".hdf5", ".pt", ".pth", ".onnx", ".pb", ".safetensors"),
            filename_keywords=("model.pkl", "model.joblib", "model.h5", "model.pt", "model.pth", "saved_model", "best_model", "checkpoint"),
            import_patterns=(
                "import sklearn", "from sklearn", "import tensorflow", "import keras",
                "import torch", "from torch", "joblib.load", "pickle.load", "load_model(",
            ),
            content_keywords=("torch.save", "model.save", "joblib.dump", "pickle.dump", "save_model("),
        ),
        CapabilitySpec(
            key="evaluation",
            label="Evaluation",
            weight=20,
            recommendation="Add model evaluation metrics",
            filename_keywords=("eval", "metrics", "evaluate", "evaluation"),
            folder_segments=("evaluation", "metrics"),
            path_markers=("/evaluation/", "/metrics/"),
            content_keywords=(
                "accuracy_score", "precision_score", "recall_score", "f1_score",
                "confusion_matrix", "classification_report", "roc_auc_score",
                "mean_squared_error", "r2_score", "mean_absolute_error",
                "log_loss", "balanced_accuracy_score",
            ),
            import_patterns=(
                "from sklearn.metrics", "import sklearn.metrics",
                "tensorflow.keras.metrics", "torchmetrics",
            ),
        ),
        CapabilitySpec(
            key="documentation",
            label="Documentation",
            weight=15,
            recommendation="Add project documentation",
            path_markers=("docs/", "documentation/"),
            filename_keywords=("readme.md", "readme.rst", "model_card", "modelcard"),
            folder_segments=("docs", "documentation"),
        ),
    ),
    "Data Science": (
        CapabilitySpec(
            key="data_processing",
            label="Data Processing",
            weight=25,
            recommendation="Add data processing libraries",
            py_packages=("pandas", "numpy", "scipy", "polars", "dask", "pyarrow"),
            tech_names=("Pandas", "NumPy"),
            import_patterns=("import pandas", "import numpy", "import scipy", "import polars", "from pandas"),
            content_keywords=("pd.read_csv(", "pd.merge(", "pd.groupby(", "np.array(", "df.drop(", "df.fillna("),
        ),
        CapabilitySpec(
            key="visualization",
            label="Visualization",
            weight=25,
            recommendation="Add data visualization",
            py_packages=("matplotlib", "seaborn", "plotly", "altair", "bokeh"),
            js_packages=("chart.js", "recharts", "plotly.js", "d3", "echarts"),
            import_patterns=("import matplotlib", "import seaborn", "import plotly", "from plotly", "import altair"),
            content_keywords=("plt.", "sns.", "plotly", "ggplot", ".plot(", "px.bar(", "px.scatter(", "fig.show("),
            filename_keywords=(".pbix", ".twb", ".twbx"),
        ),
        CapabilitySpec(
            key="dataset",
            label="Dataset",
            weight=20,
            recommendation="Add datasets for analysis",
            folder_segments=("data", "dataset", "datasets", "raw", "input"),
            path_markers=("data/", "dataset/", "datasets/"),
            file_extensions=(".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"),
            content_keywords=("pd.read_csv(", "pd.read_excel(", "read_csv(", "read_excel(", "read_parquet("),
        ),
        CapabilitySpec(
            key="eda",
            label="EDA",
            weight=15,
            recommendation="Add exploratory data analysis",
            file_extensions=(".ipynb",),
            folder_segments=("notebooks", "notebook", "eda", "analysis"),
            path_markers=("notebooks/", "/notebook/", "/eda/", "/analysis/"),
            filename_keywords=("eda", "exploratory", "analysis.ipynb", "notebook"),
            content_keywords=(
                "exploratory data analysis", "df.describe()", "df.info()", "df.head()",
                "value_counts(", "corr(", "pairplot", "heatmap",
            ),
        ),
        CapabilitySpec(
            key="documentation",
            label="Documentation",
            weight=15,
            recommendation="Add documentation and reports",
            path_markers=("reports/", "report/", "findings/", "docs/", "outputs/"),
            filename_keywords=("readme.md", "report", "analysis", "insights", "findings"),
            folder_segments=("reports", "report", "findings", "docs"),
            file_extensions=(".md", ".pdf", ".html", ".docx"),
        ),
    ),
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


def get_capabilities(project_type: str) -> tuple[CapabilitySpec, ...]:
    return CAPABILITIES_BY_TYPE[normalize_project_type(project_type)]


def get_capability_labels(project_type: str) -> dict[str, str]:
    return {spec.key: spec.label for spec in get_capabilities(project_type)}


def get_score_weights(project_type: str) -> dict[str, int]:
    return {spec.key: spec.weight for spec in get_capabilities(project_type)}


def get_recommendation_rules(project_type: str) -> dict[str, RecommendationRule]:
    return {spec.key: {"title": spec.recommendation} for spec in get_capabilities(project_type)}
