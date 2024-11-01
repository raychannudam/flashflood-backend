from sqlalchemy.orm import Session
from fastapi import Depends
from .base import SessionLocal

# Dependency to get the database session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
