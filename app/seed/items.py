from app.db.session import engine, SessionLocal
from app.models.item import Item
from app.db.base import Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    items = [
        Item(name="Apple", description="A fruit"),
        Item(name="Banana", description="Yellow fruit"),
        Item(name="Laptop", description="Device"),
    ]

    db.add_all(items)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Seed completed")