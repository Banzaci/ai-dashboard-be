from fastapi import APIRouter
from app.routes import auth, health, user, search

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(health.router)
api_router.include_router(user.router)
api_router.include_router(search.router)