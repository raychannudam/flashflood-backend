from sqlalchemy.orm import Session
from datetime import datetime
from models.alert_service import AlertService
from schemas import AlertServiceCreate, AlertServiceUpdate

def create_alert_service(db: Session, alert_service: AlertServiceCreate):
    new_alert_service = AlertService(
        name=alert_service.name,
        status=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_alert_service)
    db.commit()
    db.refresh(new_alert_service)
    return new_alert_service

def get_alert_service(db: Session, alert_service_id: int):
    return db.query(AlertService).filter(AlertService.id == alert_service_id).first()

def get_alert_services(db: Session):
    return db.query(AlertService).all()

def update_alert_service(db: Session, alert_service_id: int, alert_service: AlertServiceUpdate):
    db_alert_service = get_alert_service(db, alert_service_id)
    if db_alert_service:
        if alert_service.name is not None:
            db_alert_service.name = alert_service.name
        if alert_service.status is not None:
            db_alert_service.status = alert_service.status
        db_alert_service.updated_at = datetime.now()
        db.commit()
        db.refresh(db_alert_service)
    return db_alert_service

def delete_alert_service(db: Session, alert_service_id: int):
    db_alert_service = get_alert_service(db, alert_service_id)
    if db_alert_service:
        db.delete(db_alert_service)
        db.commit()
    return db_alert_service
