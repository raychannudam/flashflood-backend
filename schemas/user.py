from pydantic import BaseModel

# Pydantic model for request data
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Pydantic model for response data
class UserResponse(BaseModel):
    id: int
    username: str
    email: str