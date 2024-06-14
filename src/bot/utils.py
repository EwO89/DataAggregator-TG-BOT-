import calendar
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection


class DataAggregator:
    def __init__(
            self,
            data_collection: AsyncIOMotorCollection
    ) -> None:
        self.data_collection = data_collection

    async def get_aggregated_data(
            self, dt_from: datetime,
            dt_upto: datetime,
            group_type: str
    ):
        dt_format = {
            'hour': '%Y-%m-%dT%H', 'day': '%Y-%m-%d', 'month': '%Y-%m'
        }[group_type]
        iso_format = {
            'hour': ':00:00', 'day': 'T00:00:00', 'month': '-01T00:00:00'
        }[group_type]

        query = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {"$group": {"_id": {"$dateToString": {"format": dt_format, "date": "$dt"}},
                        "sum_value": {"$sum": '$value'}}},
            {"$sort": {"_id": 1}}
        ]

        cursor = self.data_collection.aggregate(query)
        data = {}
        async for doc in cursor:
            dt_raw = datetime.fromisoformat(doc['_id'] + iso_format)
            data[dt_raw] = doc['sum_value']

        result_data = []
        result_labels = []

        current_date = dt_from
        if group_type == 'hour':
            delta = timedelta(hours=1)
        elif group_type == 'day':
            delta = timedelta(days=1)
        else:
            def month_delta(date):
                if date.month == 12:
                    return datetime(date.year + 1, 1, date.day) - date
                else:
                    return datetime(date.year, date.month + 1, date.day) - date

            delta = month_delta(current_date)

        while current_date <= dt_upto:
            dt_iso = datetime.isoformat(current_date)
            result_labels.append(dt_iso)
            result_data.append(data.get(current_date, 0))

            if group_type == 'month':
                current_date += timedelta(days=calendar.monthrange(current_date.year, current_date.month)[1])
            else:
                current_date += delta

        return {'dataset': result_data, 'labels': result_labels}
