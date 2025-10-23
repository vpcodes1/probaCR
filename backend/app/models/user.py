"""User model."""
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SubscriptionTier(str, Enum):
    """Subscription tiers."""

    FREE = "free"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Subscription
    subscription_tier = Column(String, default=SubscriptionTier.FREE)
    reports_used_this_month = Column(Integer, default=0)
    reports_limit = Column(Integer, default=3)  # Free tier limit

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def can_generate_report(self) -> bool:
        """Check if user can generate a new report."""
        return self.reports_used_this_month < self.reports_limit

    def get_remaining_reports(self) -> int:
        """Get remaining reports for current month."""
        return max(0, self.reports_limit - self.reports_used_this_month)
