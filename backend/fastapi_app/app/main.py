from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import menu_router, table_router, reservation_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["*"],
)

@app.get(f"{settings.API_V1_STR}/healthz", tags=["Health"])
async def health_check():
    return {
        "status": "ok"
    }

app.include_router(menu_router.router, prefix=f"{settings.API_V1_STR}/menu", tags=["Menu"])
app.include_router(table_router.router, prefix=f"{settings.API_V1_STR}/tables", tags=["Tables"])
app.include_router(reservation_router.router, prefix=f"{settings.API_V1_STR}/reservations", tags=["Reservations"])