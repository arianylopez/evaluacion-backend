# backend/fastapi_app/app/repositories/availability_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import date, time
from uuid import UUID

from app.schemas.models import TableType, Reservation, Restaurant

class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_restaurant(self):
        rest_query = select(Restaurant).limit(1)
        result = await self.db.execute(rest_query)
        return result.scalar_one_or_none()

    async def get_table_types(self, restaurant_id: UUID, table_type_id: UUID = None):
        query = select(TableType).where(TableType.restaurant_id == restaurant_id)
        if table_type_id:
            query = query.where(TableType.id == table_type_id)
        return (await self.db.execute(query)).scalars().all()

    async def get_occupied_seats(self, target_date: date, target_time: time):
        occupied_query = select(
            Reservation.table_type_id, 
            func.sum(Reservation.party_size).label('total_reserved')
        ).where(
            Reservation.date == target_date,
            Reservation.time == target_time,
            Reservation.status == 'CONFIRMED'
        ).group_by(Reservation.table_type_id)
        
        results = (await self.db.execute(occupied_query)).all()
        return {row.table_type_id: row.total_reserved for row in results}