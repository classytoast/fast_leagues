import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config
from models.db.base import Base


engine = create_async_engine(Config.DATABASE_URI, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(create_tables())
