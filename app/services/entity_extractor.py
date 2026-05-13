import re
from dateparser import parse

from app.utils.extract_date import extract_date

def extract_entities(text: str):

    guests_match = re.search(r"(\d+)\s*(person|people|guests)?", text.lower())
    guests = int(guests_match.group(1)) if guests_match else 1

    date = extract_date(text)

    return {
        "guests": guests,
        "date": date
    }