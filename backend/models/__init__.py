"""
SQLAlchemy models package.

Import all models here so they register with Base.metadata before create_all().
"""

from models.analysis_history import AnalysisHistory
from models.user import User

__all__ = ["AnalysisHistory", "User"]
