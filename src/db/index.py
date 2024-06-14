from motor.motor_asyncio import AsyncIOMotorCollection


async def create_indexes(
        collection: AsyncIOMotorCollection
):
    await collection.create_index("dt")
    print("Index created on field 'dt'")
