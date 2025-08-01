from fastapi import APIRouter, Query, Body
from database import async_session_maker

from api.dependencies import PaginationDep
from repositories.hotels import HotelsRepository
from schemas.hotels import HotelAdd, Hotels, HotelsPATCH

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
    
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id) 


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelsPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
