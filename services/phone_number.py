from sqlalchemy.orm import Session
from models.phone_number import PhoneNumber
from schemas import PhoneNumberCreate, PhoneNumberUpdate
from datetime import datetime

def create_phone_number(db: Session, phone_number_data: PhoneNumberCreate):
    db_phone_number = PhoneNumber(
        phone_number=phone_number_data.phone_number,
        user_id=phone_number_data.user_id,
        status=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    return db_phone_number

def get_phone_number(db: Session, user_id: int):
    return db.query(PhoneNumber).filter(PhoneNumber.user_id == user_id).all()

def update_phone_number(db: Session, phone_number_id, phone_number_data: PhoneNumberUpdate):
    db_phone_number = db.query(PhoneNumber).filter(PhoneNumber.id == phone_number_id).first()
    if db_phone_number:
        for key, value in phone_number_data.dict(exclude_unset=True).items():
            setattr(db_phone_number, key, value)
        db.commit()
        db.refresh(db_phone_number)
    return db_phone_number

def delete_phone_number(db: Session, phone_number_id: int):
    db_phone_number = db.query(PhoneNumber).filter(PhoneNumber.phone_number_id == id).first()
    if db_phone_number:
        db.delete(db_phone_number)
        db.commit()
    return db_phone_number
