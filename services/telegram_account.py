from sqlalchemy.orm import Session
from datetime import datetime
from models.telegram_account import TelegramAccount
from schemas import TelegramAccountCreate, TelegramAccountUpdate

def create_telegram_account(db: Session, telegram_account: TelegramAccountCreate):
    new_account = TelegramAccount(
        user_id=telegram_account.user_id,
        username=telegram_account.username,
        status=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def get_telegram_account(db: Session, user_id: int):
    return db.query(TelegramAccount).filter(TelegramAccount.user_id == user_id).first()

def update_telegram_account(db: Session, user_id: int, telegram_account: TelegramAccountUpdate):
    db_account = get_telegram_account(db, user_id)
    if db_account:
        db_account.username = telegram_account.username or db_account.username
        db_account.status = telegram_account.status if telegram_account.status is not None else db_account.status
        db_account.updated_at = datetime.now()
        db.commit()
        db.refresh(db_account)
    return db_account

def delete_telegram_account(db: Session, user_id: int):
    db_account = get_telegram_account(db, user_id)
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account
