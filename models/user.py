from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    status = Column(Boolean, default=True)
    password = Column(String(50))
    created_by = Column(Integer, ForeignKey('users.id'))
    updated_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    created_by_user = relationship("User", remote_side=[id], foreign_keys=[created_by], backref="creators")
    updated_by_user = relationship("User", remote_side=[id], foreign_keys=[updated_by], backref="updaters")
    telegram_accounts = relationship("TelegramAccount", back_populates="user", uselist=False)
    phone_numbers = relationship("PhoneNumber", back_populates="user")
    alert_services_users = relationship("UsersAlertService", back_populates="user")
