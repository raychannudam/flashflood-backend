from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UsersAlertService(Base):
    __tablename__ = 'users_alert_services'
    
    id = Column(Integer, primary_key=True, index=True)
    alert_service_id = Column(Integer, ForeignKey('alert_services.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    alert_service = relationship("AlertService", back_populates="alert_services_users")
    user = relationship("User", back_populates="alert_services_users")
