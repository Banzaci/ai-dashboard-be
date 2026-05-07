# app/models/item.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)