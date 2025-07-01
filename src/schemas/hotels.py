from pydantic import BaseModel, Field

class Hotels(BaseModel):
    title: str
    location: str

class HotelsPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)


