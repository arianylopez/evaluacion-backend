from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from datetime import date
from typing import List

from app.core.database import get_db
from app.core.redis import get_redis
from app.schemas.schemas import MenuItemResponse
from app.repositories.menu_repo import MenuRepository

router = APIRouter()

@router.get("/", response_model=List[MenuItemResponse])
async def get_menu(
    date: date = Query(..., description="Fecha para la cual se solicita el menú"),
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    repo = MenuRepository(db, cache)
    
    return await repo.get_menu_by_date(target_date=date)

@router.get("/search/", response_model=List[MenuItemResponse])
async def search_menu(
    query: str = Query(..., min_length=1, description="Texto a buscar en nombre o descripción"),
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    repo = MenuRepository(db, cache)
    return await repo.search_menu_items(query)