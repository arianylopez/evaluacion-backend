from datetime import date, time, datetime
from zoneinfo import ZoneInfo
import logging
from uuid import UUID

from app.schemas.schemas import AvailabilityResponse
from app.core.protocols import AvailabilityRepoInterface

logger = logging.getLogger(__name__)

class AvailabilityService:
    def __init__(self, repo: AvailabilityRepoInterface):
        self.repo = repo

    async def calculate_availability(self, target_date: date, target_time: time, party: int, tz: str, table_type_id: UUID = None):
        try:
            user_tz = ZoneInfo(tz)
            aware_dt = datetime.combine(target_date, target_time, tzinfo=user_tz)
            logger.info(f"Calculando disponibilidad para {aware_dt.isoformat()} ({tz})")
        except Exception as e:
            logger.warning(f"ZONA HORARIA INVÁLIDA: {tz}. Usando UTC. Error: {e}")

        restaurant = await self.repo.get_restaurant()
        if not restaurant: return []

        table_types = await self.repo.get_table_types(restaurant.id, table_type_id)
        occupied_map = await self.repo.get_occupied_seats(target_date, target_time)

        availabilities = []
        for table in table_types:
            occupied = occupied_map.get(table.id, 0)
            available_seats = table.seats - occupied
            
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