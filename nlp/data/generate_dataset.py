import json
import random
import re

OUTPUT_FILE = "data/raw.jsonl"
TOTAL_SAMPLES = 10000

room_types = [
    "single room", "double room", "suite",
    "family room", "deluxe room", "sea view room"
]

availability_templates = [
    "I need a room for {guests} people from {date} for {nights} nights",
    "Do you have availability from {date} for {nights} nights?",
    "Need a {room_type} from {date} for {nights} nights",
    "Can I book a room from {date} for {nights} nights?"
]

wifi_templates = [
    "Do you have wifi?",
    "Is wifi included?",
    "Does the hotel have wifi?"
]

months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]


def random_date():
    day = random.randint(1, 28)
    month = random.choice(months)

    return random.choice([
        f"{day} {month}",
        f"{day}th {month}",
        f"{day} of {month}",
        f"{month} {day}",
    ])


def add_entity(entities, text, value, label):

    for match in re.finditer(re.escape(value), text, re.IGNORECASE):

        start, end = match.start(), match.end()

        # no overlap
        if any(not (end <= e["start"] or start >= e["end"]) for e in entities):
            continue

        entities.append({
            "start": start,
            "end": end,
            "label": label
        })


def generate_availability():

    guests = str(random.randint(1, 6))
    nights = str(random.randint(1, 14))
    date = random_date()
    room_type = random.choice(room_types)

    text = random.choice(availability_templates).format(
        guests=guests,
        nights=nights,
        date=date,
        room_type=room_type
    )

    entities = []

    add_entity(entities, text, guests, "GUESTS")
    add_entity(entities, text, nights, "NIGHTS")
    add_entity(entities, text, date, "START_DATE")
    add_entity(entities, text, room_type, "ROOM_TYPE")

    return {
        "text": text,
        "intent": "check_availability",
        "entities": entities
    }


def generate_wifi():

    return {
        "text": random.choice(wifi_templates),
        "intent": "ask_wifi",
        "entities": []
    }


generators = [
    generate_availability,
    generate_wifi
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for _ in range(TOTAL_SAMPLES):
        f.write(json.dumps(random.choice(generators)(), ensure_ascii=False) + "\n")

print(f"Generated {TOTAL_SAMPLES} samples → {OUTPUT_FILE}")