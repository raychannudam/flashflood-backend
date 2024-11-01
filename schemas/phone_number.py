from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# PhoneNumber Schemas
class PhoneNumberCreate(BaseModel):
    phone_number: str
    user_id: int


class PhoneNumberUpdate(BaseModel):
    phone_number: Optional[str] = None
    status: Optional[bool] = None

class PhoneNumberResponse(BaseModel):
    id: int
    user_id: int
    phone_number: str
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
