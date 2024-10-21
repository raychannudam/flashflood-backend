from pydantic import BaseModel

class InfluxDataCreate(BaseModel):
    measurement: str
    station: str
    value: float