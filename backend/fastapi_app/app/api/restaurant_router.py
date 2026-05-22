from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from uuid import UUID

from app.core.database import get_db
from app.repositories.turn_repo import TurnRepository
from app.services.turn_service import TurnService
from app.schemas.schemas import TurnAvailabilityResponse

router = APIRouter()

@router.get("/{id}/turns", response_model=List[TurnAvailabilityResponse])
async def get_restaurant_turns(
    id: UUID = Path(..., description="ID del Restaurante"),
    date: date = Query(..., description="Fecha objetivo (YYYY-MM-DD)"),
    tz: str = Query("UTC", description="Zona horaria (ej. America/La_Paz)"),
    db: AsyncSession = Depends(get_db)
):
    repo = TurnRepository(db)
    service = TurnService(repo)
    return await service.calculate_turn_metrics(id, date, tz)