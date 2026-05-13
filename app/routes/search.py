from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.db.session import get_db
from app.db.redis_client import r
from app.models.item import Item
from app.services.intent_router import route_intent
from app.services.search_service import search_training_questions

router = APIRouter()

@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):

    result = search_training_questions(db, q)

    if not result:
        return {"message": "no match"}

    return route_intent(
        result["intent"],
        db=db,
        text=q
    )
# @router.get("/search")
# def search(q: str, db: Session = Depends(get_db)):
    
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