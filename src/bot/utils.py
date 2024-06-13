from motor.motor_asyncio import AsyncIOMotorCollection


class DataAggregator:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_aggregated_data(self, dt_from, dt_upto, group_type):
        pass
