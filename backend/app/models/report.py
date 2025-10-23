"""Report model."""
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReportStatus(str, Enum):
    """Report generation status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(Base):
    """Prospect report model."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)

    # Input data
    prospect_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    additional_context = Column(Text, nullable=True)

    # Status
    status = Column(String, default=ReportStatus.PENDING)
    error_message = Column(Text, nullable=True)

    # Generated data (stored as JSON)
    company_data = Column(JSON, nullable=True)
    person_data = Column(JSON, nullable=True)
    news_data = Column(JSON, nullable=True)
    ai_insights = Column(JSON, nullable=True)

    # Report content
    talking_points = Column(JSON, nullable=True)  # List of talking points
    conversation_starters = Column(JSON, nullable=True)  # List of 3-5 starters
    personality_analysis = Column(Text, nullable=True)
    recommended_approach = Column(Text, nullable=True)

    # Metadata
    generation_time_seconds = Column(Integer, nullable=True)
    pdf_path = Column(String, nullable=True)
    docx_path = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
