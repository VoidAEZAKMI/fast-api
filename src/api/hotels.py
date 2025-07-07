from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select 
from database import async_session_maker

from api.dependencies import PaginationDep
from models.hotels import HotelsOrm
from schemas.hotels import Hotels, HotelsPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id:    int  | None = Query(None, description="Id"),
    title: str | None = Query(None, description="Название отеля"),
    
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        print(type(hotels), hotels)
        return hotels



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
            add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
            await session.execute(add_hotel_stmt)
            await session.commit()
        return {"status": "OK"}


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
