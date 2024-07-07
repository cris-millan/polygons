from fastapi import APIRouter

from src.routes.v1.polygons import router as polygons_router;

routers = APIRouter()
routers.include_router(polygons_router)

