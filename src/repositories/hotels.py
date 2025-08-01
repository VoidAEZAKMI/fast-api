from sqlalchemy import insert, select, func, literal_column
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema: Hotels

    async def get_all(self, 
        location, 
        title, 
        limit, 
        offset
    ) -> list[Hotels]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Hotels.model_validate(Hotels, from_attributes=True) for hotel in result.scalars().all()]
