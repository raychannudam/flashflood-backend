from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertServiceCreate(BaseModel):
    name: str

class AlertServiceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None

class AlertServiceResponse(BaseModel):
    id: int
    name: str
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
