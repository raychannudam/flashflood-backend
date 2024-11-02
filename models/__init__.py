from .user import User
from .telegram_account import TelegramAccount
from .phone_number import PhoneNumber
from .alert_service import AlertService
from .users_alert_service import UsersAlertService
from .db import get_db
from .base import SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from utils.jwt import get_hashed_password

db = SessionLocal()

def is_database_empty(db: Session) -> bool:
    return db.query(User).first() is None

def populate_users(db: Session):
    dummy_users = [
        User(id=1, username="raychannudam", email="channudam.ray@floodalert.live", status=True, password= get_hashed_password("Ranger@2002"), created_by=None, updated_by=None, created_at=datetime.now(), updated_at=datetime.now()),
    ]
    db.add_all(dummy_users)
    db.commit()

def populate_telegram_accounts(db: Session):
    dummy_telegram_accounts = [
        TelegramAccount(id=1, user_id=1, username="raychannudam", status=True, created_at=datetime.now(), updated_at=datetime.now()),
    ]
    db.add_all(dummy_telegram_accounts)
    db.commit()

def populate_phone_numbers(db: Session):
    dummy_phone_numbers = [
        PhoneNumber(id=1, user_id=1, phone_number="+85517701656", status=True, created_at=datetime.now(), updated_at=datetime.now()),
    ]
    db.add_all(dummy_phone_numbers)
    db.commit()

def populate_alert_services(db: Session):
    dummy_alert_services = [
        AlertService(id=1, name="telegram", status=True, created_at=datetime.now(), updated_at=datetime.now()),
        AlertService(id=2, name="sms", status=True, created_at=datetime.now(), updated_at=datetime.now()),
    ]
    db.add_all(dummy_alert_services)
    db.commit()

def run_populate():
    # Populate data in each table
    if is_database_empty(db):
        populate_users(db)
        populate_telegram_accounts(db)
        populate_phone_numbers(db)
        populate_alert_services(db)

    print("Dummy data has been inserted.")

