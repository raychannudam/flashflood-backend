from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from schemas import PhoneNumberCreate, PhoneNumberUpdate, PhoneNumberResponse
from services.phone_number import create_phone_number, get_phone_number, update_phone_number, delete_phone_number

router = APIRouter()

@router.post("/", response_model=PhoneNumberResponse)
def create_phone_number_for_user(phone_number: PhoneNumberCreate, db: Session = Depends(get_db)):
    return create_phone_number(db=db, phone_number_data=phone_number)

@router.get("/{user_id}", response_model=list[PhoneNumberResponse])
def read_phone_number(user_id: int, db: Session = Depends(get_db)):
    db_phone_number = get_phone_number(db, user_id)
    if db_phone_number is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return db_phone_number

@router.put("/{phone_number_id}", response_model=PhoneNumberResponse)
def update_existing_phone_number(phone_number_id: int,  phone_number: PhoneNumberUpdate, db: Session = Depends(get_db)):
    db_phone_number = update_phone_number(db, phone_number_id, phone_number)
    if db_phone_number is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return db_phone_number

@router.delete("/{phone_number_id}")
def delete_existing_phone_number(phone_number_id: int, db: Session = Depends(get_db)):
    db_phone_number = delete_phone_number(db, phone_number_id)
    if db_phone_number is None:
        raise HTTPException(status_code=404, detail="Phone number not found")
    return {"message": "Phone number deleted successfully"}
