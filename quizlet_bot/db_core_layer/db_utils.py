import asyncio
from sqlalchemy import Engine


async def initialize_database(engine: Engine):
    retries = 5
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")  # Just to check connection
                print("Connected to the database!")
                break
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
            await asyncio.sleep(5)
    else:
        raise Exception("Failed to connect to the database after multiple retries.")