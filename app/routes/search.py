from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.db.redis_client import r
from app.models.item import Item

router = APIRouter()

@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    
    cache_key = f"search:{q.lower()}"
    cached = r.get(cache_key)
    if cached:
      return {
          "source": "cache",
          "data": json.loads(cached) # type: ignore
      }

    # 2. DB query
    results = (
        db.query(Item)
        .filter(Item.name.contains(q))
        .all()
    )

    data = [
        {"id": i.id, "name": i.name}
        for i in results
    ]

    # 3. Spara i cache (TTL = 5 min)
    r.setex(cache_key, 300, json.dumps(data))

    return {
        "source": "db",
        "data": data
    }