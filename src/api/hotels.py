from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, func, literal_column
from database import async_session_maker

from api.dependencies import PaginationDep
from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from schemas.hotels import Hotels, HotelsPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Месторасположение"),
    title: str | None = Query(None, description="Название отеля"),
    
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location, 
            title=title, 
            limit=per_page, 
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(hotel_data: Hotels = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                },
            },
        })):
        async with async_session_maker() as session:
            hotel = await HotelsRepository(session).add(hotel_data)
            await session.commit()
            
        return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotels):
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"]  = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    name:  str | None = Body(None),
):
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}
