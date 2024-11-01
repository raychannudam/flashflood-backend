from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from schemas import UserCreate, UserUpdate
from utils.jwt import get_hashed_password

def create_user(db: Session, user: UserCreate):
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password),
        status=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user.username or db_user.username
        db_user.email = user.email or db_user.email
        db_user.status = user.status if user.status is not None else db_user.status
        db_user.updated_at = datetime.now()
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
