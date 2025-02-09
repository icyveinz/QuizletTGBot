from sqlalchemy import Engine
from db_core_layer.db_config import Base, AsyncSessionLocal


async def create_tables(engine: Engine):
    """Create tables in the database asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Provide an asynchronous session to interact with the database."""
    async with AsyncSessionLocal() as db:
        yield db