from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()

@app.get('/')
def func():
    return "Hello world"


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get('/hotels')
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



@app.post('/hotels')
def create_hotel(
    title: str
):
    global hotel
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}




@app.delete('/hotels/{hotel_id}')
def delete_hotel(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]

    return {"status": "OK"}



@app.put("/hotels/{hotel_id}")
def all_edit_hotel(
    hotel_id: int,
    title: str,
    name: str
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "обновлено", "hotel": hotel}
    return {"status": "не найдено"}

@app.patch("/hotels/{hotel_id}")
def edit_hotel(
    hotel_id: int,
    title: str = None,
    name: str = None
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "частично обновлен", "hotel": hotel}
    return {"status": "не найдено"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)