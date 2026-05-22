from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date, time

from app.core.database import get_db
from app.repositories.availability_repo import AvailabilityRepository
from app.services.availability_service import AvailabilityService
from app.schemas.schemas import AvailabilityResponse

router = APIRouter()

@router.get("/availability/", response_model=List[AvailabilityResponse])
async def get_availability(
    date: date,
    time: time,
    party: int = Query(..., ge=1),
    tz: str = "UTC",
    db: AsyncSession = Depends(get_db)
):
    repo = AvailabilityRepository(db)
    service = AvailabilityService(repo)
    
    return await service.calculate_availability(date, time, party, tz)