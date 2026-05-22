from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, time
from uuid import UUID

from app.core.database import get_db
from app.schemas.schemas import AvailabilityResponse
from app.repositories.availability_repo import AvailabilityRepository

router = APIRouter()

@router.get("/availability/", response_model=List[AvailabilityResponse])
async def get_availability(
    date: date = Query(..., description="Fecha solicitada YYYY-MM-DD"),
    time: time = Query(..., description="Hora solicitada HH:MM"),
    party: int = Query(..., ge=1, description="Tamaño del grupo"),
    table_type: Optional[UUID] = Query(None, description="ID opcional del tipo de mesa"),
    tz: str = Query("UTC", description="Timezone del usuario (ej. America/La_Paz)"),
    db: AsyncSession = Depends(get_db)
):
    repo = AvailabilityRepository(db)
    return await repo.check_availability(
        target_date=date,
        target_time=time,
        party=party,
        tz=tz,
        table_type_id=table_type
    )