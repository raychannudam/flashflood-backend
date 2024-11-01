from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from schemas import TelegramAccountCreate, TelegramAccountUpdate, TelegramAccountResponse
from services.telegram_account import create_telegram_account, get_telegram_account, update_telegram_account, delete_telegram_account

router = APIRouter()

@router.post("/", response_model=TelegramAccountResponse)
def create_account(account: TelegramAccountCreate, db: Session = Depends(get_db)):
    return create_telegram_account(db=db, telegram_account=account)

@router.get("/{user_id}", response_model=TelegramAccountResponse)
def read_account(user_id: int, db: Session = Depends(get_db)):
    db_account = get_telegram_account(db, user_id=user_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.put("/{user_id}", response_model=TelegramAccountResponse)
def update_account(user_id: int, account: TelegramAccountUpdate, db: Session = Depends(get_db)):
    db_account = update_telegram_account(db=db, user_id=user_id, telegram_account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.delete("/{user_id}", response_model=TelegramAccountResponse)
def delete_account(user_id: int, db: Session = Depends(get_db)):
    db_account = delete_telegram_account(db=db, user_id=user_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
