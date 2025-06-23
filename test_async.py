
# @router.get("/sync/{id}")
# def sync_func(id: int):
#     print(f"sync. Начало {id}: {time.time():.2f}")
#     time.sleep(3)
#     print(f"sync. Закончил {id}: {time.time():.2f}")


# @router.get("/async/{id}")
# async def async_func(id: int):
#     print(f"async. Начало {id}: {time.time():.2f}")
#     await asyncio.sleep(3)
#     print(f"async. Закончил {id}: {time.time():.2f}")