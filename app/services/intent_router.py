
import re

from app.db import session
from app.services.entity_extractor import extract_entities
from app.flows.availability_flow import availability_flow
from app.flows.wifi_flow import wifi_available_flow
from app.services.session_store import sessions
from datetime import datetime, timedelta
from app.services.entity_extractor import extract_entities

def route_intent(intent: str, db, text: str, session_id: str):

    # -----------------------
    # session load
    # -----------------------
    session = sessions.get(session_id, {})

    print(f"Routing intent: {intent}, session_id: {session_id}, session state: {session}")

    # -----------------------
    # entity extraction
    # -----------------------
    entities = extract_entities(text)

    guests = entities["guests"]
    start_date = entities["start_date"]
    end_date = entities["end_date"]

    # -----------------------
    # update session state
    # -----------------------
    if guests:
        session["guests"] = guests
    if start_date:
        session["start_date"] = start_date
    if end_date:
        session["end_date"] = end_date

    sessions[session_id] = session

    print(f"Extracted entities: {entities}, updated session state: {session}")

    # -----------------------
    # wifi intent
    # -----------------------
    if intent == "ask_wifi":
        return wifi_available_flow()
    
    is_followup = (
        session.get("start_date")
        and not session.get("end_date")
    )

    text_clean = text.lower().strip()

    nights_match = re.fullmatch(r"(\d+)\s*(nights?)?", text_clean)

    if is_followup and nights_match:

        nights = int(nights_match.group(1))

        start_date = datetime.strptime(session["start_date"], "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=nights)

        session["end_date"] = end_date.isoformat()
        sessions[session_id] = session

        return availability_flow(
            db=db,
            guests=session.get("guests", guests),
            start_date=session["start_date"],
            end_date=session["end_date"]
        )

    # -----------------------
    # availability intent
    # -----------------------
    if intent == "check_availability":
        if session.get("start_date") and not session.get("end_date"):
            return {
                "message": "For how many nights?",
                "status": "missing_nights"
            }

        return availability_flow(
            db=db,
            guests=session.get("guests", guests),
            start_date=session.get("start_date"),
            end_date=session.get("end_date")
        )

    return "no match"