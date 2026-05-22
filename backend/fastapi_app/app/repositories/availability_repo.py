import logging
from zoneinfo import ZoneInfo
from datetime import date, time, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from uuid import UUID

from app.schemas.models import TableType, Reservation, Restaurant
from app.schemas.schemas import AvailabilityResponse

logger = logging.getLogger(__name__)

class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_availability(self, target_date: date, target_time: time, party: int, tz: str, table_type_id: UUID = None):
        try:
            user_tz = ZoneInfo(tz)
            aware_dt = datetime.combine(target_date, target_time, tzinfo=user_tz)
            logger.info(f"TIMEZONE: Calculando disponibilidad exacta para {aware_dt.isoformat()} en zona {tz}")
        except Exception as e:
            logger.warning(f"ZONA HORARIA INVÁLIDA: {tz}. Cayendo a UTC. Error: {e}")

        rest_query = select(Restaurant).limit(1)
        restaurant = (await self.db.execute(rest_query)).scalar_one_or_none()
        if not restaurant: return []

        query = select(TableType).where(TableType.restaurant_id == restaurant.id)
        if table_type_id:
            query = query.where(TableType.id == table_type_id)
        
        table_types = (await self.db.execute(query)).scalars().all()
        availabilities = []

        for table in table_types:
            res_query = select(func.coalesce(func.sum(Reservation.party_size), 0)).where(
                and_(
                    Reservation.table_type_id == table.id,
                    Reservation.date == target_date,
                    Reservation.time == target_time,
                    Reservation.status == 'CONFIRMED'
                )
            )
            occupied_seats = (await self.db.execute(res_query)).scalar()

            available_seats = table.seats - occupied_seats

            if available_seats >= party:
                availabilities.append(AvailabilityResponse(
                    time=target_time.strftime("%H:%M"),
                    table_type=table.id,
                    table_type_name=table.name,
                    seats=table.seats,
                    available_seats=available_seats,
                    price_per_seat=float(table.price_per_seat)
                ))
        
        return availabilities