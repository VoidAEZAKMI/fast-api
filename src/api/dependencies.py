from typing import Annotated


from fastapi import Depends, Query
from pydantic import BaseModel

class ParamsPagination(BaseModel):
    page:  Annotated[int | None,  Query(1,  ge=1, description="Номер страницы (по умолчанию 1)")]
    per_page: Annotated[int | None,  Query(3,  ge=1, description="Записей на странице (по умолчанию 3)")]


PaginationDep = Annotated[ParamsPagination, Depends()]