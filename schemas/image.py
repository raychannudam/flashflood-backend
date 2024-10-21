from pydantic import BaseModel

# Pydantic model for request data
class ImageCreate(BaseModel):
    name: str

# Pydantic model for response data
class ImageResponse(BaseModel):
    id: int
    name: str