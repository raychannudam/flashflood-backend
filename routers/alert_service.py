from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from schemas import AlertServiceCreate, AlertServiceUpdate, AlertServiceResponse
from services.alert_service import create_alert_service, get_alert_service, update_alert_service, delete_alert_service, get_alert_services

router = APIRouter()

@router.post("/", response_model=AlertServiceResponse)
def create_service(service: AlertServiceCreate, db: Session = Depends(get_db)):
    return create_alert_service(db=db, alert_service=service)

@router.get("/", response_model=list[AlertServiceResponse])
def read_services(db: Session = Depends(get_db)):
    return get_alert_services(db)

@router.get("/{service_id}", response_model=AlertServiceResponse)
def read_service(service_id: int, db: Session = Depends(get_db)):
    db_service = get_alert_service(db, alert_service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Alert service not found")
    return db_service

@router.put("/{service_id}", response_model=AlertServiceResponse)
def update_service(service_id: int, service: AlertServiceUpdate, db: Session = Depends(get_db)):
    db_service = update_alert_service(db=db, alert_service_id=service_id, alert_service=service)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Alert service not found")
    return db_service

@router.delete("/{service_id}", response_model=AlertServiceResponse)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = delete_alert_service(db=db, alert_service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Alert service not found")
    return db_service
