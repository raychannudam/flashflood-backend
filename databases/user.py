from sqlalchemy import Column, Integer, String
from databases import Base

# Database model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String)
    password = Column(String)


