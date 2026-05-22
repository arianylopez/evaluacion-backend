from datetime import date, datetime
from zoneinfo import ZoneInfo
import logging
from uuid import UUID

from app.schemas.schemas import TurnAvailabilityResponse
from app.core.protocols import TurnRepoInterface

logger = logging.getLogger(__name__)

class TurnService:
    def __init__(self, repo: TurnRepoInterface):
        self.repo = repo

    async def calculate_turn_metrics(self, restaurant_id: UUID, target_date: date, tz: str):
        try:
            user_tz = ZoneInfo(tz)
            logger.info(f"Calculando métricas de turnos para {target_date} en la zona {user_tz}")
        except Exception as e:
            logger.warning(f"ZONA HORARIA INVÁLIDA: {tz}. Error: {e}")

        turns = await self.repo.get_turns(restaurant_id)
        if not turns:
            return []

        total_capacity = await self.repo.get_total_capacity(restaurant_id)

        response_list = []
        for turn in turns:
            confirmed = await self.repo.get_turn_occupancy(
                restaurant_id, target_date, turn.start_time, turn.end_time
            )

            if total_capacity > 0:
                occupancy_percentage = round((confirmed / total_capacity) * 100, 2)
            else:
                occupancy_percentage = 0.0

            is_closed = occupancy_percentage >= 100.0 or total_capacity == 0

            response_list.append(TurnAvailabilityResponse(
                name=turn.name,
                start_time=turn.start_time,
                end_time=turn.end_time,
                total_capacity=total_capacity,
                confirmed_reservations=confirmed,
                occupancy_percentage=occupancy_percentage,
                is_closed=is_closed
            ))

        return response_list