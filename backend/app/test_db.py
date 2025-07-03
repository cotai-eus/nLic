import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_db_connection():
    DATABASE_URL = "postgresql+psycopg_async://7cd0071bc256202c:0c6eccbf16a5fdb93c06f2d1a7e6a15f@db:5432/nradardb"
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            if result.scalar_one() == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed: SELECT 1 did not return 1.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db_connection())