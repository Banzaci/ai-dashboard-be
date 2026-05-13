# app/db/init_db.py

from app.db.session import engine
from app.db.base import Base

# import ALL models så SQLAlchemy känner till dem
from app.models.training_question import TrainingQuestion 
from app.models.user import User
from app.models.room import Room


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized")