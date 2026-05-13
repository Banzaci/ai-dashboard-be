
from app.services.entity_extractor import extract_entities
from app.flows.availability_flow import availability_flow
from app.flows.wifi_flow import wifi_available_flow

def route_intent(intent: str, db, text: str):
    entities = extract_entities(text)
    if intent == "ask_wifi":
        return wifi_available_flow()

    if intent == "check_availability":
        return availability_flow(
            db=db,
            date=entities["date"],
            guests=entities["guests"]
        )

    return "default_flow"