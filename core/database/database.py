from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from .env import load_dotenv
import os

load_dotenv()


class Database:
    # Step 1: Hold MongoDB client
    client: AsyncIOMotorClient | None = None

    # Step 2: Hold ODMantic engine
    engine: AIOEngine | None = None


# Step 3: Create a single shared database instance
db_instance = Database()


async def connect_to_mongo():
    # Step 4: Create MongoDB client (lazy connection)
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)

    # Step 5: Create ODMantic engine using the client
    db_instance.engine = AIOEngine(
        client=db_instance.client,
        database=settings.DATABASE_NAME,
    )

    # Step 6: Force a real connection check
    await db_instance.client[settings.DATABASE_NAME].command("ping")

    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")


async def close_mongo_connection():
    # Step 7: Close MongoDB client during shutdown
    if db_instance.client:
        db_instance.client.close()
        print("Closed MongoDB connection")


def get_engine() -> AIOEngine:
    # Step 8: Provide ODMantic engine for CRUD operations
    return db_instance.engine
