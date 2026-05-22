from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.models import TableType, Restaurant
from app.schemas.schemas import TableTypeResponse

class TableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_table_types(self):
        rest_query = select(Restaurant).limit(1)
        rest_result = await self.db.execute(rest_query)
        restaurant = rest_result.scalar_one_or_none()

        if not restaurant:
            return []

        query = select(TableType).where(TableType.restaurant_id == restaurant.id)
        result = await self.db.execute(query)
        table_types = result.scalars().all()

        return [TableTypeResponse.model_validate(t) for t in table_types]