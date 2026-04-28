from fastapi import FastAPI
from app.api.routes import api_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

app.include_router(api_router)

Base.metadata.create_all(bind=engine)