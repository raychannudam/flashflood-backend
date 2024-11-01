from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TelegramAccountCreate(BaseModel):
    user_id: int
    username: str = Field(..., max_length=50)

class TelegramAccountUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    status: Optional[bool] = True

class TelegramAccountResponse(BaseModel):
    id: int
    user_id: int
    username: str
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
