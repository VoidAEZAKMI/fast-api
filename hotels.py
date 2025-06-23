from fastapi import  Query, APIRouter, Body
from pydantic import BaseModel
import time
import asyncio

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get('/')
def func():
    return "Hello world"


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]

class Hotels(BaseModel):
    title: str
    name: str



@router.get('/hotels')
def get_hotels(
    id: int  = Query(None, description="Id"), 
    title: str  = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_



@router.post('')
def create_hotel(hotel_data: Hotels):
    global hotel
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}





@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int,hotel_data: Hotels):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}



@router.delete('/{hotel_id}')
def delete_hotel(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}