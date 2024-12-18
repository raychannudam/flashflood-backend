from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=50)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    status: Optional[bool] = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
