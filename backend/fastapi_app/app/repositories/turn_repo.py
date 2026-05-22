from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import date, time
from uuid import UUID

from app.schemas.models import Turn, TableType, Reservation

class TurnRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_turns(self, restaurant_id: UUID):
        query = select(Turn).where(Turn.restaurant_id == restaurant_id)
        return (await self.db.execute(query)).scalars().all()

    async def get_total_capacity(self, restaurant_id: UUID) -> int:
        query = select(func.sum(TableType.seats)).where(TableType.restaurant_id == restaurant_id)
        result = await self.db.execute(query)
        capacity = result.scalar()
        return capacity or 0

    async def get_turn_occupancy(self, restaurant_id: UUID, target_date: date, start_time: time, end_time: time) -> int:
        query = select(func.sum(Reservation.party_size)).where(
            and_(
                Reservation.restaurant_id == restaurant_id,
                Reservation.date == target_date,
                Reservation.time >= start_time,
                Reservation.time <= end_time,
                Reservation.status == 'CONFIRMED'
            )
        )
        result = await self.db.execute(query)
        occupied = result.scalar()
        return occupied 