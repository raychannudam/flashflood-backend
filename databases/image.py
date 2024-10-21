from sqlalchemy import Column, Integer, String
from databases import Base

# Database model
class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


