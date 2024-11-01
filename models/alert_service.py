from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class AlertService(Base):
    __tablename__ = 'alert_services'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    alert_services_users = relationship("UsersAlertService", back_populates="alert_service")
