from fastapi import APIRouter, Query, Body
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["Отели"])

# @router.get("/")
# def func():
#     return "Hello world"


hotels = [
    {"id": 1, "title": "Сочи",  "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Париж", "name": "paris"},
    {"id": 4, "title": "Лондон","name": "london"},
    {"id": 5, "title": "Берлин","name": "berlin"},
]

class Hotels(BaseModel):
    title: str
    name: str


@router.get("")
def get_hotels(
    id:    int  | None = Query(None, description="Id"),
    title: str | None = Query(None, description="Название отеля"),
    page:      int      = Query(1,  ge=1, description="Номер страницы (по умолчанию 1)"),
    per_page:  int      = Query(3,  ge=1, description="Записей на странице (по умолчанию 3)"),
):

    # Фильтрация
    filtered = [
        h for h in hotels
        if (id is None or h["id"] == id) and (title is None or h["title"] == title)
    ]

    # Пагинация
    start = (page - 1) * per_page
    end   = start + per_page
    items = filtered[start:end]

    return {
        "total": len(filtered),   
        "page": page,
        "per_page": per_page,
        "items": items
    }


# @router.post("")
# def create_hotel(hotel_data: Hotels):
#     hotels.append({
#         "id": hotels[-1]["id"] + 1,
#         "title": hotel_data.title,
#         "name": hotel_data.name,
#     })
#     return {"status": "OK"}


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
