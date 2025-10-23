"""Company model for B2B Hub."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Company(Base):
    """Company model."""

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False, index=True)
    company_type = Column(String(100))  # dobavljac, transporter, proizvodjac, itd
    description = Column(Text)
    website = Column(String(255))
    phone = Column(String(50))
    address = Column(String(500))
    city = Column(String(100))
    country = Column(String(100))
    logo_url = Column(String(500))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    listings = relationship('Listing', back_populates='company', cascade='all, delete-orphan')
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')

    def to_dict(self, include_sensitive=False):
        """Convert company to dictionary."""
        data = {
            'id': self.id,
            'email': self.email,
            'company_name': self.company_name,
            'company_type': self.company_type,
            'description': self.description,
            'website': self.website,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'logo_url': self.logo_url,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            data['password_hash'] = self.password_hash
        return data
