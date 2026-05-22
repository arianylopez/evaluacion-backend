import json
import logging
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as redis

from app.schemas.models import MenuItem
from app.schemas.schemas import MenuItemResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MenuRepository:
    def __init__(self, db: AsyncSession, cache: redis.Redis):
        self.db = db
        self.cache = cache

    async def get_menu_by_date(self, target_date: datetime.date):
        cache_key = f"menu:{target_date.isoformat()}"

        try:
            cached_data = await self.cache.get(cache_key)
            if cached_data:
                logger.info(f"CACHE HIT: Menú cargado desde Redis para {target_date}")
                items_dict = json.loads(cached_data)
                return [MenuItemResponse(**item) for item in items_dict]
        except Exception as e:
            logger.warning(f"CACHE ERROR: Redis falló o está inactivo ({e})")

        logger.info(f"DB QUERY: Consultando el menú en PostgreSQL para {target_date}")
        query = select(MenuItem).where(MenuItem.date == target_date)
        result = await self.db.execute(query)
        menu_items_orm = result.scalars().all()

        response_data = [MenuItemResponse.model_validate(item) for item in menu_items_orm]

        try:
            if response_data:
                json_data = json.dumps([item.model_dump(mode='json') for item in response_data])
                await self.cache.setex(cache_key, 120, json_data)
                logger.info(f"CACHE SAVED: Menú guardado en Redis")
        except Exception as e:
            logger.warning(f"CACHE WRITE ERROR: No se pudo guardar ({e})")

        return response_data