from fastapi import APIRouter
from app.api.v1.endpoints import declarations, auth, users

api_router = APIRouter()
api_router.include_router(declarations.router, prefix="/declarations", tags=["declarations"])
# Add other routers as they are implemented
