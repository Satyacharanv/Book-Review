import asyncio
from app.db import engine
from app.db_base import Base
from app.models import book, review  # Ensure models are registered

async def create_tables():
    """Create all database tables defined in the models."""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables()) 