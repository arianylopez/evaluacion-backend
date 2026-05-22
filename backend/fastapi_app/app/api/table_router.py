from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.schemas import TableTypeResponse
from app.repositories.table_repo import TableRepository

router = APIRouter()

@router.get("/types/", response_model=List[TableTypeResponse])
async def get_table_types(db: AsyncSession = Depends(get_db)):
    repo = TableRepository(db)
    return await repo.get_table_types()