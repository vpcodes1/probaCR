"""Message model for B2B Hub."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Message(Base):
    """Message model for company communication."""

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    sender = relationship('Company', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = relationship('Company', foreign_keys=[receiver_id], back_populates='messages_received')

    def to_dict(self):
        """Convert message to dictionary."""
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sender_name': self.sender.company_name if self.sender else None,
            'receiver_name': self.receiver.company_name if self.receiver else None
        }
