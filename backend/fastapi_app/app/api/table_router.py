from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.schemas import TableTypeResponse
from app.repositories.table_repo import TableRepository

router = APIRouter()

@router.get("/types/", response_model=List[TableTypeResponse])
async def get_table_types(
    skip: int = Query(0, ge=0, description="Número de registros a saltar (paginación offset)"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a retornar"),
    db: AsyncSession = Depends(get_db)
):
    repo = TableRepository(db)
    return await repo.get_table_types(skip=skip, limit=limit)