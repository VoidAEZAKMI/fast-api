from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(settings.DB_URL)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

session = new_session()
