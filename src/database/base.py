from typing import Collection, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import select, insert, update
from src.settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@" \
                          f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class BaseModel(DeclarativeBase):
    pass


class BaseDAO:
    model = None

    @classmethod
    async def get_by_filter(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            query_result = await session.execute(query)
            return query_result.scalars().all()

    @classmethod
    async def get_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            query_result = await session.execute(query)
            return query_result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            query_result = await session.execute(query)
            obj = query_result.scalar_one_or_none()
            if not obj:
                raise ValueError(f'id {model_id} does not exist in {cls.model.__tablename__}')
            return obj

    @classmethod
    async def create(cls, **fields):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**fields)
            result = await session.execute(query)
            await session.commit()

    @classmethod
    async def create_or_update(cls, **fields):
        pass

    @classmethod
    async def create_many(cls, objects: Collection):
        pass