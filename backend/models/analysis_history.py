from sqlalchemy import Column, DateTime, Integer, JSON, String, Text, func

from database.database import Base


class AnalysisHistory(Base):
    """Stores each repository analysis result."""

    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String(512), nullable=False, index=True)
    repo_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String(100), nullable=True)
    stars = Column(Integer, nullable=True, default=0)
    forks = Column(Integer, nullable=True, default=0)
    score = Column(Integer, nullable=False, default=0)
    maturity = Column(String(50), nullable=True)
    potential_score = Column(Integer, nullable=True)
    technologies = Column(JSON, nullable=True)
    features = Column(JSON, nullable=True)
    evaluation = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
