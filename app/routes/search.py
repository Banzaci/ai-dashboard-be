from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import spacy
import json
import dateparser
from app.services.availability_service import search_available_rooms
from app.db.session import get_db
from app.db.redis_client import r

router = APIRouter()
nlp = spacy.load("./nlp/model/model-best")

SESSION_TTL = 60 * 30  # 30 minuter

REQUIRED_SLOTS = ["START_DATE", "GUESTS"]
FOLLOWUP_QUESTIONS = {
    "NIGHTS":     "How many nights would you like to stay?",
    "START_DATE": "What date would you like to check in?",
    "GUESTS":     "How many guests will be staying?",
}

FAQ_ANSWERS = {
    "ask_wifi":      "Yes, we offer free WiFi throughout the hotel. The password is provided at check-in.",
    "ask_parking":   "We have free parking on site. No reservation needed.",
    "ask_breakfast": "Breakfast is served 07:00–10:00 in the main restaurant.",
    "ask_pool":      "Yes, we have a pool open daily 08:00–21:00.",
}

class SearchPayload(BaseModel):
    text: str
    session_id: str = "default"

class BookingQuery(BaseModel):
    check_in: str
    check_out: str
    guests: int
    rooms: int = 1

def to_int(value: str) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    word_map = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20,
    }
    return word_map.get(value.lower().strip())

def get_session(session_id: str) -> dict:
    data = r.get(f"session:{session_id}")
    if not data:
        return {"slots": {}, "pending_slot": None}
    return json.loads(str(data))

def save_session(session_id: str, session: dict):
    r.setex(f"session:{session_id}", SESSION_TTL, json.dumps(session))

def delete_session(session_id: str):
    r.delete(f"session:{session_id}")

def parse_entities(text: str) -> dict:
    doc = nlp(text)
    return {ent.label_: ent.text for ent in doc.ents}

def resolve_date(date_str: str) -> str | None:
    parsed = dateparser.parse(
        date_str,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False,
        }
    )
    if not parsed:
        return None
    if parsed.date() < datetime.today().date():
        return None
    return parsed.strftime("%Y-%m-%d")

def find_missing_slots(slots: dict) -> str | None:
    for slot in [*REQUIRED_SLOTS, "NIGHTS"]:
        if slot not in slots:
            return slot
    return None

def build_db_query(slots: dict) -> BookingQuery | None:
    check_in = resolve_date(slots.get("START_DATE", ""))
    if not check_in:
        return None
    nights = to_int(slots.get("NIGHTS", "1")) or 1
    guests = to_int(slots.get("GUESTS", ""))
    if not guests:
        return None
    check_out = (
        datetime.strptime(check_in, "%Y-%m-%d") + timedelta(days=nights)
    ).strftime("%Y-%m-%d")
    return BookingQuery(
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        rooms=to_int(slots.get("ROOMS", "1")) or 1,
    )


def handle_booking(q: str, session_id: str, db: Session) -> dict:
    session = get_session(session_id)
    slots   = session["slots"]

    if session["pending_slot"]:
        slots[session["pending_slot"]] = q
        session["pending_slot"] = None
    else:
        slots.update(parse_entities(q))

    missing = find_missing_slots(slots)
    if missing:
        session["pending_slot"] = missing
        save_session(session_id, session)
        return {"status": "follow_up", "question": FOLLOWUP_QUESTIONS[missing]}

    query = build_db_query(slots)
    delete_session(session_id)

    if not query:
        return {"status": "error", "message": "Could not parse date or guests"}

    # ← Sök i databasen
    results = search_available_rooms(
        db,
        check_in=query.check_in,
        check_out=query.check_out,
        guests=query.guests,
        rooms=query.rooms,
    )

    return {
        "status":  "ready",
        "query":   query.model_dump(),
        "results": results,
        "count":   len(results),
    }

@router.post("/search")
def search(payload: SearchPayload, db: Session = Depends(get_db)):
    q          = payload.text.strip()
    session_id = payload.session_id

    if not q:
        return {"status": "error", "message": "Missing text"}

    # ← Kolla pending_slot FÖRST innan NLP körs
    session = get_session(session_id)
    if session["pending_slot"]:
        print(f"Pending slot: {session['pending_slot']}, filling with: {q}")
        return handle_booking(q, session_id, db)

    # Ingen pending slot – klassificera intent
    doc = nlp(q)
    cats: dict[str, float] = dict(doc.cats)
    intent = max(cats, key=lambda k: cats[k])
    confidence = cats[intent]

    print(f"Intent: {intent}, Confidence: {confidence}")

    if confidence < 0.6:
        return {
            "status":  "unknown",
            "message": "I'm not sure I understood that. You can ask about availability, WiFi, or opening hours."
        }

    if intent in FAQ_ANSWERS:
        return {"status": "faq", "answer": FAQ_ANSWERS[intent]}

    if intent == "check_availability":
        return handle_booking(q, session_id, db)

    return {
        "status":  "unknown",
        "message": "I'm not sure I understood that. You can ask about availability, WiFi, or opening hours."
    }