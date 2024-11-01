# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, text
# from sqlalchemy.ext.declarative import declarative_base
# DATABASE_URL = "sqlite:///./mrc.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# from .user import User
# # from .image import Image
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from .user import User
from .telegram_account import TelegramAccount
from .phone_number import PhoneNumber
from .alert_service import AlertService
from .users_alert_service import UsersAlertService
from .db import get_db
