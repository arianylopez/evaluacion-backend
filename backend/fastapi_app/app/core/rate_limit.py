import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.redis import redis_client
from app.core.config import settings

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith(settings.API_V1_STR):
            client_ip = request.headers.get("X-Forwarded-For", request.client.host)
            client_ip = client_ip.split(",")[0].strip()
            
            key = f"rate_limit:{client_ip}"
            
            try:
                current_requests = await redis_client.incr(key)
                
                if current_requests == 1:
                    await redis_client.expire(key, 60)
                
                if current_requests > settings.RATE_LIMIT_PER_MINUTE:
                    logger.warning(f"RATE LIMIT: IP {client_ip} bloqueada por exceso de peticiones.")
                    return JSONResponse(
                        status_code=429, 
                        content={"detail": "Too Many Requests - Rate limit exceeded"}
                    )
            except Exception as e:
                logger.error(f"RATE LIMIT BYPASS: Redis inactivo. Ignorando límite. ({e})")
        
        return await call_next(request)