from pydantic import BaseModel

class Hotels(BaseModel):
    title: str
    name: str

class HotelsPATCH(BaseModel):
    pass

