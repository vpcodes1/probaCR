"""Listing model for B2B Hub."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base


class Listing(Base):
    """Listing model for services/products."""

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)  # transport, dobavljac, proizvodnja, itd
    subcategory = Column(String(100))  # kamionski_prevoz, sirovine, itd
    price_range = Column(String(100))  # "100-500 EUR", "Po dogovoru", itd
    location = Column(String(255))
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship('Company', back_populates='listings')

    def to_dict(self, include_company=True):
        """Convert listing to dictionary."""
        data = {
            'id': self.id,
            'company_id': self.company_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'price_range': self.price_range,
            'location': self.location,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'views_count': self.views_count,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_company and self.company:
            data['company'] = {
                'id': self.company.id,
                'company_name': self.company.company_name,
                'logo_url': self.company.logo_url,
                'city': self.company.city,
                'is_verified': self.company.is_verified
            }
        return data
